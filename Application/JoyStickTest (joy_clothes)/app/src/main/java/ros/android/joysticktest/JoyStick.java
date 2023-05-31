package ros.android.joysticktest;

import static ros.android.joysticktest.R.id.angleTextView;

import android.os.Bundle;
import android.widget.Button;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import com.zerokol.views.joystickView.JoystickView;

import org.eclipse.paho.android.service.MqttAndroidClient;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

public class JoyStick extends AppCompatActivity {
    private TextView angleTextView;
    private TextView powerTextView;
    private TextView directionTextView;
    // Importing also other views
    private JoystickView joystick;

    // mqtt
    static String MQTTHOST = "tcp://3.36.243.219:1883";
    static String USERNAME = "App";
    static String PASSWORD = "App_PW";
    // angle, power pub 변수
    String pubTopic1 = "angle_topic";
    String pubTopic2 = "power_topic";
    String Angle = "";
    String Power = "";

    MqttAndroidClient client;

    // 화면 전환 버튼
    Button Joy, Cloth;

    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.joy_stick_view);

        angleTextView = (TextView) findViewById(R.id.angleTextView);
        powerTextView = (TextView) findViewById(R.id.powerTextView);
        directionTextView = (TextView) findViewById(R.id.directionTextView);
        //Referencing also other views
        joystick = (JoystickView) findViewById(R.id.joystickView);

        Joy = (Button) findViewById(R.id.BJoyStick);
        Cloth = (Button) findViewById(R.id.BClothes);

        try {
            MqttClient mqttClient = new MqttClient(MQTTHOST, MqttClient.generateClientId(), null);
            mqttClient.connect();

            //Event listener that always returns the variation of the angle in degrees, motion power in percentage and direction of movement
            joystick.setOnJoystickMoveListener(new JoystickView.OnJoystickMoveListener() {

                @Override
                public void onValueChanged(int angle, int power, int direction) {
                    // TODO Auto-generated method stub

                    Angle = String.valueOf(angle);
                    Power = String.valueOf(power);

                    angleTextView.setText(" " + Angle + "°");
                    powerTextView.setText(" " + Power + "%");
                    switch (direction) {
                        case JoystickView.FRONT:
                            directionTextView.setText(R.string.front_lab);
                            break;
                        case JoystickView.FRONT_RIGHT:
                            directionTextView.setText(R.string.front_right_lab);
                            break;
                        case JoystickView.RIGHT:
                            directionTextView.setText(R.string.right_lab);
                            break;
                        case JoystickView.RIGHT_BOTTOM:
                            directionTextView.setText(R.string.right_bottom_lab);
                            break;
                        case JoystickView.BOTTOM:
                            directionTextView.setText(R.string.bottom_lab);
                            break;
                        case JoystickView.BOTTOM_LEFT:
                            directionTextView.setText(R.string.bottom_left_lab);
                            break;
                        case JoystickView.LEFT:
                            directionTextView.setText(R.string.left_lab);
                            break;
                        case JoystickView.LEFT_FRONT:
                            directionTextView.setText(R.string.left_front_lab);
                            break;
                        default:
                            directionTextView.setText(R.string.center_lab);
                    }

                    try {
                        mqttClient.publish(pubTopic1, new MqttMessage(Angle.getBytes()));
                        mqttClient.publish(pubTopic2, new MqttMessage(Power.getBytes()));
                    } catch (MqttException e) {
                        e.printStackTrace();
                    }
                }
            }, JoystickView.DEFAULT_LOOP_INTERVAL);
        } catch (MqttException e) {
            e.printStackTrace();
        }


    }
}
