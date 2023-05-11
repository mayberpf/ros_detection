#!/usr/bin/env python


import numpy as np
import rospy
from std_msgs.msg import Header
from sensor_msgs.msg import Image , PointCloud2 , Imu , NavSatFix
import sensor_msgs.point_cloud2 as pcl2
from cv_bridge import CvBridge
from visualization_msgs.msg import Marker , MarkerArray
from geometry_msgs.msg import Point
import tf
import math
import cv2


FRAME_ID = 'map'
bridge = CvBridge()
DETECTION_COLOR_DICT = {'Car': (255, 255, 0), 'Pedestrian':(0, 255, 255), 'Cyclist': (140, 40, 255)}
LIFETIME = 0.1

LINES = [[0,1],[1,2],[2,3],[3,0]]
LINES += [[4,5],[5,6],[6,7],[7,4]]
LINES += [[4,0],[1,5],[6,2],[7,3]]
LINES += [[4,1],[5,0]]

def publish_camera(cam_pub , bridge , image, boxes, types):
    # cv2.rectangle(image, (10,10), (100,100), (0, 0, 255), 2)

    for  box in boxes:

        top_left = int(box[0]), int(box[1])
        bottom_right = int(box[2]), int(box[3])
        cv2.rectangle(image,top_left,bottom_right,(0,0,255),2)

        # cv2.imshow("Image",img)
    cam_pub.publish(bridge.cv2_to_imgmsg(image))
    #"bgr8" is no need!

def publish_point_cloud(pcl_pub , point_cloud):
    header = Header()
    header.stamp = rospy.Time.now()
    header.frame_id  = FRAME_ID
    pcl_pub.publish(pcl2.create_cloud_xyz32(header,point_cloud[:,:3]))


def publish_ego_car(ego_car_pub):

    marker_array = MarkerArray()


    marker = Marker()
    marker.header.frame_id = FRAME_ID
    marker.header.stamp = rospy.Time.now()
    #mei ge marker zhi you yi ge id
    marker.id = 0

    marker.action = Marker.ADD
    #chu xian zai hua mian duo jiu 
    marker.lifetime = rospy.Duration()
    #marker de lei xing
    marker.type = Marker.LINE_STRIP
    #she ding yan se rgb tou ming du  cu du
    marker.color.r = 0.0
    marker.color.g = 1.0
    marker.color.b = 0.0
    marker.color.a = 1.0
    marker.scale.x = 0.2

    marker.points = []
    marker.points.append(Point(10,-10,0))
    marker.points.append(Point(0,0,0))
    marker.points.append(Point(10,10,0))

    marker_array.markers.append(marker)

    mesh_marker = Marker()
    mesh_marker.header.frame_id = FRAME_ID
    mesh_marker.header.stamp = rospy.Time.now()
    #mei ge marker zhi you yi ge id
    mesh_marker.id = -1

    mesh_marker.action = Marker.ADD
    #chu xian zai hua mian duo jiu
    mesh_marker.lifetime = rospy.Duration()
    #marker de lei xing
    mesh_marker.type = Marker.MESH_RESOURCE
    mesh_marker.mesh_resource = 'package://kitti_tutorial/Car-Model/Car-Model/Car.dae'

    mesh_marker.pose.position.x = 0.0
    mesh_marker.pose.position.y = 0.0
    mesh_marker.pose.position.z = -1.5

    q = tf.transformations.quaternion_from_euler(0,0,math.pi/2)
    mesh_marker.pose.orientation.x = q[0]
    mesh_marker.pose.orientation.y = q[1]
    mesh_marker.pose.orientation.z = q[2]
    mesh_marker.pose.orientation.w = q[3]

    #she ding yan se rgb tou ming du  cu du
    mesh_marker.color.r = 1.0
    mesh_marker.color.g = 1.0
    mesh_marker.color.b = 1.0
    mesh_marker.color.a = 1.0

    mesh_marker.scale.x = 0.9
    mesh_marker.scale.y = 0.9
    mesh_marker.scale.z = 0.9

    marker_array.markers.append(mesh_marker)

    ego_car_pub.publish(marker_array)

