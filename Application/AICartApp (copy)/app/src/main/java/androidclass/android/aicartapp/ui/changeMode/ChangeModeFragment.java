package androidclass.android.aicartapp.ui.changeMode;

import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;
import androidx.lifecycle.ViewModelProvider;

import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.navigation.NavController;
import androidx.navigation.Navigation;

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
import androidclass.android.aicartapp.ui.clothes.ClothesFragment;
import androidclass.android.aicartapp.ui.clothes.ClothesViewModel;
import androidclass.android.aicartapp.ui.joystick.JoyStickFragment;

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
        // Navigation Component를 사용하여 화면 전환
        NavController navController = Navigation.findNavController(requireActivity(), R.id.nav_host_fragment_content_main);

        // 네비게이션 상태를 업데이트하여 화면 전환 반영
        NavigationView navigationView = requireActivity().findViewById(R.id.nav_view);
        Menu menu = navigationView.getMenu();
        MenuItem menuItem;
        switch(view.getId()) {
            case R.id.mode_robot:
                mode_id = 0;
                disableNavigationBarItem(1); // mode_id가 0일 때 item 1(joystick)을 disable
                // Navigation Component를 사용하여 화면 전환
                navController.navigate(R.id.nav_clothes);

                // 네비게이션 상태를 업데이트하여 화면 전환 반영
                menuItem = menu.findItem(R.id.nav_clothes);
                menuItem.setChecked(true);
                break;
            case R.id.mode_joystick:
                mode_id = 1;
                disableNavigationBarItem(2); // mode_id가 1일 때 item 2(clothes)를 disable
                // Navigation Component를 사용하여 화면 전환
                navController.navigate(R.id.nav_joystick);

                // 네비게이션 상태를 업데이트하여 화면 전환 반영
                menuItem = menu.findItem(R.id.nav_joystick);
                menuItem.setChecked(true);
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