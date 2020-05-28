import json
import threading
import time

import utils
'''
    多线程
    超时几率高
    下载失败居多
    下载画师全部插画创作
'''
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36 '
}
all_time = 0


def download_thread(illust_id):
    utils.save_pixiv_pic(illust_id, root_dir, 1)



start = time.time()
user_id = 4754550
root_dir = "D:\\pixiv\\user_{}".format(user_id)
json_text_url = "https://www.pixiv.net/ajax/user/{}/profile/all?lang=zh_tw".format(user_id)
json_text = utils.get_html_utf8_text_with_cookie(json_text_url, headers)
json_obj = json.loads(json_text)
illusts = json_obj.get('body').get('illusts')
print("▶▶▶▶▶▶寻找到{}个作品ID".format(len(illusts)))
for illust in illusts:
    t1 = threading.Thread(target=download_thread, kwargs={'illust_id':illust})
    t1.start()

print('总计：{:.2f}s'.format(time.time()-start))
