#!/usr/bin/env python
# -*- coding:utf-8 -*-

import rospy
import numpy as np
from cv_bridge import CvBridge
from sensor_msgs.msg import Image, LaserScan

class HPSensor:

    def __init__(self):

        # video
        self.cam = None
        self.bridge = CvBridge()
        rospy.Subscriber("/camera/usb_cam/image_raw", Image, self.callback_cam)

        # lidar filtered
        self.lidar_filtered = None
        rospy.Subscriber("scan_filtered", LaserScan, self.callback_lidar_filtered)
    
    def callback_cam(self, msg):
        self.cam = self.bridge.imgmsg_to_cv2(msg, "bgr8")

    def callback_lidar_filtered(self, msg):
        self.lidar_filtered = msg
        #print('rm', len(LaserScan.ranges))
        

    def init(self, rate):

        #제대로 연결되지 않으면 실행 X

        while self.cam is None:
             rate.sleep()
        rospy.loginfo("video ready")

        #while self.lidar_filtered is None:
        #    rate.sleep()
        #rospy.loginfo("filtered lidar ready") 