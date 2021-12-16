import os


def maybe_mkdir(path:str):
    if os.path.exists(path):
        print(f'Path {path} already existed !')
    else:
        os.mkdir(path)
        print(f'Path {path} created !')


def maybe_mkdirs(paths:list):
    for path in paths:
        maybe_mkdir(path)