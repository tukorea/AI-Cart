package androidclass.android.aicartapp.ui.clothes;


import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;

import androidclass.android.aicartapp.databinding.FragmentClothesBinding;

public class ClothesFragment extends Fragment {

    private FragmentClothesBinding binding;

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        ClothesViewModel clothesViewModel =
                new ViewModelProvider(this).get(ClothesViewModel.class);

        binding = FragmentClothesBinding.inflate(inflater, container, false);
        View root = binding.getRoot();

        final TextView textView = binding.textClothes;
        ClothesViewModel.getText().observe(getViewLifecycleOwner(), textView::setText);
        return root;
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }
}