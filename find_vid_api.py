from fastapi import FastAPI
from find_vid_hash import find_vid
import os
import argparse


# if __name__ == '__main__':
    # argparser = argparse.ArgumentParser()
    # argparser.add_argument('dataset')
    #
    # args = argparser.parse_args()
dataset = '/Volumes/ExtremeSSD/dataset'
app = FastAPI()



@app.get('/findvid/{pic_url:path}')
async def find_vid_api(pic_url):
    res = find_vid(pic_path='https://' + pic_url, dataset_path=dataset, pic_path_is_url=True)
    res_str = ''
    for itm in res:
        res_str = res_str + str(itm['vid_index']) + '\t' + itm['vid_folder'] + '\t' \
                  + itm['vid_name'] + '\t时间: ' + str(itm['vid_timestamp']) + '\n'
    return res