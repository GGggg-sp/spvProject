
import pywebio as wio
import argparse
import os

from find_vid import find_vid

dataset_path = ''
def web_server():
    while True:
        wio.output.put_text('茉莉系列视频查找')
        img = wio.input.file_upload('上传截图: ', accept='image/*', max_size='10M')
        if not img:
            continue
        wio.output.put_text('Finding videos ...')
        res = find_vid('', dataset_path=dataset_path, pic_bytecontent=img['content'])
        wio.output.put_text('This video may be located in:\nIndex:\tDirectory:\tFile:\tError(lower is better):\n' + res)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('dataset', help='Dataset location')
    args = argparser.parse_args()
    dataset_path = args.dataset
    assert os.path.isdir(dataset_path)
    wio.start_server(web_server, port=8008, host='')