
import shutil as su
import os
import json
import argparse
import random
import string


from utils.operations import maybe_mkdir


def merge_datasets(original_datasets:[str], target_dir:str):
    new_rela_dict = {}

    for dataset_path in original_datasets:
        print('Merging dataset @ {}'.format(dataset_path))
        with open(os.path.join(dataset_path, 'rela_dict.json'), 'r') as f:
            rela_dict = json.load(f)

        for npy_file_name in rela_dict:
            new_npy_file_name = npy_file_name
            if npy_file_name in new_rela_dict.keys():
                while True:
                    new_npy_file_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7)) + '.npy'
                    if not new_npy_file_name in new_rela_dict.keys():
                        break
            su.copyfile(os.path.join(dataset_path, npy_file_name),
                        os.path.join(target_dir, new_npy_file_name))
            new_rela_dict[new_npy_file_name] = rela_dict[npy_file_name]
        with open(os.path.join(target_dir, 'rela_dict.json'), 'w') as f:
            json.dump(new_rela_dict, f, indent=4)
    print("The following datasets are successfully merged to new datasets @ {}:\n".format(target_dir))
    for itm in original_datasets:
        print(itm + '\n')


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--original_datasets', help='The datasets to be merged', action='append')
    argparser.add_argument('--target_dir', help='Where the new dataset will be located in')

    args = argparser.parse_args()
    original_datasets = args.original_datasets
    target_dir = args.target_dir

    assert len(original_datasets) >= 2
    assert not target_dir in original_datasets

    maybe_mkdir(target_dir)
    merge_datasets(original_datasets=original_datasets, target_dir=target_dir)
