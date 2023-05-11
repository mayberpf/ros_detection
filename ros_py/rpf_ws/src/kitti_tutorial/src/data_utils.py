#!/usr/bin/env python
#coding:utf-8

import cv2
import numpy as np
import pandas as pd






IMU_COLUMN_NAMES = ['lat','lon','alt','roll','pitch','yaw','vn','ve','vf','vl',
                    'vu','ax','ay','az','af','al','au','wx','wy','wz','wf','wl',
                    'wu','posacc','velacc','navstat','numsats','posmode','velmose','orimode']

TRACKING_NAMES = ['frame', 'track_id', 'type', 'truncated', 'occluded', 'alpha',
                'bbox_left', 'bbox_top',
                'bbox_right', 'bbox_bottom', 'height', 'width', 'length', 'pos_x',
                'pos_y', 'pos_z', 'rot_y']

    #
    # COLUMN_NAMES = {'frame':[1],'track_id':[1],'type':[1],'truncated':[1],'occluded':[1],'alpha':[1],'bbox_left':[1],'bbox_top':[1],
    #                 'bbox_right':[1],'bbox_bottom':[1],'height':[1],'width':[1],'length':[1],'pos_x':[1],'pos_y':[1],'pos_z':[1],'rot_y':[1]}
    #在jupyter notebook zhong zhe yang xie cai neng bao zheng lie de shun xu dui ying shang
def read_camera(path):
    return cv2.imread(path)

def read_point_cloud(path):
    return np.fromfile(path,dtype = np.float32 ).reshape(-1,4)

def read_imu_data(path):
    df = pd.read_csv(path,header=None,sep=' ')
    df.columns = IMU_COLUMN_NAMES
    return df

def read_tracking(path):


    df = pd.read_csv(path, header=None, sep=' ')
    df.columns = TRACKING_NAMES
    df.loc[df.type.isin(['Truck', 'Van', 'Tram']), 'type'] = 'Car'
    df = df[df.type.isin(['Car', 'Pedestrian', 'Cyclist'])]

    return df