# def publish_car_model(modle_pub):
#     mesh_marker = Marker()
#     mesh_marker.header.frame_id = FRAME_ID
#     mesh_marker.header.stamp = rospy.Time.now()
#     #mei ge marker zhi you yi ge id
#     mesh_marker.id = -1
#
#     mesh_marker.action = Marker.ADD
#     #chu xian zai hua mian duo jiu
#     mesh_marker.lifetime = rospy.Duration()
#     #marker de lei xing
#     mesh_marker.type = Marker.MESH_RESOURCE
#     mesh_marker.mesh_resource = 'package://kitti_tutorial/Car-Model/Car-Model/Car.dae'
#
#     mesh_marker.pose.position.x = 0.0
#     mesh_marker.pose.position.y = 0.0
#     mesh_marker.pose.position.z = -1.5
#
#     q = tf.transformations.quaternion_from_euler(0,0,math.pi/2)
#     mesh_marker.pose.orientation.x = q[0]
#     mesh_marker.pose.orientation.y = q[1]
#     mesh_marker.pose.orientation.z = q[2]
#     mesh_marker.pose.orientation.w = q[3]
#
#     #she ding yan se rgb tou ming du  cu du
#     mesh_marker.color.r = 1.0
#     mesh_marker.color.g = 1.0
#     mesh_marker.color.b = 1.0
#     mesh_marker.color.a = 1.0
#
#     mesh_marker.scale.x = 0.9
#     mesh_marker.scale.y = 0.9
#     mesh_marker.scale.z = 0.9
#
#
#     modle_pub.publish(mesh_marker)
def publish_imu(imu_pub , imu_data):
    imu = Imu()
    imu.header.frame_id = FRAME_ID
    imu.header.stamp = rospy.Time.now()
    q = tf.transformations.quaternion_from_euler(float(imu_data.roll),float(imu_data.pitch),float(imu_data.yaw))
    imu.orientation.x = q[0]
    imu.orientation.y = q[1]
    imu.orientation.z = q[2]
    imu.orientation.w = q[3]

    imu.linear_acceleration.x = imu_data.af
    imu.linear_acceleration.y = imu_data.al
    imu.linear_acceleration.z = imu_data.au

    imu.angular_velocity.x = imu_data.wf
    imu.angular_velocity.y = imu_data.wl
    imu.angular_velocity.z = imu_data.wu

    imu_pub.publish(imu)


def publish_gps(gps_pub,imu_data):
    gps = NavSatFix()
    gps.header.frame_id = FRAME_ID
    gps.header.stamp = rospy.Time.now()
    gps.latitude = imu_data.lat
    gps.longitude = imu_data.lon
    gps.altitude = imu_data.alt
    gps_pub.publish(gps)

def publish_3dbox(box3d_pub,corners_3d_velos,tracking_ids):

    marker_array = MarkerArray()

    for i ,corners_3d_velo in enumerate(corners_3d_velos):
        marker = Marker()

        marker.header.frame_id = FRAME_ID
        marker.header.stamp = rospy.Time.now()
        marker.id = i
        marker.action = Marker.ADD
        marker.lifetime = rospy.Duration(LIFETIME)
        marker.type = Marker.LINE_LIST


        marker.color.r = 0.0
        marker.color.g = 1.0
        marker.color.b = 0.0

        marker.color.a = 1.0
        marker.scale.x = 0.1


        marker.points = []
        for l in LINES:
            p1 = corners_3d_velo[l[0]]
            marker.points.append(Point(p1[0],p1[1],p1[2]))
            p2 = corners_3d_velo[l[1]]
            marker.points.append(Point(p2[0],p2[1],p2[2]))
        marker_array.markers.append(marker)

        text_marker = Marker()

        text_marker.header.frame_id = FRAME_ID
        text_marker.header.stamp = rospy.Time.now()
        text_marker.id = i+1000
        text_marker.action = Marker.ADD
        text_marker.lifetime = rospy.Duration(LIFETIME)
        text_marker.type = Marker.TEXT_VIEW_FACING

        p4 = corners_3d_velo[4]

        text_marker.pose.position.x = p4[0]
        text_marker.pose.position.y = p4[1]
        text_marker.pose.position.z = p4[2]+0.5

        text_marker.text = str(tracking_ids[i])
        text_marker.color.r = 1.0
        text_marker.color.g = 1.0
        text_marker.color.b = 0.0

        text_marker.color.a = 1.0
        text_marker.scale.x = 1
        text_marker.scale.y = 1
        text_marker.scale.z = 1
        marker_array.markers.append(text_marker)







    

    box3d_pub.publish(marker_array)

