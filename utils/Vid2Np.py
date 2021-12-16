import ffmpeg
import numpy as np
from PIL import Image
import cv2


def Vid2Np(vid_path: str, interval: int, resolution: (int, int)):
    # Get video information
    probe = ffmpeg.probe(vid_path)
    vid_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    width = int(vid_stream['width'])
    height = int(vid_stream['height'])
    total_frames = int(vid_stream['nb_frames'])

    # Convert video frames to numpy arrays
    vid_input = ffmpeg.input(vid_path)
    # out, _ = (
    #     ffmpeg.input(vid_path).output('pipe:', format='rawvideo', pix_fmt='rgb24')
    #     .run(capture_stdout=True)
    # )
    # np_vid = np.frombuffer(out, np.uint8).reshape([-1, height, width, 3])

    # Extract video frames at specific interval
    is_first_frame = True
    frame_idx = 1
    while frame_idx <= total_frames:
        # current_frame = np_vid[frame_idx, :, :, :]
        current_vid_frame_buffer, _ = (vid_input.filter('select', 'gte(n,{})'.format(frame_idx)).output('pipe:', vframes=1, format='image2', vcodec='mjpeg', loglevel="quiet").run(capture_stdout=True))
        current_frame_array = np.asarray(bytearray(current_vid_frame_buffer), dtype='uint8')
        current_frame = cv2.imdecode(current_frame_array, cv2.IMREAD_COLOR)
        current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)
        current_frame = cv2.resize(current_frame, dsize=resolution)[None, :, :, :]

        # current_frame = np.frombuffer(current_vid_frame_buffer, np.uint8).reshape([height, width, 3])
        # current_image = Image.fromarray(current_frame)
        # current_image = current_image.resize(resolution)
        # current_frame = np.asarray(current_image)[None, :, :, :]

        if is_first_frame:
            ext_np_vid = current_frame
            is_first_frame = False
        else:
            ext_np_vid = np.concatenate((ext_np_vid, current_frame), axis=0)
        print("Processing frame: {} ".format(frame_idx))
        frame_idx = frame_idx + interval
        del current_frame
    # Now the ext_np_vid contains all the frames to output
    return ext_np_vid


if __name__=='__main__':
    vid = Vid2Np(vid_path='test_data/testvid1.mp4', interval=150, resolution=(1024, 768))
    # for idx in range(0, vid.shape[0]):
    #     current_image = Image.fromarray(vid[idx, :, :, :])
    #     current_image.save('image_' + str(idx) + '.jpg')

    np.save('test_data/vid.npy', vid)
