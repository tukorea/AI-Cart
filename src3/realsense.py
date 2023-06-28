import cv2
import numpy as np
import pyrealsense2 as rs

def get_object_distance(depth_frame, x, y):
    return depth_frame.get_distance(x, y)

try:
    pipeline = rs.pipeline()
    config = rs.config()

    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    pipeline.start(config)

    while True:
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        if not depth_frame or not color_frame:
            continue

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Object's center point (x, y)
        object_center_x = 320
        object_center_y = 240

        object_distance = get_object_distance(depth_frame, object_center_x, object_center_y)

        # Draw a circle in the object's center and display distance
        cv2.circle(color_image, (object_center_x, object_center_y), int(10 * (1 / (object_distance + 1e-6))), (0, 255, 0), 2)
        cv2.putText(color_image, f"Distance: {object_distance:.2f} meters", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.namedWindow('RealSense', cv2.WINDOW_NORMAL)
        cv2.imshow('RealSense', color_image)
        cv2.waitKey(1)

finally:
    pipeline.stop()
