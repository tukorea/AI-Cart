#!/usr/bin/env python3
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
        
        #depth information
        #/camera/depth/image_rect_raw 
        #format : index
        

        
        # realsense video
        # self.realsense_cam = None
        # self.bridge = CvBridge()
        # rospy.Subscriber("/camera/color/image_raw", Image, self.callback_realsense_cam)
        
        # lidar filtered
        self.lidar_filtered = None
        rospy.Subscriber("scan_filtered", LaserScan, self.callback_lidar_filtered)
        #rospy.Subscriber('laser_scan', LaserScan, self.callback)
    
    def callback_cam(self, msg):
        self.cam = self.bridge.imgmsg_to_cv2(msg, "bgr8")

    def callback_realsense_cam(self, msg):
        self.realsense_cam = self.bridge.imgmsg_to_cv2(msg, "passthrough")
        
    def callback_lidar_filtered(self, msg):
        self.lidar_filtered = msg
        #print('rm', len(LaserScan.ranges))

        # rospy.loginfo("LIDAR data received.") # jw
        
    ## jw ##
    
    # def process(self, msg, img):
    #     if msg is not None:
    #         coordinate = self.coordinate_transform(msg.ranges)
            
    #         processed_data = self.value_handling(coordinate)
            
    #         centroid_list = self.clustering(processed_data)

    #         self.rp.main(msg, img)
    #         self.steering_angle = self.avoidance(centroid_list)
            
                
    #         return self.steering_angle #, self.flag
    #     else:
    #         rospy.loginfo("No LIDAR data received.")
    
    ## jw ##
    
    # def callback(self, data):
    #     self.process(data)
        
    ## jw ##  
        
    # def init(self, rate):
    #     while self.cam is None or self.lidar_filtered is None:
    #         rate.sleep()

    #     rospy.loginfo("Sensor data ready")
        

    def init(self, rate):

        #제대로 연결되지 않으면 실행 X

        while self.cam is None:
            rate.sleep()
        rospy.loginfo("video ready")

        while self.lidar_filtered is None:
            rate.sleep()
        rospy.loginfo("filtered lidar ready") 