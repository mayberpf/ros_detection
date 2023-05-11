#!/usr/bin/env python


from data_utils import *
from publish_utils import *
import cv2
import os
import rospy
from std_msgs.msg import Header
from cv_bridge import CvBridge
import numpy as np
from sensor_msgs.msg import Image 

DATA_PATH = '/home/rpf/data/kitti/RawData/2011_09_26/2011_09_26_drive_0005_sync'
if __name__ =="__main__":
    frame = 0

    rospy.init_node('kitti_node',anonymous= True)

    cam_pub = rospy.Publisher('kitti_cam',Image,queue_size = 10)

    bridge = CvBridge()

    rate = rospy.Rate(10)

    df_tracking = read_tracking('/home/rpf/data/kitti/training/label_02/0000.txt')

    while not rospy.is_shutdown():

	df_tracking_frame = df_tracking[df_tracking.frame==frame]

	boxes = np.array(df_tracking_frame[['bbox_left', 'bbox_top', 'bbox_right', 'bbox_bottom']])

	types = np.array(df_tracking_frame['type'])


        image = read_camera(os.path.join(DATA_PATH,'image_02/data/%010d.png'%frame))

        publish_camera(cam_pub,bridge,image,boxes,types)

        rospy.loginfo('published')
        rate.sleep()
        frame +=1
	frame %=154
