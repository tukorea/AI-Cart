package androidclass.android.aicartapp;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

public class clothes extends AppCompatActivity {

    ImageView[] Tshirt = new ImageView[6];
    ImageView[] Bpants = new ImageView[6];

    TextView T, B;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.clothes);

        Tshirt[0] = (ImageView) findViewById(R.id.Tblue);
        Tshirt[1] = (ImageView) findViewById(R.id.Tgreen);
        Tshirt[2] = (ImageView) findViewById(R.id.Tbeige);
        Tshirt[3] = (ImageView) findViewById(R.id.Twhite);
        Tshirt[4] = (ImageView) findViewById(R.id.Tblack);
        Tshirt[5] = (ImageView) findViewById(R.id.Tgray);

        Bpants[0] = (ImageView) findViewById(R.id.Bwhite);
        Bpants[1] = (ImageView) findViewById(R.id.Blb);
        Bpants[2] = (ImageView) findViewById(R.id.Bmb);
        Bpants[3] = (ImageView) findViewById(R.id.Bdb);
        Bpants[4] = (ImageView) findViewById(R.id.Bgray);
        Bpants[5] = (ImageView) findViewById(R.id.Bblack);

        for (int i = 0; i < Tshirt.length; i++) {
            Tshirt[i].setVisibility(View.GONE);
        }
        Tshirt[3].setVisibility(View.VISIBLE);

        for (int i = 1; i < Tshirt.length; i++) {
            Bpants[i].setVisibility(View.GONE);
        }
        Bpants[0].setVisibility(View.VISIBLE);

        T = (TextView) findViewById(R.id.T);
        B = (TextView) findViewById(R.id.B);
    }

    public void TClick(View v) {
        int index = 0;
        switch(v.getId()) {
            case R.id.BTblue:
                index = 0;
                T.setText("T : Blue");
                break;
            case R.id.BTgreen:
                index = 1;
                T.setText("T : Green");
                break;
            case R.id.BTbeige:
                T.setText("T : Beige");
                index = 2;
                break;
            case R.id.BTwhite:
                T.setText("T : White");
                index = 3;
                break;
            case R.id.BTblack:
                T.setText("T : Black");
                index = 4;
                break;
            case R.id.BTgray:
                T.setText("T : Gray");
                index = 5;
                break;
        }
        for (int i = 0; i < Tshirt.length; i++) {
            if (i == index) {
                Tshirt[i].setVisibility(View.VISIBLE);
            } else {
                Tshirt[i].setVisibility(View.GONE);
            }
        }
    }

    public void BClick(View v) {
        int index = 0;
        switch(v.getId()) {
            case R.id.BBwhite:
                B.setText("B : White");
                index = 0;
                break;
            case R.id.BBlb:
                B.setText("B : Sky Blue");
                index = 1;
                break;
            case R.id.BBmb:
                B.setText("B : Medium Blue");
                index = 2;
                break;
            case R.id.BBdb:
                B.setText("B : Dark Blue");
                index = 3;
                break;
            case R.id.BBgray:
                B.setText("B : Gray");
                index = 4;
                break;
            case R.id.BBblack:
                B.setText("B : Black");
                index = 5;
                break;
        }
        for (int i = 0; i < Bpants.length; i++) {
            if (i == index) {
                Bpants[i].setVisibility(View.VISIBLE);
            } else {
                Bpants[i].setVisibility(View.GONE);
            }
        }
    }
}