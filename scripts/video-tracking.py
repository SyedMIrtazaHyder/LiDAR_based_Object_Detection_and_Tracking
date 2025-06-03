import sys
from ultralytics import YOLO
from tracker.track import traj_store
from tracker import register_tracker
import cv2 as cv
import numpy as np



if __name__ == '__main__':
    model = YOLO('models/Pytorch/YOLO_11s/epoch525_11s.pt', task="obb")  # insert model here
    register_tracker(model, persist=True)

    video_path = sys.argv[1]
    cap = cv.VideoCapture(video_path)
    out_cap = cv.VideoWriter(
        f'{video_path}_result.avi', # this time it was 525+57=582 
        cv.VideoWriter_fourcc(*'MJPG'),
        10, 
        (608, 608)
    )

    while cap.isOpened():
        success, frame = cap.read()
        if success:
            results = model.track(frame, persist=True)
            boxes = results[0].obb.xywhr.cpu()
            annotated_frame = results[0].plot(conf=False, labels=False)
            if len(traj_store.keys()) != 0:
                traj = np.stack(traj_store[0]).transpose(1, 0, 2)
                for tra in traj:
                    points = tra.astype(np.int32).reshape((-1, 1, 2))
                    cv.polylines(annotated_frame, [points], isClosed=False, color=(230, 230, 230), thickness=2)
            out_cap.write(annotated_frame)
        else:
            break
    cap.release()
    out_cap.release()
