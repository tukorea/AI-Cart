package androidclass.android.aicartapp.ui.camera;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

public class CameraViewModel extends ViewModel {
    // TODO: Implement the ViewModel

    private MutableLiveData<Integer> view_n;

    public LiveData<Integer> getViewNumIndex() {
        if (view_n == null) {
            view_n = new MutableLiveData<>();
            view_n.setValue(0); // 초기 값 설정
        }
        return view_n;
    }

    public void setViewNumIndex(int index) {
        if (view_n != null) {
            view_n.setValue(index);
        }
    }
}