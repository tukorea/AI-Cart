#!/usr/bin/env python3


import rospy
import cv2
from horse_power import HP
import pyrealsense2 as rs

from std_msgs.msg import String
import paho.mqtt.client as mqtt

import json

rospy.init_node('main')
horse_power = HP()

def callback(payload):
	try:
		mqtt_msg = json.loads(payload)
		rospy.loginfo(mqtt_msg)
		top_value = mqtt_msg.get("Top")
		bottom_value = mqtt_msg.get("Bottom")
		color_list = []
		if top_value == 3:
			color_list.append("Bottomlb") # App TopWhite
		elif top_value == 4:
			color_list.append("TopWhite") # App TopBlack
		if bottom_value == 1:
			color_list.append("Bottomlb") # App Bottomlb
		ros_msg = String()
		ros_msg.data = color_list[0]
		pub.publish(ros_msg)
		rospy.loginfo("Published ROS message: %s", ros_msg.data)
	except Exception as e:
		rospy.logwarn("Failed to process MQTT message: %s", str(e))

	rospy.loginfo("Received: %s", payload)

def on_connect(client, userdata, flags, rc):
	rospy.loginfo("Connected with RC: " + str(rc))
	client.subscribe("colorset")

def on_message(client, userdata, msg):
	rospy.loginfo("Topic: %s, Message: %s", msg.topic, str(msg.payload))
	callback(msg.payload)
	recvData = str(msg.payload.decode("utf-8"))
	rospy.loginfo("Received message = %s", recvData)
 
client = mqtt.Client()
client.connect("3.36.243.219", 1883, 60)
client.on_connect = on_connect
client.on_message = on_message
client.loop_start()
pub = rospy.Publisher('ros_color_topic', String, queue_size=15)

if __name__ == '__main__': 
	rospy.loginfo(rospy.get_name() + " started!")  # 노드 네임 출력
	while not rospy.is_shutdown():
		horse_power.control()
		if cv2.waitKey(1) & 0xff == ord('q'): # 주석처리
			break
	cv2.destroyAllWindows()
