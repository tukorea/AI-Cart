#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import horse_power_sensor as HP
import rospy

# =======================
# parameter
# =======================
class CustomObjectDetector: # 서버에서 받은 클래스 여기에 추가
    
    def __init__(self,class_filepath="/home/tuk/yolo_data/obj.names"):  # 경로 넣어라
        
        self.rate =rospy.Rate(10)
        self.sensor=HP.HPSensor()
        self.sensor.init(self.rate)

        self.img = self.sensor.cam
        self.classes = self.load_classes(class_filepath)
        self.received_class = ["TopBlack", "BottomLightBlue"]
        self.matched_classes = ["TopBlack", "BottomLightBlue"]  # 초기 값 
        ##############################################################
        ## YOLOv4 가중치 및 설정 파일 로드
        ##############################################################
        self.yolo_weights = "/home/tuk/yolo_data/yolov4-custom_best.weights"
        self.yolo_config = "/home/tuk/yolo_data/yolov4-custom.cfg"
        self.yolo_names = "/home/tuk/yolo_data/obj.names"
        # YOLO 모델 초기화
        self.yolo_net = cv2.dnn.readNet(self.yolo_weights, self.yolo_config)
        self.classes = []
        with open(self.yolo_names, "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
         ## Yolo 네트워크 계층 구성 ##
        self.layer_names = self.yolo_net.getLayerNames()
        self.output_layers = [self.layer_names[i[0] - 1] for i in self.yolo_net.getUnconnectedOutLayers()]
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))
        self.roi = (200, 120, 240, 240) # 초기값
        
        self.width = 10
#         self.received_class = None
#         self.matched_classes = []

# """
#         rospy.init_node('class_comparison_node')
#         rospy.Subscriber("input_class_topic", String, self.class_callback)
#         self.drive_pub = rospy.Publisher("ackermann_drive_topic", AckermannDriveStamped, queue_size=10)

# """

    def load_classes(self, path):
        classes = []
        with open(path, 'rt') as f:
            lines = f.read().splitlines()
            for line in lines:
                classes += line.split('\n')
        return classes
    
    
    def class_callback(self, data):
        received_class = data.data
        if received_class in self.classes:
            self.received_class = received_class
            self.matched_classes.append(received_class)  # 리스트에 새로운 요소 추가
     #       self.print_matched_classes()
            
     #  self.matched_classes - 서버에서 받은 클래스랑 매칭해서 맞는 클래스
    
    #def print_matched_class(self):
    #    print(f"Matched class: {self.matched_classes}")

    #    return matched_class
    
                        
       
    def detect_objects(self, data):
        # 입력 이미지를 YOLO 모델에 맞는 형식으로 변환하여 blob 생성
        blob = cv2.dnn.blobFromImage(data, 0.00392, (416, 416), (0,0,0), swapRB=True, crop=False)
        self.yolo_net.setInput(blob)
        outs = self.yolo_net.forward(self.output_layers)  

        # 매칭된 클래스 목록
        #my_detector = CustomObjectDetector()
        #self.matched_classes = my_detector.matched_classes  

        # 객체 검출
        #self.output_layer_names = self.yolo_net.getUnconnectedOutLayers()
          

        # 객체 정보 추출
        boxes = []
        confidences = []
        class_ids = [0,2]

        #객체 검출
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > 0.5:
                    # 객체의 경계 상자 좌표 추출
                    center_x = int(detection[0] * data.shape[1])
                    center_y = int(detection[1] * data.shape[0])
                    self.width = int(detection[2] * data.shape[1])
                    height = int(detection[3] * data.shape[0])
                    left = int(center_x - self.width / 2)
                    top = int(center_y - height / 2)

                    boxes.append([left, top, self.width, height])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
                    
        # 매칭된 클래스와 매칭되는 객체만 필터링
        self.matched_classes = ["TopBlack", "Bottomlb"]  # 초기 값 
        matched_objects = [(self.matched_classes[class_ids], *boxes) for class_ids, boxes in zip(class_ids, boxes)]
        filtered_objects = [(cls, x, y, w, h) for cls, x, y, w, h in matched_objects if cls in self.matched_classes]

        # empty
        print(matched_objects)
        print(filtered_objects)
        
        if len(filtered_objects) != 2:
            return None, None
        elif len(filtered_objects[0]) == 1:
            pass

        # 클래스 좌표 추출
        #top_left_coordinates = self.roi[0:2]
        #bottom_right_coordinates = self.roi[2:4]

        for i, (self.matched_classes, x, y, w, h) in enumerate(filtered_objects):
            # 좌표 정보 추출 코드
            if i == 0:
                top_left_coordinates = (x, y)
            elif i == 1:
                bottom_right_coordinates = (x + w, y + h)
                
        if bottom_right_coordinates is None:
            # 사각형 그리기
            width = abs(top_left_coordinates[0] - (top_left_coordinates[0] + w))
            height = abs(top_left_coordinates[1] - (top_left_coordinates[1] + h))
            bottom_right_coordinates = (top_left_coordinates[0] + width, top_left_coordinates[1] + height)

            return top_left_coordinates, bottom_right_coordinates
        else:
            return top_left_coordinates, bottom_right_coordinates

    
