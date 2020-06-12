import threading
import cv2
import utils
import pyperclip
import time
import re
import PIL

'''
每隔一秒监测剪切板变化 ，有变化就解析获取id，获取到id就执行下载
'''


def download_thread(illust_id):
    utils.save_pixiv_pic(illust_id, "D:\\pixiv\\like\\", 1)
    pass


before = ''
while 1:
    time.sleep(1)
    data = pyperclip.paste()
    if data != before:
        print(data)
        result = re.findall('\\d{6,8}', data)
        if not len(result) == 0:
            illust_id = result[0]
            print("匹配到结果：{}".format(illust_id))
            t1 = threading.Thread(target=download_thread, kwargs={'illust_id': illust_id})
            t1.start()
        else:
            print('无效数据')
            # utils.save_pixiv_pic(illust_id)
        before = data
