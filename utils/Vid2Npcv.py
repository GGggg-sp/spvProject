import numpy as np
import cv2


def Vid2Np(vid_path: str, interval: int, resolution: (int, int)):
    cv_vid = cv2.VideoCapture(vid_path)
    vid_frames_count = int(cv_vid.get(cv2.CAP_PROP_FRAME_COUNT))
    vid_frames_rate = cv_vid.get(cv2.CAP_PROP_FPS)
    current_frame_idx = 1
    frame_interval = interval * vid_frames_rate
    vid_np_arr = None
    is_first = True
    while True:
        cv_vid.set(1, current_frame_idx)
        # cv_vid.set(cv2.CAP_PROP_POS_MSEC, current_pos_msec)
        is_success, frame = cv_vid.read()
        if is_success:
            frame = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), resolution)[None, :, :, :]
            if is_first:
                vid_np_arr = frame
                is_first = False
            else:
                if vid_np_arr is None:
                    return False, 0
                vid_np_arr = np.concatenate((vid_np_arr, frame), axis=0)
            current_frame_idx = current_frame_idx + frame_interval
            if current_frame_idx >= vid_frames_count:
                break
        else:
            break
    if vid_np_arr is None:
        return False, 0
    return True, vid_np_arr

if __name__=='__main__':
    vid = Vid2Np(vid_path='test_data/2.wmv', interval=3 , resolution=(320, 240))
    # for idx in range(0, vid.shape[0]):
    #     current_image = Image.fromarray(vid[idx, :, :, :])
    #     current_image.save('image_' + str(idx) + '.jpg')

    np.save('test_data/vid.npy', vid)
