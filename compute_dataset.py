
import os
import argparse
import cv2
import numpy as np
import pickle as pk
import json


def phash(img):
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


def compute_database(database_dir:str):
    rela_dict_path = os.path.join(database_dir, 'rela_dict.json')
    with open(rela_dict_path, 'r') as f:
        rela_dict = json.load(f)
    print('Loaded rela_dict.json!')
    phash_table = {}
    for (npy_file_name, rela_video_file_path) in rela_dict.items():
        npy_file_path = os.path.join(database_dir, npy_file_name)
        print("Processing {}".format(npy_file_name))
        npy_content = np.load(npy_file_path)
        phash_list = []
        for i in range(0, npy_content.shape[0]):
            current_phash, _ = phash(npy_content[i, :, :])
            phash_list.append(current_phash)
        phash_table[rela_video_file_path] = phash_list
    phash_tabel_path = os.path.join(database_dir, 'hash_tabel.pkl')
    with open(phash_tabel_path, 'wb') as f:
        pk.dump(phash_table, f)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('dataset')
    args = argparser.parse_args()
    dataset_dir = args.dataset
    compute_database(dataset_dir)


# img1 = cv2.imread('test_imgs/1.png')
# img2 = cv2.imread('test_imgs/3.png')
# imgp1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
# imgp2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
#
# ((res1, _), (res2, _)) = phash(imgp1), phash(imgp2)
# print(hamming_distance(res1, res2))
# print("")