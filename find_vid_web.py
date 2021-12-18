
import pywebio as wio

from find_vid import find_vid

def web_server():
    while True:
        img = wio.input.file_upload('Upload your image: ', accept='image/*', max_size='10M')
        if not img:
            continue
        wio.output.put_text('Finding videos ...')
        res = find_vid('', '/Volumes/ExtremeSSD/spm_dataset', pic_bytecontent=img['content'])
        wio.output.put_text('This video may be located in:\nIndex:\tDirectory:\tFile:\tError(lower is better):\n' + res)


if __name__ == '__main__':
    wio.start_server(web_server, 8008)