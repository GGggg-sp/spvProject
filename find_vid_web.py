
import pywebio as wio
import argparse
import os

from find_vid_hash_mp import find_vid

dataset_path = ''
def web_server():
    wio.session.set_env(title='404 sp video finder')
    while True:
        wio.output.put_text('汉责, 茉莉, Handspanking, Spanking Movie jp, Spanking Real Life, Lupus, NuWest, Spanked in uniform, GBS, '
                            'Shadow Lane, Cutie spankee, Northern spanking系列视频及日本部分影片查找')
        # wio.output.put_text('仅在避难所测试使用')
        img = wio.input.file_upload('上传截图: ', accept='image/*', max_size='10M')
        if not img:
            continue
        wio.output.put_text('正在查找视频中，请勿刷新界面 ...')
        res = find_vid('', dataset_path=dataset_path, pic_bytecontent=img['content'])
        wio.output.put_text('spm-mp4 为 spanking movie jp\nmicro-videos, micro-films为汉责视频\nChinses Spanking 为茉莉视频\n')
        # wio.output.put_text('该视频可能是下列视频中的一个:\n序号:\t所属目录:\t视频名称: （从上往下可能性依次递减）\n' + res)
        wio.output.put_image(bytearray(img['content']))
        wio.output.put_text('该视频可能是下列视频中的某一个（从上往下可能性依次递减）:')
        wio.output.put_table(res, header=[('序号','vid_index'), ('目录','vid_folder'), ('视频名称','vid_name'),
                                          ('时间点', 'vid_timestamp'), ('误差程度', 'hamming_dist')])



if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('dataset', help='Dataset location')
    args = argparser.parse_args()
    dataset_path = args.dataset
    assert os.path.isdir(dataset_path)
    wio.start_server(web_server, port=8008, host='')