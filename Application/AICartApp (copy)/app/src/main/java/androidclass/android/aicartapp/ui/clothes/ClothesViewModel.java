package androidclass.android.aicartapp.ui.clothes;

import androidx.appcompat.app.AppCompatActivity;
import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

import android.os.Bundle;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

import androidclass.android.aicartapp.R;

public class ClothesViewModel extends ViewModel {
    private MutableLiveData<Integer> tshirtIndex;

    public LiveData<Integer> getTshirtIndex() {
        if (tshirtIndex == null) {
            tshirtIndex = new MutableLiveData<>();
            tshirtIndex.setValue(3); // 초기 값 설정
        }
        return tshirtIndex;
    }

    public void setTshirtIndex(int index) {
        if (tshirtIndex != null) {
            tshirtIndex.setValue(index);
        }
    }
}