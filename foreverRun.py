import os
from datetime import time
import time
import utils
import json


# https://www.pixiv.net/ajax/illust/79962521/recommend/init?limit=18

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/79.0.3945.117 Safari/537.36 '
}


def create_dir():
    root_dir = "I:\\pixiv\\recommend"
    # 格式化成2016-03-20 11:45:39形式
    date = time.strftime("%Y_%m_%d", time.localtime())
    print(date)
    save_dir = root_dir + "\\" + date + "_pic"+"\\"
    if os.path.exists(save_dir):
        print("文件夹已存在！")
    else:
        os.makedirs(save_dir)
    return save_dir


data_json_url = "https://www.pixiv.net/ajax/illust/80069351/recommend/init?limit=18"
json_text = utils.get_html_soure_with_cookie(data_json_url, headers)
data = json.load(json_text)
save_dir = create_dir()
illusts = data.get("body").get("illusts")
for illust in illusts:
    print(illust.get("illustId") + ":" + illust.get("illustTitle"))
    utils.save_pixiv_pic(illust.get("illustId"), save_dir)
