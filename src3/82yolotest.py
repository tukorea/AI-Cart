#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import pyrealsense2 as rs

class YoloDetector:
    def __init__(self, weights_path, cfg_path, names_path):
        self.net = cv2.dnn.readNet(weights_path, cfg_path)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        with open(names_path, "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

        self.trackers = cv2.legacy_TrackerKCF.create()
        self.roi = []
        self.tolerance = 30 # 중간점과 간격 차이 얼마나 줄 것인지
        
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
    
    def update_roi(self, boxes):
        self.roi = boxes


def yolo_main():
    pipeline = rs.pipeline()
    config = rs.config()

    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    # Start streaming 
    profile = pipeline.start(config)

    yolo = YoloDetector("/home/tuk/yolo_data/0622/yolov4-chan_final.weights",
                        "/home/tuk/yolo_data/0622/yolov4-chan.cfg",
                        "/home/tuk/yolo_data/obj.names")

    colors = np.random.uniform(0, 255, size=(len(yolo.classes), 3))

    while True:
        frameset = pipeline.wait_for_frames()
        color_frame = frameset.get_color_frame()
        depth_frame = frameset.get_depth_frame()
        if not color_frame or not depth_frame:
            continue

        img = np.asanyarray(color_frame.get_data())
        outs, height, width = yolo.detect(img)
        boxes, class_ids, confidences, x_center, y_center = yolo.process_detections(outs, height, width)
        yolo.update_roi(boxes)
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(yolo.classes[class_ids[i]])
                color = colors[class_ids[i]]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label, (x, y + 30), font, 3, color, 3)

                # Red Circle
                center_x = x_center[i]
                center_y = y_center[i]
                cv2.circle(img, (center_x, center_y), 5, (0, 0, 255), -1)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    pipeline.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    yolo_main()