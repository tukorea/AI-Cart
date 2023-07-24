package androidclass.android.aicartapp.ui.joystick;

import androidx.lifecycle.ViewModelProvider;

import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import com.google.gson.JsonObject;
import com.zerokol.views.joystickView.JoystickView;

import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import androidclass.android.aicartapp.R;
import androidclass.android.aicartapp.databinding.FragmentChangeModeBinding;
import androidclass.android.aicartapp.databinding.FragmentJoyStickBinding;
import androidclass.android.aicartapp.ui.changeMode.ChangeModeViewModel;

public class JoyStickFragment extends Fragment {

    private TextView angleTextView;
    private TextView powerTextView;
    private TextView directionTextView;
    // Importing also other views
    private JoystickView joystick;

    String Angle = "";
    String Power = "";

    String Direction = "";

    //MqttAndroidClient client;

    private FragmentJoyStickBinding binding;
    private JoyStickViewModel joystickViewModel;

    private String pub_joy = "joystick";

    // MQTT
    private static final String MQTTHOST = "tcp://3.36.243.219:1883";
    private static final String USERNAME = "App";
    private static final String PASSWORD = "App_PW";

    private MqttClient mqttClient;

    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {

        binding = FragmentJoyStickBinding.inflate(inflater, container, false);
        joystickViewModel = new ViewModelProvider(this).get(JoyStickViewModel.class);
        View root = binding.getRoot();

        angleTextView = (TextView) root.findViewById(R.id.angleTextView);
        powerTextView = (TextView) root.findViewById(R.id.powerTextView);
        directionTextView = (TextView) root.findViewById(R.id.directionTextView);
        //Referencing also other views
        joystick = (JoystickView) root.findViewById(R.id.joystickView);

        try {
            mqttClient = new MqttClient(MQTTHOST, MqttClient.generateClientId(), null);
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
                            directionTextView.setText(R.string.left_front_lab);
                            break;
                        case JoystickView.RIGHT:
                            directionTextView.setText(R.string.left_lab);
                            break;
                        case JoystickView.RIGHT_BOTTOM:
                            directionTextView.setText(R.string.bottom_left_lab);
                            break;
                        case JoystickView.BOTTOM:
                            directionTextView.setText(R.string.bottom_lab);
                            break;
                        case JoystickView.BOTTOM_LEFT:
                            directionTextView.setText(R.string.right_bottom_lab);
                            break;
                        case JoystickView.LEFT:
                            directionTextView.setText(R.string.right_lab);
                            break;
                        case JoystickView.LEFT_FRONT:
                            directionTextView.setText(R.string.front_right_lab);
                            break;
                        default:
                            directionTextView.setText(R.string.center_lab);
                    }

                    Direction = String.valueOf(directionTextView.getText());

                    JsonObject jsonObject = new JsonObject();
                    //jsonObject.addProperty("angle", Angle);
                    //jsonObject.addProperty("power", Power);
                    jsonObject.addProperty("direction", Direction);

                    String jsonString = jsonObject.toString();

                    try {
                        mqttClient.publish(pub_joy, new MqttMessage(jsonString.getBytes()));
                    } catch (MqttException e) {
                        e.printStackTrace();
                    }
                }
            }, JoystickView.DEFAULT_LOOP_INTERVAL);
        } catch (MqttException e) {
            e.printStackTrace();
        }

        return root;
    }


}