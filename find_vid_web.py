
import pywebio as wio
import argparse
import os

from find_vid_hash import find_vid

dataset_path = ''
def web_server():
    while True:
        wio.output.put_text('汉责，茉莉，Handspanking, Spanking Movie jp 系列视频查找')
        img = wio.input.file_upload('上传截图: ', accept='image/*', max_size='10M')
        if not img:
            continue
        wio.output.put_text('Finding videos ...')
        res = find_vid('', dataset_path=dataset_path, pic_bytecontent=img['content'])
        wio.output.put_text('spm-mp4 为 spanking movie jp\nmicro-videos, micro-films为汉责视频\nChinses Spanking 为茉莉视频\n')
        wio.output.put_text('该视频可能是下列视频中的一个:\n序号:\t所属目录:\t视频名称: （从上往下可能性依次递减）\n' + res)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('dataset', help='Dataset location')
    args = argparser.parse_args()
    dataset_path = args.dataset
    assert os.path.isdir(dataset_path)
    wio.start_server(web_server, port=8008, host='')