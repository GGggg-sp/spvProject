import numpy as np
import argparse
import os
import pickle as pk
import json
import cv2
from urllib.request import urlopen
import urllib.request as request
import datetime

def loss_mae(imga, imgb):
    mae = 0.0
    for chan in (0,1,2):
        (a, b) = imga[:,:,chan], imgb[:,:,chan]
        diff = a.astype(np.int16) - b.astype(np.int16)
        scale = a.shape[0] * a.shape[1]
        mae_s = np.sum(np.abs(diff))/scale
        mae = mae + mae_s
    return mae/3


def phash_c(img):
    hash_size = 8
    highfreq_factor = 4
    img_size = hash_size * highfreq_factor
    imgp = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)/255.0
    dct = cv2.dct(cv2.resize(imgp, (img_size, img_size)))
    dctlowfreq = dct[:hash_size, :hash_size]
    med = np.median(dctlowfreq)
    diff = dctlowfreq > med
    bit_string = ''.join(str(b) for b in 1 * diff.flatten())
    width = int(np.ceil(len(bit_string) / 4))
    hash_str = '{:0>{width}x}'.format(int(bit_string, 2), width=width)
    hash = diff.flatten()
    return (hash, hash_str)


def hamming_distance(hash1, hash2):
    # return sum(elm1 != elm2 for elm1, elm2 in zip(hash1, hash2))
    return np.count_nonzero(hash1 != hash2)



def find_vid(pic_path:str, dataset_path:str, resolution:(int, int) = (160, 120), topN:int = 5, pic_path_is_url:bool = False,
             pic_bytecontent = None):
    if pic_bytecontent:
        image = np.asarray(bytearray(pic_bytecontent), dtype='uint8')
        pic = cv2.imdecode(image, cv2.IMREAD_COLOR)
    elif pic_path_is_url:
        print("Loading image from url:")
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        req_h = request.Request(url=pic_path, headers=headers)
        req = urlopen(req_h)
        image = np.asarray(bytearray(req.read()), dtype='uint8')
        pic = cv2.imdecode(image, cv2.IMREAD_COLOR)
        print("Image loaded!")
    else:
        pic = cv2.imread(pic_path)

    pic = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
    pic = cv2.resize(pic, resolution)

    pic_hash, _ = phash_c(pic)

    # pkl_file_path = os.path.join(dataset_path, 'hash_tabel.pkl')
    pkl_file_path_list = [i for i in os.listdir(dataset_path) if i.endswith('.pkl')]
    phash_table = {}
    for pkl_file_name in pkl_file_path_list:
        pkl_file_path = os.path.join(dataset_path, pkl_file_name)
        with open(pkl_file_path, 'rb') as f:
            phash_table_t = pk.load(f)
            phash_table.update(phash_table_t)
    hamming_dist_list = []
    for vid_path in phash_table:
        phash_list_for_sigle_vid = phash_table[vid_path]
        most_sim_frame_idx = 0
        most_sim_frame_hash = 1000
        for (idx, phash) in enumerate(phash_table[vid_path]):
            sub = hamming_distance(phash, pic_hash)
            if sub <= most_sim_frame_hash:
                most_sim_frame_hash = sub
                most_sim_frame_idx = idx
        hamming_dist_list.append((vid_path, most_sim_frame_hash, most_sim_frame_idx))

    sorted_similarity_list = sorted(hamming_dist_list, key=lambda x:x[1], reverse=False)[:topN]
    res = []
    for idx in range(0, topN):
        vid_path = sorted_similarity_list[idx][0].split('/')
        vid_time = datetime.timedelta(seconds=sorted_similarity_list[idx][2] * 4)
        # vid_list = [str(idx + 1), +vid_path[-2], vid_path[-1] ] # +'\t' + str(sorted_similarity_list[idx][1])
        # res = res + vid_path_to_disp + '\t    @ {}\n'.format(vid_time)
        res.append({'vid_index': idx + 1,
                    'vid_folder': vid_path[-2],
                    'vid_name': vid_path[-1],
                    'vid_timestamp': vid_time,
                    'hamming_dist': sorted_similarity_list[idx][1]})
    return res


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()

    argparser.add_argument('picture', help='Picture to find')
    argparser.add_argument('dataset', help='Dataset location')
    # argparser.add_argument('--multi_datasets', help='If the dataset location contains more than one dataset folder',
    #                        action='store_true')
    argparser.add_argument('--pic_is_url', help='Use this flag when the picture is a URL', action='store_true')

    args = argparser.parse_args()
    pic_path = args.picture
    dataset_path = args.dataset
    # is_multi_datasets = args.multi_datasets
    pic_is_url = args.pic_is_url
    assert os.path.isdir(dataset_path)
    # assert os.path.isfile(pic_path)

    # if is_multi_datasets:
    #     ds_list = [os.path.join(dataset_path, ds) for ds in os.listdir(dataset_path) if os.path.isdir(ds)]
    #     res = []
    #     for ds in ds_list:
    #         res.append(find_vid(pic_path=pic_path, dataset_path=ds, resolution=(160, 120), pic_path_is_url=pic_is_url))
    #     [print('This video may be located in:\nIndex:\tDirectory:\tFile:\tError(lower is better):\n' + r) for r in res]
    # else:
    res = find_vid(pic_path=pic_path, dataset_path=dataset_path, resolution=(160, 120), pic_path_is_url=pic_is_url)
    print('spm-mp4 为 spanking movie jp\nmicro-videos, micro-films为汉责视频\nChinses Spanking 为茉莉视频\n')
    print('该视频可能是下列视频中的一个 in:\n序号:\t所属目录:\t视频名称: （从上往下可能性依次递减）\n')
    for itm in res:
        print(str(itm['vid_index']) + '\t' +
              itm['vid_folder'] + '\t' +
              itm['vid_name'] + '\t' +
              '@ ' + itm['vid_timestamp' + '\n'])


