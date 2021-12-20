import os
import argparse
import cv2
import numpy as np
import pickle as pk
import json


def remove_black_border(img):
    new_image = None
    row_threshold = 6
    border_height_threshhold = 3
    (height, width) = img.shape[0], img.shape[1]
    rgb_sum = np.sum(img, axis=2)
    row_sum = np.sum(rgb_sum, axis=1)
    index = np.where(row_sum > row_threshold)[0]
    if index.shape[0] > 0 and index[0] > border_height_threshhold:
        if np.abs(index[0] - (height - index[-1])) < 6 and index[-1] - index[0] > 30:
            new_image = img[index[0]:index[-1], :, :]
            new_image = cv2.resize(new_image, (width, height))
    if new_image is None:
        return img
    else:
        return new_image


def phash(img):
    hash_size = 8
    highfreq_factor = 4
    img_size = hash_size * highfreq_factor
    imgp = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) / 255.0
    dct = cv2.dct(cv2.resize(imgp, (img_size, img_size)))
    dctlowfreq = dct[:hash_size, :hash_size]
    med = np.median(dctlowfreq)
    diff = dctlowfreq > med
    bit_string = ''.join(str(b) for b in 1 * diff.flatten())
    width = int(np.ceil(len(bit_string) / 4))
    hash_str = '{:0>{width}x}'.format(int(bit_string, 2), width=width)
    hash = diff.flatten()
    return (hash, hash_str)


def compute_database(database_dir: str, if_remove_black_border=False):
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
            if if_remove_black_border:
                img = remove_black_border(npy_content[i, :, :, :])
            else:
                img = npy_content[i, :, :, :]
            current_phash, _ = phash(img)
            phash_list.append(current_phash)
        phash_table[rela_video_file_path] = phash_list
    phash_tabel_path = os.path.join(database_dir, 'hash_tabel.pkl')
    with open(phash_tabel_path, 'wb') as f:
        pk.dump(phash_table, f)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('dataset')
    argparser.add_argument('--remove_black_border', action='store_true')
    args = argparser.parse_args()
    dataset_dir = args.dataset
    if_remove_black_border = args.remove_black_border
    compute_database(dataset_dir, if_remove_black_border=if_remove_black_border)

# img1 = cv2.imread('test_imgs/1.png')
# img2 = cv2.imread('test_imgs/3.png')
# imgp1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
# imgp2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
#
# ((res1, _), (res2, _)) = phash(imgp1), phash(imgp2)
# print(hamming_distance(res1, res2))
# print("")
