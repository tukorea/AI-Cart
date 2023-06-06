package com.example.mqtttest;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

public class MainActivity extends AppCompatActivity {
    private String ServerIP = "tcp://3.36.243.219:1883";
    private String TOPIC = "TopicName";

    private MqttClient mqttClient;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Button button = findViewById(R.id.button_send);
        Log.d("MQTTService", "log test");

        try {
            mqttClient = new MqttClient(ServerIP, MqttClient.generateClientId(), null);
            Log.d("MQTTService", "mqtt new");
            mqttClient.connect();
            Log.d("MQTTService", "mqtt connect");

            button.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    try {
                        mqttClient.publish(TOPIC, new MqttMessage("hello!".getBytes()));
                        Log.d("MQTTService", "mqtt pub");

                    } catch (MqttException e) {
                        e.printStackTrace();
                        Log.d("MQTTService", "pub error");

                    }
                }
            });
            mqttClient.subscribe(TOPIC);
            mqttClient.setCallback(new MqttCallback() {
                @Override
                public void connectionLost(Throwable throwable) {
                    Log.d("MQTTService", "Connection Lost");
                }

                @Override
                public void messageArrived(String s, MqttMessage mqttMessage) throws Exception {
                    Log.d("MQTTService", "Message Arrived : " + mqttMessage.toString());
                }

                @Override
                public void deliveryComplete(IMqttDeliveryToken iMqttDeliveryToken) {
                    Log.d("MQTTService", "Delivery Complete");
                }
            });
        } catch (MqttException e) {
            e.printStackTrace();
            Log.d("MQTTService", "mqtt error");

        }
    }
}