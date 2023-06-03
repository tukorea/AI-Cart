package androidclass.android.aicartapp;

import android.os.Bundle;
import android.view.View;
import android.widget.RelativeLayout;

import androidx.appcompat.app.AppCompatActivity;
import androidx.navigation.ui.AppBarConfiguration;

import androidclass.android.aicartapp.databinding.ActivityLoginBinding;
import androidclass.android.aicartapp.databinding.ActivityMainBinding;

public class LoginActivity extends AppCompatActivity {

    private AppBarConfiguration mAppBarConfiguration;
    private ActivityLoginBinding binding;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        binding = ActivityLoginBinding.inflate(getLayoutInflater());
        View view = binding.getRoot();
        setContentView(view);

        // 초기에는 로그인 레이아웃을 표시
        binding.layoutLogin.getRoot().setVisibility(View.VISIBLE);
        binding.layoutRegister.getRoot().setVisibility(View.GONE);

    }
}
