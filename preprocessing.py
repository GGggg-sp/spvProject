import numpy as np

from utils.Vid2Npcv import Vid2Np
from utils.operations import maybe_mkdir

import argparse
import os
import random
import string
import json


def ProcessLeafDir(dir_path: str, target_resolution: (int, int), target_dir: str, rela_dict: dict):
    # video_list = [vid_name for vid_name in os.listdir(dir_path) if vid_name.endswith('.mp4') or vid_name.endswith('.MP4')
    #               or vid_name.endswith('.wmv') or vid_name.endswith('.mkv') or vid_name.endswith('.mpg') or vid_name.endswith('.rm')
    #               or vid_name.endswith('.avi') or vid_name.endswith('.asf') or vid_name.endswith('.rmvb')]
    video_list = [vid_name for vid_name in os.listdir(dir_path) if
                  vid_name.endswith(('.mp4', '.MP4', '.wmv', '.mkv', '.mpg', '.rm', '.avi', '.asf', '.rmvb'))]
    processed_vid_list = list(rela_dict.values())
    print('{} video files in path: {}\n{} videos has been processed!'.format(len(video_list), dir_path,
                                                                             len(processed_vid_list)))
    for vid_file_name in video_list:
        vid_path = os.path.join(dir_path, vid_file_name)
        if vid_path in processed_vid_list:
            print('{} has been processed, skipped'.format(vid_path))
            continue
        print('Processing {}'.format(vid_path))
        success, np_vid = Vid2Np(vid_path=vid_path, interval=4, resolution=target_resolution)
        if not success:
            print("{} File format error, skipped!".format(vid_path))
            continue
        # npz_file_path = os.path.join(dir_path, vid_file_name.replace('.mp4', '.npy'))
        while True:
            npy_file_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7)) + '.npy'
            if not npy_file_name in rela_dict.keys():
                break
        npy_file_path = os.path.join(target_dir, npy_file_name)
        np.save(npy_file_path, np_vid)
        rela_dict[npy_file_name] = vid_path
        with open(os.path.join(target_dir, 'rela_dict.json'), 'w') as f:
            json.dump(rela_dict, f, indent=4)
    return


def ProcessRootDir(dir_path: str, if_recursive: bool, target_resolution: (int, int), target_dir: str, rela_dict: dict):
    ProcessLeafDir(dir_path=dir_path, target_resolution=target_resolution, target_dir=target_dir, rela_dict=rela_dict)
    if if_recursive:
        dir_list = [dirp for dirp in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, dirp))]
        if len(dir_list) > 0:
            for dirp in dir_list:
                ProcessRootDir(dir_path=os.path.join(dir_path, dirp), if_recursive=True,
                               target_resolution=target_resolution, target_dir=target_dir, rela_dict=rela_dict)


if __name__ == '__main__':
    apser = argparse.ArgumentParser()
    apser.add_argument('videos_dir', help='The directory containing all the videos to be processed')
    apser.add_argument('--width', help='Target image width', default=160)
    apser.add_argument('--height', help='Target image height', default=120)
    apser.add_argument('--target_dir', help='The directory will store the processed dataset', required=True)
    apser.add_argument('--recursive', help='If process the videos in the directory recursively', action='store_true')
    apser.add_argument('--continue_on', help='Continue processing this dataset', action='store_true')
    args = apser.parse_args()

    vid_dir = args.videos_dir
    target_resolution = (int(args.width), int(args.height))
    if_recursive = args.recursive
    target_dir = args.target_dir
    if_continue = args.continue_on

    assert os.path.isdir(vid_dir)
    maybe_mkdir(target_dir)
    rela_dict = {}
    if if_continue and os.path.isfile(os.path.join(target_dir, 'rela_dict.json')):
        print('Loading dataset info, continuing on it: {}'.format(target_dir))
        with open(os.path.join(target_dir, 'rela_dict.json'), 'r') as f:
            rela_dict = json.load(f)

    ProcessRootDir(dir_path=vid_dir, if_recursive=if_recursive, target_resolution=target_resolution,
                   target_dir=target_dir, rela_dict=rela_dict)
    # with open(os.path.join(target_dir, 'rela_dict.json'), 'w') as f:
    #     json.dump(rela_dict, f, indent=4)
