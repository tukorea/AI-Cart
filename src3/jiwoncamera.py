#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import cv2
import numpy as np
import math
import time
from cv_bridge import CvBridge
import rospy
from ackermann_msgs.msg import AckermannDriveStamped # 패키지의 메시지 파일
from horse_power_sensor import HPSensor
from sensor_msgs.msg import Image, LaserScan
from std_msgs.msg import String
import pyrealsense2 as rs
from yolotest import YoloDetector

# video Transmissin 
# pub = rospy.Publisher('image_topic', Image, queue_size=10)
bridge = CvBridge()
    
class Camera:
    def __init__(self):
            # self.pipeline = rs.pipeline()
            # config = rs.config()

            # config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
            # config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
            
            # # Start streaming
            # self.pipeline.start(config)

            weights_path = "/home/tuk/yolo_data/0622/yolov4-chan_final.weights"
            cfg_path = "/home/tuk/yolo_data/0622/yolov4-chan.cfg"
            names_path = "/home/tuk/yolo_data/obj.names"
            self.rate = rospy.Rate(30)  # 30Hz로 토픽 발행
            self.motor_pub = rospy.Publisher('ackermann_cmd', AckermannDriveStamped, queue_size=30)  # motor msg publisher
            self.color_sub = rospy.Subscriber('ros_color_topic', String, queue_size=15) # color msg subscriber
            self.motor_msg = AckermannDriveStamped()  # 제어를 위한 속도, 조향각 정보를 담고 있는 xycar_motor 호출
            self.flag = 0 # flag 신호 주기
            self.speed = 5
            self.steering_angle = 0            
            self.sensor = HPSensor()
            self.net = cv2.dnn.readNet(weights_path, cfg_path)
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
            with open(names_path, "r") as f:
                self.classes = [line.strip() for line in f.readlines()]
            self.layer_names = self.net.getLayerNames()
            self.output_layers = [self.layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
            self.trackers = cv2.legacy_TrackerKCF.create()
            self.tolerance = 30 # 중간점과 간격 차이 얼마나 줄 것인지
            self.roi = []
            self.object = None
       
            #self.Direction = Direction()
            #self.direction = 0
#YOLOv4
# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
    def detect(self, img):
        height, width = img.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(img, (416, 416)), 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)
        return outs, height, width

    def process_detections(self, outs, height, width, confidence_threshold=0.8):
        class_ids = []
        confidences = []
        boxes = []
        x_center = []
        y_center = []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > confidence_threshold:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # 좌표
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])

                    # 중앙좌표 
                    center_x = int(center_x)
                    center_y = int(center_y)
                    x_center.append(center_x)
                    y_center.append(center_y)

                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        return boxes, class_ids, confidences, x_center, y_center
    # ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
    
    def update_roi(self, boxes):
        self.roi = boxes
        
    def Direction(self, direction):
        if direction == "left":
            self.steering_angle = -20
            # self.speed = 5
        elif direction =='right':
            self.steering_angle = 20
            # self.speed = 5
        elif direction =='up':
            self.steering_angle = 0
            # self.speed = 5
        elif direction =='down':
            self.steering_angle = 0
            # self.speed = -5
        # else :
        #     self.speed = 5
        return self.steering_angle
        # return self.steering_angle, self.speed
    
    
    def process(self, pipeline):
        # pipeline = rs.pipeline()
        # config = rs.config()

        # config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        # config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        
        # # Start streaming
        # pipeline.start(config)

        yolo = YoloDetector("/home/tuk/yolo_data/0622/yolov4-chan_final.weights",
                            "/home/tuk/yolo_data/0622/yolov4-chan.cfg",
                            "/home/tuk/yolo_data/obj.names")

        colors = np.random.uniform(0, 255, size=(len(yolo.classes), 3))

        # Capture a single frame
        frameset = pipeline.wait_for_frames()
        color_frame = frameset.get_color_frame()
        depth_frame = frameset.get_depth_frame()

        if not color_frame or not depth_frame:
            print("Error capturing frame")
            return []
        
        img = np.asanyarray(color_frame.get_data())
        outs, height, width = yolo.detect(img)
        boxes, class_ids, confidences, x_center, y_center = yolo.process_detections(outs, height, width)
        self.roi = yolo.update_roi(boxes)
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        
        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(yolo.classes[class_ids[i]])
                color = colors[class_ids[i]]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label, (x, y + 30), font, 3, color, 3)
                
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
                cv2.putText(data, "go", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                pass

            elif abs(dx) > self.tolerance and abs(dy) < self.tolerance:
                if dx > 0:
                    self.direction = "left"
                    cv2.putText(data, "left", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                else:
                    self.direction = "right"
                    cv2.putText(data, "right", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            
            elif abs(dx) < self.tolerance and abs(dy) > self.tolerance:
                if dy < 0:
                    self.direction = "up"                  
                    cv2.putText(data, "up", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                else:
                    self.direction = "down"
                    cv2.putText(data, "down", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            
            else:
                if abs(dx) > abs(dy):
                    if dx > 0:
                        self.direction = "left"
                        cv2.putText(data, "left", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    else:
                        self.direction = "right"
                        cv2.putText(data, "right", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                else:
                    if dy > 0:
                        self.direction = "up"
                        cv2.putText(data, "up", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    else:
                        self.direction = "down"
                        cv2.putText(data, "down", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                        
                # self.motor_pub.publish(self.motor_msg.drive.steering_angle)        
            #self.motor_pub.publish(self.motor_msg.drive.steering_angle)            
            
            # 객체 및 로봇 이동 방향이 포함된 디스플레이 프레임            
            cv2.line(data, (0, data_center_y), (data.shape[1], data_center_y), (255, 0, 0), 1)
            cv2.line(data, (data_center_x, 0), (data_center_x, data.shape[0]), (255, 0, 0), 1)
        
            # 현재 프레임 출력             
            cv2.imshow("Object Tracking", data)
            
            # OpenCV 영상을 ROS 메시지로 변환하여 게시
            # pub.publish(bridge.cv2_to_imgmsg(data, "bgr8"))
            
            # 'q' 키를 누르면 종료            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                pipeline.stop()

        # cv2.imshow("Object Tracking2", data)
        
        # Tracker 초기화
        # data : 입력 영상
        # self.roi : 추적 대상 객체가 있는 좌표 
        
        #self.steering_angle, self.speed = Direction(self.direction)

        return self.direction
    
