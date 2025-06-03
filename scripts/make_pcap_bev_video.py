import sys
import numpy as np
import cv2 as cv

from ouster.sdk import pcap, client

import config.kitti_config as cnf
import data_process.kitti_bev_utils as bev_utils


def pcap_2_bev(source):
	lut = client.XYZLut(source.metadata)
	bevs = []
	for scan in source:
		xyz = lut(scan.field(client.ChanField.RANGE))
		sig = scan.field(client.ChanField.SIGNAL)
		sig = cv.normalize(sig, None, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)
		xyz = np.concatenate((xyz, sig[..., np.newaxis]), axis=-1)
		xyz = bev_utils.removePoints(xyz.reshape(-1, 4), cnf.boundary)
		bev = bev_utils.makeBVFeature(xyz, cnf.DISCRETIZATION, cnf.boundary).transpose(1, 2, 0)
		bev = cv.flip((bev * 255).astype(np.uint8), -1)
		bevs.append(bev)
	return bevs


if __name__ == '__main__':
	source = pcap.PcapScanSource(sys.argv[1]).single_source(0)
	vid_writer = cv.VideoWriter(f'{sys.argv[2]}.avi', cv.VideoWriter_fourcc(*'MJPG'), 10, (cnf.BEV_WIDTH, cnf.BEV_HEIGHT))
	for frame in pcap_2_bev(source):
		vid_writer.write(frame)

