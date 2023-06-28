#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import rospy
from std_msgs.msg import String
import paho.mqtt.client as mqtt

import json

class GetColor:
    def __init__(self):
        # rospy.init_node('mqtt_color_node', anonymous=True)
        self.client = mqtt.Client()
        self.client.connect("3.36.243.219", 1883, 60)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.loop_start()
        self.pub = rospy.Publisher('ros_color_topic', String, queue_size=15)

    def callback(self, payload):
        try:
            mqtt_msg = json.loads(payload)
            rospy.loginfo(mqtt_msg)
            top_value = mqtt_msg.get("Top")
            bottom_value = mqtt_msg.get("Bottom")
            color_list = []
            if top_value == 3:
                color_list.append("TopWhite")
            elif top_value == 4:
                color_list.append("TopBlack")
            if bottom_value == 1:
                color_list.append("Bottomlb")
            color_list_str = ", ".join(color_list)
            ros_msg = String()
            ros_msg.data = color_list_str
            self.pub.publish(ros_msg)
            rospy.loginfo("Published ROS message: %s", ros_msg.data)
        except Exception as e:
            rospy.logwarn("Failed to process MQTT message: %s", str(e))

        rospy.loginfo("Received: %s", payload)

    def on_connect(self, client, userdata, flags, rc):
        rospy.loginfo("Connected with RC: " + str(rc))
        client.subscribe("colorset")

    def on_message(self, client, userdata, msg):
        rospy.loginfo("Topic: %s, Message: %s", msg.topic, str(msg.payload))
        self.callback(msg.payload)
        recvData = str(msg.payload.decode("utf-8"))
        rospy.loginfo("Received message = %s", recvData)
        # 처리할 로직 추가

    def run(self):
        rospy.spin()

#if __name__ == '__main__':
#    node = GetColor()
#    node.run()
