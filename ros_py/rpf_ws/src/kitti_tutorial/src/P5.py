#!/usr/bin/env python

from kitti_util import *
from data_utils import *
from publish_utils import *
# import cv2
import os
import rospy
from std_msgs.msg import Header
from cv_bridge import CvBridge
import numpy as np
# import sys
# sys.path.remove('/opt/ros/melodic/lib/python2.7/dist-packages')
#
from sensor_msgs.msg import Image , PointCloud2 ,Imu ,NavSatFix

#import     shu ju ge shi
import sensor_msgs.point_cloud2 as pcl2
DATA_PATH = '/home/rpf/data/kitti/RawData/2011_09_26/2011_09_26_drive_0005_sync'


def compute_3d_cam2(h,w,l,x,y,z,yaw):
    R = np.array([[np.cos(yaw),0,np.sin(yaw)],[0,1,0],[-np.sin(yaw),0,np.cos(yaw)]])
    x_corners = [l/2,l/2,-l/2,-l/2,l/2,l/2,-l/2,-l/2]
    y_corners = [0,0,0,0,-h,-h,-h,-h]
    z_corners = [w/2,-w/2,-w/2,w/2,w/2,-w/2,-w/2,w/2]
    corners_3d_cam2 = np.dot(R,np.vstack([x_corners,y_corners,z_corners]))
    corners_3d_cam2 += np.vstack([x,y,z])
    return corners_3d_cam2

if __name__ =="__main__":
    frame = 0
    # jian li node      anonymous shi ni ming de yi si
    rospy.init_node('kitti_node',anonymous= True)
    # chuang jian publisher  1.fa bu topic ming cheng 2.fa bu xun xi ge shi 3.zui duo bao liu duo shao zi liao
    cam_pub = rospy.Publisher('kitti_cam',Image,queue_size = 10)
    pcl_pub = rospy.Publisher('kitti_pointcloud',PointCloud2,queue_size = 10)
    ego_pub = rospy.Publisher('kitti_ego_car', MarkerArray, queue_size=10)
    # model_pub = rospy.Publisher('kitti_car_model',Marker,queue_size = 10)
    imu_pub = rospy.Publisher('kitti_imu',Imu,queue_size = 10)
    gps_pub = rospy.Publisher('kitti_gps',NavSatFix,queue_size = 10)
    box3d_pub = rospy.Publisher('kitti_3d',MarkerArray,queue_size = 10)

    bridge = CvBridge()
    # 1s 10 ci geng xin
    rate = rospy.Rate(10)
    df_tracking = read_tracking('/home/rpf/data/kitti/training/label_02/0000.txt')
    calib = Calibration('/home/rpf/data/kitti/RawData/2011_09_26/', from_video=True)

    while not rospy.is_shutdown():
        # img = cv2.imread(os.path.join(DATA_PATH,'image_02/data/%010d.png'%frame))
        df_tracking_frame = df_tracking[df_tracking.frame==frame]
        boxes = np.array(df_tracking_frame[['bbox_left', 'bbox_top', 'bbox_right', 'bbox_bottom']])
            # boxes = np.array(df[df.frame == frame][['bbox_left', 'bbox_top', 'bbox_right', 'bbox_bottom']])
        types = np.array(df_tracking_frame['type'])
        tracking_ids = np.array(df_tracking_frame['track_id'])

        # types = np.array(df[df.frame == frame]['type'])
        image = read_camera(os.path.join(DATA_PATH,'image_02/data/%010d.png'%frame))
        # point_cloud = np.fromfile(os.path.join(DATA_PATH,'velodyne_points/data/%010d.bin'%frame),dtype = np.float32).reshape(-1,4)
        point_cloud = read_point_cloud(os.path.join(DATA_PATH,'velodyne_points/data/%010d.bin'%frame))
        boxes_3d = np.array(df_tracking_frame[['height','width','length','pos_x','pos_y','pos_z','rot_y']])

        corners_3d_velos=[]
        for box_3d in boxes_3d:
            corners_3d_cam2 = compute_3d_cam2(*box_3d)
            # corners_3d_cam2 = compute_3d_cam2(box_3d[0],box_3d[1],box_3d[2],box_3d[3],box_3d[4],box_3d[5],box_3d[6])
            corners_3d_velo = calib.project_rect_to_velo(corners_3d_cam2.T)
            corners_3d_velos +=[corners_3d_velo]



        # cv2.imshow('img',img)
        # cv2.waitkey(0)
        # cv2.destroyAllWindows()
        # img = np.array(img)
        # sys.path.remove('/opt/ros/melodic/lib/python2.7/dist-packages')

        # cam_pub.publish(bridge.cv2_to_imgmsg(img))


        


        publish_camera(cam_pub,bridge,image,boxes,types)
        publish_3dbox(box3d_pub,corners_3d_velos,tracking_ids)

        # header = Header()
        # header.stamp = rospy.Time.now()
        # header.frame_id = 'map'
        # pcl_pub.publish(pcl2.create_cloud_xyz32(header,point_cloud[:,:3]))

        publish_point_cloud(pcl_pub , point_cloud)

        publish_ego_car(ego_pub)
        # publish_car_model(model_pub)
        imu_data = read_imu_data(os.path.join(DATA_PATH,'oxts/data/%010d.txt'%frame))
        publish_imu(imu_pub,imu_data)
        publish_gps(gps_pub, imu_data)


        rospy.loginfo('publish')
        rate.sleep()
        frame +=1
        frame %=154
