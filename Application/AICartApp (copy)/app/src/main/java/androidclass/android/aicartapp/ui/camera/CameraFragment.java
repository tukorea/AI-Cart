package androidclass.android.aicartapp.ui.camera;

import androidx.lifecycle.ViewModel;
import androidx.lifecycle.ViewModelProvider;

import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.TextView;

import org.eclipse.paho.client.mqttv3.MqttException;

import androidclass.android.aicartapp.R;
import androidclass.android.aicartapp.databinding.FragmentCameraBinding;
import androidclass.android.aicartapp.ui.clothes.ClothesViewModel;

public class CameraFragment extends Fragment {

    private FragmentCameraBinding binding;
    private CameraViewModel cameraViewModel;

    private TextView view_text;
    private Button[] b_img = new Button[3];
    private WebView[] img_view = new WebView[3];

    int index = 0;

    private String[] img_url = {"/image4", "/image", "/tracking"};

    private static final String StreamHOST = "http://3.36.243.219:5000";

    public static CameraFragment newInstance() {
        return new CameraFragment();
    }

    @Override
    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        binding = FragmentCameraBinding.inflate(inflater, container, false);
        cameraViewModel = new ViewModelProvider(this).get(CameraViewModel.class);
        View root = binding.getRoot();

        view_text = (TextView) root.findViewById(R.id.view_text);

        b_img[0] = (Button) root.findViewById(R.id.b_image4);
        b_img[1] = (Button) root.findViewById(R.id.b_image);
        b_img[2] = (Button) root.findViewById(R.id.b_tracking);

        img_view[0] = (WebView) root.findViewById(R.id.image4_view);
        img_view[1] = (WebView) root.findViewById(R.id.image_view);
        img_view[2] = (WebView) root.findViewById(R.id.tracking_view);


        for (int i = 0; i < img_view.length; i++) {
            img_view[i].setWebViewClient(new WebViewClient());
            img_view[i].setWebChromeClient(new WebChromeClient());
            img_view[i].getSettings().setLoadWithOverviewMode(true);
            img_view[i].getSettings().setUseWideViewPort(true);
            img_view[i].loadUrl(StreamHOST+img_url[i]);
        }

        for (int i = 0; i < b_img.length; i++){
            int finalI = i;
            b_img[i].setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    index = finalI;
                    view_text.setText(img_url[index]);
                    cameraViewModel.setViewNumIndex(index);
                }
            });
        }

        return root;
    }


    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }

    public void onViewCreated(@NonNull View view, Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        cameraViewModel = new ViewModelProvider(requireActivity()).get(CameraViewModel.class);
        observeViewModel();
    }

    private void observeViewModel() {
        cameraViewModel.getViewNumIndex().observe(getViewLifecycleOwner(), index -> {
            for (int i = 0; i < img_view.length; i++) {
                if (i == index) {
                    img_view[i].loadUrl(StreamHOST+img_url[i]);
                    img_view[i].setVisibility(View.VISIBLE);
                } else {
                    img_view[i].setVisibility(View.GONE);
                }
            }
        });

    }

}