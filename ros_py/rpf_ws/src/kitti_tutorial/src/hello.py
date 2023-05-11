#!/usr/bin/env python

import rospy
#
from std_msgs.msg import String
#import     shu ju ge shi
if __name__ =="__main__":
    # jian li node      anonymous shi ni ming de yi si
    rospy.init_node('talker',anonymous= True)
    # chuang jian publisher  1.fa bu topic ming cheng 2.fa bu xun xi ge shi 3.zui duo bao liu duo shao zi liao
    pub = rospy.Publisher('chat',String,queue_size = 10)
    # 1s 10 ci geng xin
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        hello = 'hello world ! %s' % rospy.get_time()
        pub.publish(hello)
        rospy.loginfo(hello)
        rate.sleep()