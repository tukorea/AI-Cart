#!/usr/bin/env python
# -*- coding:utf-8 -*-
# import time
import cv2
import numpy as np
import math
import time
import rospy # ROS 라이브러리 "#include <ros.h>"에 해당하는 구문
from ackermann_msgs.msg import AckermannDriveStamped # 패키지의 메시지 파일
from horse_power_sensor import HPSensor
from sensor_msgs.msg import Image, LaserScan

class Camera:
    def __init__(self):
            
            self.rate = rospy.Rate(30)  # 30Hz로 토픽 발행
            self.motor_pub = rospy.Publisher('ackermann_cmd', AckermannDriveStamped, queue_size=30)  # motor msg publisher
            self.motor_msg = AckermannDriveStamped()  # 제어를 위한 속도, 조향각 정보를 담고 있는 xycar_motor 호출
            self.flag = 0 # flag 신호 주기
            self.speed = 5
            self.steering_angle = 0            
            self.sensor = HPSensor()
            #self.trackers = cv2.legacy.Tracker.Tracker() # KCF tracker 생성
            # self.trackers = cv2.TrackerMOSSE_create()
            self.trackers = cv2.legacy_TrackerKCF.create()
            self.tolerance = 30 # 중간점과 간격 차이 얼마나 줄 것인지
            self.roi = (200, 120, 240, 240)
            self.object = None
            #self.Direction = Direction()
            #self.direction = 0

    def selection(self, data): # roi 선택하기
        start_time = time.time()
        while (time.time() - start_time) < 5: # 20초 동안 반복
            for i in range(50):
                
                time_value = time.time() - start_time
                time_value=int(time_value)
 
                data = self.sensor.cam
                cv2.rectangle(data, (200, 120), (440, 360), (0, 255, 255), 2)
                
                # # roi 설정 번호(초)
                cv2.putText(data, "Range: {}".format(5-time_value), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.imshow("Object", data)
                key = cv2.waitKey(1)
                if key == ord('q'):
                    break

        self.roi_select = data
        cv2.destroyAllWindows()
        return self.roi_select

    def Direction(self, direction):
        if direction == "left":
            self.steering_angle = -20
        elif direction =='right':
            self.steering_angle = 20
        elif direction =='up':
            self.speed = 5
        elif direction =='down':
            self.speed = -5
        else :
            self.speed = 5
            
        return self.steering_angle, self.speed
    
    def process(self, data):
        success = self.trackers.init(data, self.roi)
        if self.object is None:
            data = cv2.resize(data, (640, 480))  # 영상 크기 조정
            
            # 파란색 선 그리기
            cv2.line(data, (0, 240), (640, 240), (255, 0, 0), 1)
            cv2.line(data, (320, 0), (320, 480), (255, 0, 0), 1)
            cx, cy = 0, 0

        if self.flag == 0:
                self.selection(data)
                self.flag = 1
                
        if self.trackers is None: #트랙커 생성 안된 경우
            cv2.putText(data, "Press the Space to set ROI!!", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2,cv2.LINE_AA)
        
        else:
            success, self.roi = self.trackers.update(data) # 객체 추적              
            if success: # 추적 성공
                x, y, w, h = map(int, self.roi)
                
                # 객체와 중심점(빨간점) 주위에 사각형 그리기
                # 추적 중심점 표시
                cv2.rectangle(data, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cx, cy = x + w // 2, y + h // 2  # 중심 좌표
                cv2.circle(data, (cx, cy), 5, (0, 0, 255), -1) # 빨간점 그리기
                cv2.putText(data, "Tracking", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
            else:
                cv2.putText(data, "Lost", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                print("Lost")
                self.roi_select = "Lost"
                self.flag == 0
            
            data_center_x, data_center_y = data.shape[1] // 2, data.shape[0] // 2
            dx, dy = cx - data_center_x, cy - data_center_y    

            if abs(dx) < self.tolerance and abs(dy) < self.tolerance:
                self.direction = "go"
                #self.motor_msg.drive.steering_angle = 0
                cv2.putText(data, "go", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                pass

            elif abs(dx) > self.tolerance and abs(dy) < self.tolerance:
                if dx > 0:
                    self.direction = "left"
                    # print("left")
                    # 아두이노에 left 문자열을 전송
                    #self.motor_msg.drive.steering_angle = -20
                    cv2.putText(data, "left", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                else:
                    self.direction = "right"
                    # print("right")
                    # 아두이노에 right 문자열을 전송
                    #self.motor_msg.drive.steering_angle = 20
                    cv2.putText(data, "right", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            
            elif abs(dx) < self.tolerance and abs(dy) > self.tolerance:
                if dy < 0:
                    self.direction = "up"
                    # print("up")
                    # 아두이노에 up 문자열을 전송
                    #self.motor_msg.drive.speed = -5
                    #self.motor_msg.drive.steering_angle = 0                    
                    cv2.putText(data, "up", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                else:
                    self.direction = "down"
                    # print("down")
                    #self.motor_msg.drive.speed = 5
                    #self.motor_msg.drive.steering_angle = 0
                    cv2.putText(data, "down", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            
            else:
                if abs(dx) > abs(dy):
                    if dx > 0:
                        self.direction = "left"
                        # print("left")
                        #self.motor_msg.drive.steering_angle = -20
                        cv2.putText(data, "left", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    else:
                        self.direction = "right"
                        # print("right")
                        #self.motor_msg.drive.steering_angle = 20
                        cv2.putText(data, "right", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                else:
                    if dy > 0:
                        self.direction = "up"
                        # print("up")
                        #self.motor_msg.drive.speed = 5
                        #self.motor_msg.drive.steering_angle = 0  
                        cv2.putText(data, "up", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    else:
                        self.direction = "down"
                        # print("down")
                        #self.motor_msg.drive.speed = -5
                        #self.motor_msg.drive.steering_angle = 0
                        cv2.putText(data, "down", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                        
                # self.motor_pub.publish(self.motor_msg.drive.steering_angle)        
            #self.motor_pub.publish(self.motor_msg.drive.steering_angle)            
            
            # 객체 및 로봇 이동 방향이 포함된 디스플레이 프레임            
            cv2.line(data, (0, data_center_y), (data.shape[1], data_center_y), (255, 0, 0), 1)
            cv2.line(data, (data_center_x, 0), (data_center_x, data.shape[0]), (255, 0, 0), 1)
        
            # 현재 프레임 출력             
            cv2.imshow("Object Tracking", data)
        
            # 'q' 키를 누르면 종료            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()

        # cv2.imshow("Object Tracking2", data)
        
        # Tracker 초기화
        # data : 입력 영상
        # self.roi : 추적 대상 객체가 있는 좌표 
        
        #self.steering_angle, self.speed = Direction(self.direction)

        return self.direction
   
    
    