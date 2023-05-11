#!/usr/bin/env python

import cv2
import os
import rospy
from std_msgs.msg import Header
from cv_bridge import CvBridge
import numpy as np
import sys
sys.path.remove('/opt/ros/melodic/lib/python2.7/dist-packages')
#
from sensor_msgs.msg import Image , PointCloud2

#import     shu ju ge shi
import sensor_msgs.point_cloud2 as pcl2
DATA_PATH = '/home/rpf/data/kitti/RawData/2011_09_26/2011_09_26_drive_0005_sync'

if __name__ =="__main__":
    frame = 0
    # jian li node      anonymous shi ni ming de yi si
    rospy.init_node('kitti_node',anonymous= True)
    # chuang jian publisher  1.fa bu topic ming cheng 2.fa bu xun xi ge shi 3.zui duo bao liu duo shao zi liao
    cam_pub = rospy.Publisher('kitti_cam',Image,queue_size = 10)
    pcl_pub = rospy.Publisher('kitti_pointcloud',PointCloud2,queue_size = 10)
    bridge = CvBridge()
    # 1s 10 ci geng xin
    rate = rospy.Rate(10)


    while not rospy.is_shutdown():
        img = cv2.imread(os.path.join(DATA_PATH,'image_02/data/%010d.png'%frame))
        point_cloud = np.fromfile(os.path.join(DATA_PATH,'velodyne_points/data/%010d.bin'%frame),dtype = np.float32).reshape(-1,4)
        # cv2.imshow('img',img)
        # cv2.waitkey(0)
        # cv2.destroyAllWindows()
        # img = np.array(img)
        # sys.path.remove('/opt/ros/melodic/lib/python2.7/dist-packages')

        cam_pub.publish(bridge.cv2_to_imgmsg(img))

        header = Header()
        header.stamp = rospy.Time.now()
        header.frame_id = 'map'
        pcl_pub.publish(pcl2.create_cloud_xyz32(header,point_cloud[:,:3]))
        rospy.loginfo('published')
        rate.sleep()
        frame +=1
        frame %=154
