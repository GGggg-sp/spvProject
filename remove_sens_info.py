import os
import pickle as pk
import argparse

from utils.operations import maybe_mkdir


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('dataset')
    argparser.add_argument('target_dir')
    args = argparser.parse_args()
    dataset_dir = args.dataset
    target_dir = args.target_dir
    maybe_mkdir(target_dir)
    assert os.path.isdir(dataset_dir)

    pkl_file_list = [file for file in os.listdir(dataset_dir) if file.endswith('.pkl')]
    for pkl_file in pkl_file_list:
        no_sense_phash_table = {}
        pkl_file_path = os.path.join(dataset_dir, pkl_file)
        with open(pkl_file_path, 'rb') as f:
            phash_table = pk.load(f)
        for vid_path in phash_table:
            vid_path_split = vid_path.split('/')
            no_sens_path = vid_path_split[-2] + '/' + vid_path_split[-1]
            no_sense_phash_table[no_sens_path] = phash_table[vid_path]
        no_sens_pkl_path = os.path.join(target_dir, pkl_file)
        with open(no_sens_pkl_path, 'wb') as f:
            pk.dump(no_sense_phash_table, f)
        print(f'Dataset {pkl_file} Processed! ')
