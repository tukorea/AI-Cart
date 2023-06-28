#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


def callback(data):
    bridge = CvBridge()
    try:
        cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
        print(e)

    # 이미지를 화면에 표시
    cv2.imshow("Shared Images", cv_image)
    cv2.waitKey(1)


def main():
    rospy.init_node('image_subscriber')
    rospy.Subscriber("image_topic", Image, callback)

    # Spin until rospy is shutdown
    rospy.spin()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()