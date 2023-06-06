package androidclass.android.aicartapp.ui.changeMode;

import androidx.lifecycle.ViewModelProvider;

import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageButton;

import com.google.android.material.bottomnavigation.BottomNavigationView;
import com.google.android.material.navigation.NavigationView;

import androidclass.android.aicartapp.MainActivity;
import androidclass.android.aicartapp.R;
import androidclass.android.aicartapp.databinding.FragmentChangeModeBinding;
import androidclass.android.aicartapp.databinding.FragmentClothesBinding;
import androidclass.android.aicartapp.ui.clothes.ClothesViewModel;

public class ChangeModeFragment extends Fragment implements View.OnClickListener{

    ImageButton mode_robot, mode_joystick;
    
    public int mode_id;
    private FragmentChangeModeBinding binding;
    private ChangeModeViewModel changemodeViewModel;

    @Override
    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {

        binding = FragmentChangeModeBinding.inflate(inflater, container, false);
        changemodeViewModel = new ViewModelProvider(this).get(ChangeModeViewModel.class);
        View root = binding.getRoot();

        mode_robot = (ImageButton) root.findViewById(R.id.mode_robot);
        mode_joystick = (ImageButton) root.findViewById(R.id.mode_joystick);

        mode_robot.setOnClickListener(this);
        mode_joystick.setOnClickListener(this);



        return root;
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }

    @Override
    public void onClick(@NonNull View view) {
        switch(view.getId()) {
            case R.id.mode_robot:
                mode_id = 0;
                disableNavigationBarItem(1); // mode_id가 0일 때 item 1(joystick)을 disable
                break;
            case R.id.mode_joystick:
                mode_id = 1;
                disableNavigationBarItem(2); // mode_id가 1일 때 item 2(clothes)를 disable
                break;
        }
    }

    private void disableNavigationBarItem(int itemIndex) {
        MainActivity mainActivity = (MainActivity) getActivity();
        NavigationView navigationView = mainActivity.findViewById(R.id.nav_view);
        Menu menu = navigationView.getMenu();

        for (int i = 0; i < menu.size(); i++) {
            menu.getItem(i).setEnabled(true);
        }

        MenuItem menuItem = menu.getItem(itemIndex);
        menuItem.setEnabled(false);
    }

}