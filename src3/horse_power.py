#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import cv2
import rospy
from ackermann_msgs.msg import AckermannDriveStamped
from time import time
from horse_power_sensor import HPSensor

from controller import PID
from obstacle_detector import Clustering #장애물 확인
from camera import Camera
#from camera import Camera #객체 따라가기

from cv_bridge import CvBridge
import pyrealsense2 as rs
import numpy as np

bridge = CvBridge()

# pipeline = rs.pipeline()

# config = rs.config()

# config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
# config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    
# Start streaming
# pipeline.start(config)
    
class HP:
    def __init__(self):
        self.obstacle_detector = Clustering()
        self.rate = rospy.Rate(20)  # 20Hz로 토픽 발행
        self.motor_pub = rospy.Publisher('ackermann_cmd', AckermannDriveStamped, queue_size=20)
        self.motor_msg = AckermannDriveStamped()  # 제어를 위한 속도, 조향각 정보를 담고 있는 ackermann_cmd 호출
        self.sensor = HPSensor()
        self.sensor.init(self.rate)
        

        self.camera = Camera()
        #self.stanley = Stanley()
        self.start_time = time()
        self.speed = 0
        self.steering_angle = 0

    # def calc_speed(self, angle):  # 최저속도(min): 10.0, 최고속도: 50.0(50.0)
    #     if angle > 0:
    #         slope = -0.8

    #     elif angle < 0:
    #         slope = 0.8

    #     else:
    #         slope = 0.0

    #     speed = (slope * angle) + 50.0

    #     return speefloat(speed)



    def control(self):

        # if time() - self.start_time <= 1.0:
        #     self.motor_msg.drive.speed = 5
        #     self.motor_msg.drive.steering_angle = 0

        try:
            #print('hello\n')
            # frames = pipeline.wait_for_frames(timeout_ms=100000)
            
            # color_frame = frames.get_color_frame()
            # color_image = np.asanyarray(color_frame.get_data())
            
            steering_angle = self.obstacle_detector.process(self.sensor.lidar_filtered, self.sensor.cam)
            print('done object detecting')
            # cv2.imshow("fake_video", self.sensor.cam) # 앱에서 출력 안하면 돼
            direction= self.camera.process(self.sensor.cam)
            print('done camera processing')
            print("\n\n\n\ndetect!!!!\n\n\n\n")
            speed = 0

            #steering_angle = curvature_angle# 모터로 보내는 조향각
            #if flag == 1:
            #    speed = 5
            #    print(steering_angle)
            
            # speed = self.calc_speed(steering_angle)
        except ValueError :
            # cv2.imshow("fake_video", self.sensor.cam) # 앱에서 출력 안하면 돼
            direction = self.camera.process(self.sensor.cam)
            print('done valueerror processing')
            


            #steering_angle = curvature_angle# 모터로 보내는 조향각
            # speed = 0

        # print("Current motor speed: {}, Current motor angle: {}".format(
            # self.motor_msg.drive.speed, self.motor_msg.drive.steering_angle))

            steering_angle, speed = self.camera.Direction(direction)

        self.motor_msg.drive.speed = int(speed)
        self.motor_msg.drive.steering_angle = int(steering_angle)

        self.motor_pub.publish(self.motor_msg)
        self.rate.sleep() 