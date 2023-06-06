import paho.mqtt.client as mqtt
topic = "colorset"
server = "3.36.243.219"

def on_connect(client, userdata, flags, rc):
    print("Connected with RC : " + str(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    print("Topic: ", msg.topic + '\nMessage: ' + str(msg.payload))
    recvData = str(msg.payload.decode("utf-8"))
    print("received message =", recvData)

client = mqtt.Client()
print("connect_server")
client.connect(server, 1883, 60)
print("on_connect")
client.on_connect = on_connect
print("on_message")
client.on_message = on_message

client.loop_forever()
