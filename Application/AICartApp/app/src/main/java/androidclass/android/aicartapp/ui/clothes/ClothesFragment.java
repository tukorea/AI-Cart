package androidclass.android.aicartapp.ui.clothes;


import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;

import androidclass.android.aicartapp.R;
import androidclass.android.aicartapp.databinding.FragmentClothesBinding;

public class ClothesFragment extends Fragment{

    private ImageView[] Tshirt = new ImageView[6];
    private ImageView[] Bpants = new ImageView[6];
    private TextView T, B;
    private FragmentClothesBinding binding;
    private ClothesViewModel clothesViewModel;

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {

        binding = FragmentClothesBinding.inflate(inflater, container, false);
        clothesViewModel = new ViewModelProvider(this).get(ClothesViewModel.class);
        View root = binding.getRoot();

        Tshirt[0] = (ImageView) root.findViewById(R.id.Tblue);
        Tshirt[1] = (ImageView) root.findViewById(R.id.Tgreen);
        Tshirt[2] = (ImageView) root.findViewById(R.id.Tbeige);
        Tshirt[3] = (ImageView) root.findViewById(R.id.Twhite);
        Tshirt[4] = (ImageView) root.findViewById(R.id.Tblack);
        Tshirt[5] = (ImageView) root.findViewById(R.id.Tgray);

        Bpants[0] = (ImageView) root.findViewById(R.id.Bwhite);
        Bpants[1] = (ImageView) root.findViewById(R.id.Blb);
        Bpants[2] = (ImageView) root.findViewById(R.id.Bmb);
        Bpants[3] = (ImageView) root.findViewById(R.id.Bdb);
        Bpants[4] = (ImageView) root.findViewById(R.id.Bgray);
        Bpants[5] = (ImageView) root.findViewById(R.id.Bblack);

        for (int i = 0; i < Tshirt.length; i++) {
            Tshirt[i].setVisibility(View.GONE);
        }
        Tshirt[3].setVisibility(View.VISIBLE);

        for (int i = 1; i < Tshirt.length; i++) {
            Bpants[i].setVisibility(View.GONE);
        }
        Bpants[0].setVisibility(View.VISIBLE);

        T = (TextView) root.findViewById(R.id.T);
        B = (TextView) root.findViewById(R.id.B);

        return root;
    }


    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }

    public void onViewCreated(@NonNull View view, Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        clothesViewModel = new ViewModelProvider(requireActivity()).get(ClothesViewModel.class);
        observeViewModel();
    }

    private void observeViewModel() {
        clothesViewModel.getTshirtIndex().observe(getViewLifecycleOwner(), index -> {
            for (int i = 0; i < Tshirt.length; i++) {
                if (i == index) {
                    Tshirt[i].setVisibility(View.VISIBLE);
                } else {
                    Tshirt[i].setVisibility(View.GONE);
                }
            }
        });

        clothesViewModel.getBpantsIndex().observe(getViewLifecycleOwner(), index -> {
            for (int i = 0; i < Bpants.length; i++) {
                if (i == index) {
                    Bpants[i].setVisibility(View.VISIBLE);
                } else {
                    Bpants[i].setVisibility(View.GONE);
                }
            }
        });
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
        clothesViewModel.setTshirtIndex(index);
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
        clothesViewModel.setBpantsIndex(index);
    }
}