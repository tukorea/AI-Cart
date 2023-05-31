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

public class ClothesFragment extends Fragment implements View.OnClickListener{

    private ImageView[] Tshirt = new ImageView[6];
    private ImageView[] Bpants = new ImageView[6];
    private TextView T, B;
    private FragmentClothesBinding binding;
    private ClothesViewModel clothesViewModel;

    private Button btblue, btgreen, btbeige, btwithe, btblack, btgray;
    private Button bbwhite, bblb, bbmb, bbdb, bbgray, bbblack;

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

        T = (TextView) root.findViewById(R.id.T);
        B = (TextView) root.findViewById(R.id.B);

        btblue = (Button) root.findViewById(R.id.BTblue);
        btgreen = (Button) root.findViewById(R.id.BTgreen);
        btbeige = (Button) root.findViewById(R.id.BTbeige);
        btwithe = (Button) root.findViewById(R.id.BTwhite);
        btblack = (Button) root.findViewById(R.id.BTblack);
        btgray = (Button) root.findViewById(R.id.BTgray);

        bbwhite = (Button) root.findViewById(R.id.BBwhite);
        bblb = (Button) root.findViewById(R.id.BBlb);
        bbmb = (Button) root.findViewById(R.id.BBmb);
        bbdb = (Button) root.findViewById(R.id.BBdb);
        bbgray = (Button) root.findViewById(R.id.BBgray);
        bbblack = (Button) root.findViewById(R.id.BBblack);

        btblue.setOnClickListener(this);
        btgreen.setOnClickListener(this);
        btbeige.setOnClickListener(this);
        btwithe.setOnClickListener(this);
        btblack.setOnClickListener(this);
        btgray.setOnClickListener(this);

        bbwhite.setOnClickListener(this);
        bblb.setOnClickListener(this);
        bbmb.setOnClickListener(this);
        bbdb.setOnClickListener(this);
        bbgray.setOnClickListener(this);
        bbblack.setOnClickListener(this);

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

    @Override
    public void onClick(@NonNull View view) {
        int index1 = 0;
        int index2 = 0;
        int torb = 0;
        switch(view.getId()) {
            case R.id.BTblue:
                index1 = 0;
                T.setText("T : Blue");
                torb = 1;
                break;
            case R.id.BTgreen:
                index1 = 1;
                T.setText("T : Green");
                torb = 1;
                break;
            case R.id.BTbeige:
                T.setText("T : Beige");
                index1 = 2;
                torb = 1;
                break;
            case R.id.BTwhite:
                T.setText("T : White");
                index1 = 3;
                torb = 1;
                break;
            case R.id.BTblack:
                T.setText("T : Black");
                index1 = 4;
                torb = 1;
                break;
            case R.id.BTgray:
                T.setText("T : Gray");
                index1 = 5;
                torb = 1;
                break;
        }
        if(torb == 1){
            clothesViewModel.setTshirtIndex(index1);
            return;
        }

        switch(view.getId()) {
            case R.id.BBwhite:
                B.setText("B : White");
                index2 = 0;
                break;
            case R.id.BBlb:
                B.setText("B : Sky Blue");
                index2 = 1;
                break;
            case R.id.BBmb:
                B.setText("B : Medium Blue");
                index2 = 2;
                break;
            case R.id.BBdb:
                B.setText("B : Dark Blue");
                index2 = 3;
                break;
            case R.id.BBgray:
                B.setText("B : Gray");
                index2 = 4;
                break;
            case R.id.BBblack:
                B.setText("B : Black");
                index2 = 5;
                break;
        }
        clothesViewModel.setBpantsIndex(index2);
    }

}