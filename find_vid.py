import numpy as np
import argparse
import os

import json
import cv2
from urllib.request import urlopen
import urllib.request as request

from utils.loss_utils import loss_mae

def find_vid(pic_path:str, dataset_path:str, resolution:(int, int), topN:int = 3, pic_path_is_url:bool = False):
    if pic_path_is_url:
        print("Loading image from url:")
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        req_h = request.Request(url=pic_path, headers=headers)
        req = urlopen(req_h)
        image = np.asarray(bytearray(req.read()), dtype='uint8')
        pic = cv2.imdecode(image, cv2.IMREAD_COLOR)
        print("Image loaded!")
    else:
        pic = cv2.imread(pic_path)

    pic = cv2.resize(pic, resolution)

    json_file_path = os.path.join(dataset_path, 'rela_dict.json')
    with open(json_file_path, 'r') as f:
        rela_dict = json.load(f)
    # max2_ssim = [30000, '']
    similarity_list = []
    for npy_file_name in rela_dict:
        npy_file_path = os.path.join(dataset_path, npy_file_name)
        single_npy_content = np.load(npy_file_path)
        max_ssim_single_npy = 300000
        for i in range(0, single_npy_content.shape[0]):
            frame_ssim = loss_mae(pic, single_npy_content[i, :, :, :])
            if frame_ssim < max_ssim_single_npy:
                max_ssim_single_npy = frame_ssim
        similarity_list.append((npy_file_name, max_ssim_single_npy))
        # if max_ssim_single_npy < max2_ssim[0]:
        #     max2_ssim[0] = max_ssim_single_npy
        #     max2_ssim[1] = npy_file_name
    sorted_similarity_list = sorted(similarity_list, key=lambda x:x[1], reverse=False)[:topN]
    res = ''
    for idx in range(0, topN):
        vid_path = rela_dict[sorted_similarity_list[idx][0]].split('/')
        vid_path_to_disp = vid_path[-2] + '\t' + vid_path[-1] + '\t' + str(sorted_similarity_list[idx][1])
        res = res + vid_path_to_disp + '\n'

    return res
    # if max2_ssim[1] != '':
    #     # print(max2_ssim[0])
    #     vid_path = rela_dict[max2_ssim[1]].split('/')
    #     vid_path_to_disp = vid_path[-2] + '\t' + vid_path[-1]
    #     return vid_path_to_disp
    # else:
    #     return 'No video found! '


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()

    argparser.add_argument('picture', help='Picture to find')
    argparser.add_argument('dataset', help='Dataset location')
    argparser.add_argument('--multi_datasets', help='If the dataset location contains more than one dataset folder',
                           action='store_true')
    argparser.add_argument('--pic_is_url', help='Use this flag when the picture is a URL', action='store_true')

    args = argparser.parse_args()
    pic_path = args.picture
    dataset_path = args.dataset
    is_multi_datasets = args.multi_datasets
    pic_is_url = args.pic_is_url
    assert os.path.isdir(dataset_path)
    # assert os.path.isfile(pic_path)

    if is_multi_datasets:
        ds_list = [os.path.join(dataset_path, ds) for ds in os.listdir(dataset_path) if os.path.isdir(ds)]
        res = []
        for ds in ds_list:
            res.append(find_vid(pic_path=pic_path, dataset_path=ds, resolution=(160, 120), pic_path_is_url=pic_is_url))
        [print('This video may be located in:\nDirectory:\tFile:\n' + r) for r in res]
    else:
        res = find_vid(pic_path=pic_path, dataset_path=dataset_path, resolution=(160, 120), pic_path_is_url=pic_is_url)
        print('This video may be located in:\nDirectory:\tFile:\n' + res)


