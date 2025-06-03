import cv2 as cv
import numpy as np
import sys
import pandas as pd
from ultralytics import YOLO
from ouster.sdk import client, sensor
from time import time_ns

from contextlib import closing
from tracker.track import traj_store
from tracker import register_tracker

#------------------ BEV CONVERSION ARGS AND FUNCTIONS ---------------------#
BEV_HEIGHT = 608
BEV_WIDTH = 608

boundary = {
    "minX": 0,
    "maxX": 50,
    "minY": -25,
    "maxY": 25,
    "minZ": -1.73,
    "maxZ": 2.27
}

DISCRETIZATION = (boundary["maxX"] - boundary["minX"]) / 608


def removePoints(PointCloud, BoundaryCond):
    # Boundary condition
    minX = BoundaryCond['minX']
    maxX = BoundaryCond['maxX']
    minY = BoundaryCond['minY']
    maxY = BoundaryCond['maxY']
    minZ = BoundaryCond['minZ']
    maxZ = BoundaryCond['maxZ']

    # Remove the point out of range x,y,z
    mask = np.where((PointCloud[:, 0] >= minX) & (PointCloud[:, 0] <= maxX) & (PointCloud[:, 1] >= minY) & (
            PointCloud[:, 1] <= maxY) & (PointCloud[:, 2] >= minZ) & (PointCloud[:, 2] <= maxZ))
    PointCloud = PointCloud[mask]

    PointCloud[:, 2] = PointCloud[:, 2] - minZ

    return PointCloud


def makeBVFeature(PointCloud_, Discretization, bc):
    Height = BEV_HEIGHT + 1
    Width = BEV_WIDTH + 1

    # Discretize Feature Map
    PointCloud = np.copy(PointCloud_)
    PointCloud[:, 0] = np.int_(np.floor(PointCloud[:, 0] / Discretization))
    PointCloud[:, 1] = np.int_(np.floor(PointCloud[:, 1] / Discretization) + Width / 2)

    # sort-3times
    indices = np.lexsort((-PointCloud[:, 2], PointCloud[:, 1], PointCloud[:, 0]))
    PointCloud = PointCloud[indices]

    # Height Map
    heightMap = np.zeros((Height, Width))

    _, indices = np.unique(PointCloud[:, 0:2], axis=0, return_index=True)
    PointCloud_frac = PointCloud[indices]
    # some important problem is image coordinate is (y,x), not (x,y)
    max_height = float(np.abs(bc['maxZ'] - bc['minZ']))
    heightMap[np.int_(PointCloud_frac[:, 0]), np.int_(PointCloud_frac[:, 1])] = PointCloud_frac[:, 2] / max_height

    # Intensity Map & DensityMap
    intensityMap = np.zeros((Height, Width))
    densityMap = np.zeros((Height, Width))

    _, indices, counts = np.unique(PointCloud[:, 0:2], axis=0, return_index=True, return_counts=True)
    PointCloud_top = PointCloud[indices]

    normalizedCounts = np.minimum(1.0, np.log(counts + 1) / np.log(64))

    intensityMap[np.int_(PointCloud_top[:, 0]), np.int_(PointCloud_top[:, 1])] = PointCloud_top[:, 3]
    densityMap[np.int_(PointCloud_top[:, 0]), np.int_(PointCloud_top[:, 1])] = normalizedCounts

    RGB_Map = np.zeros((3, Height - 1, Width - 1))
    RGB_Map[2, :, :] = densityMap[:BEV_HEIGHT, :BEV_WIDTH]  # r_map
    RGB_Map[1, :, :] = heightMap[:BEV_HEIGHT, :BEV_WIDTH]  # g_map
    RGB_Map[0, :, :] = intensityMap[:BEV_HEIGHT, :BEV_WIDTH]  # b_map

    return RGB_Map

#------------------- SENSOR SETUP -------------------#
# set up the sensor
hostname = "169.254.166.184"   # set the actual IP address or the hostname of the sensor
lidar_port = None		# Setting port automatically on runtime is not configured

#------------------- MAIN LOGIC --------------------#
if __name__ == '__main__':
    # Initializing Model and csv logger
    model = YOLO('models/Pytorch/YOLO_11s/epoch525_11s.pt', task='obb')  # insert model here

    register_tracker(model, persist=True)
    
    data_frame = pd.DataFrame(columns=["duration", "id", "cls", "coords"])
    
    # recording video
    out_cap = cv.VideoWriter(
        f'live_recording.avi', # this time it was 525+57=582 
        cv.VideoWriter_fourcc(*'MJPG'),
        10, 
        (608, 608)
    )
    
    start_time = time_ns()
    
    with closing(sensor.SensorScanSource(hostname, lidar_port=lidar_port,
                                         complete=False)) as stream:
        xyz_LUT = client.XYZLut(stream.metadata[0], True)
        try:
            for scan, *_ in stream:
                # Getting LiDAR frame
                xyz = xyz_LUT(scan.field(client.ChanField.RANGE))
                sig = scan.field(client.ChanField.SIGNAL)
                  
                # LiDAR PC -> BEV
                sig = cv.normalize(sig, None, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)
                xyzi = np.concatenate((xyz, sig[..., np.newaxis]), axis=-1)
                xyzi = removePoints(xyzi.reshape(-1, 4), boundary)
                bev = makeBVFeature(xyzi, DISCRETIZATION, boundary)
                bev = (bev * 255).astype(np.uint8)
                bev = np.transpose(bev, (1, 2, 0))
                frame = cv.flip(bev, -1)
                
                # Ultralytics model on BEV
                results = model.track(frame, persist=True, imgsz=608, half=True) #, verbose=False)		# conf=0.05, iou=0.05
                boxes = results[0].obb.xywhr.cpu()
                annotated_frame = results[0].plot(conf=False, labels=False)
                if len(traj_store.keys()) != 0:
                    traj = np.stack(traj_store[0]).transpose(1, 0, 2)
                    index = 0
                    for tra in traj:
                        points = tra.astype(np.int32).reshape((-1, 1, 2))
                        cv.polylines(annotated_frame, [points], isClosed=False, color=(230, 230, 230), thickness=2)
                        cv.line(annotated_frame, (294, 582), (314, 582), color=(0, 230, 230), thickness=2)
                        cv.line(annotated_frame, (294, 582), (294, 608), color=(0, 230, 230), thickness=2)
                        cv.line(annotated_frame, (314, 582), (314, 608), color=(0, 230, 230), thickness=2)
                        try:
                            # Duration is in milliseconds
                            data_frame.loc[len(data_frame)] = {"duration": round((time_ns() - start_time) / 10e6, 2), "id": results[0].obb.id[index].item(), "cls": results[0].obb.cls[index].item(), "coords": [points]}
                        except:
                            continue
                        index += 1
                cv.imshow("runtime output", annotated_frame)
                out_cap.write(annotated_frame)
                cv.waitKey(75)
        except KeyboardInterrupt:
            cv.destroyAllWindows()
            data_frame.to_csv('live_output_obb.csv')
            out_cap.release()
            print("Complete")

