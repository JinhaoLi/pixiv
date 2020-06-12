import os
import re
import time
import utils
import daily

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36 '
}
# 每日排行榜
url = "https://www.pixiv.net/ranking.php?mode=daily_r18"
root_dir = "I:\\pixiv\\"
date = time.strftime("%Y_%m_%d", time.localtime())  # 格式化成2016_03_20形式
print("▶-->下载{}的R18排行榜".format(date),end="\t")
save_dir = root_dir + "\\" + "daily_r18_" + date
if os.path.exists(save_dir):
    print("----->文件夹已存在！")
    exit(0)
else:
    print("----->创建文件夹！")
    os.makedirs(save_dir)
html_text = utils.get_html_utf8_text_with_cookie(url, headers)
if html_text is None:
    exit(-1)
paras = daily.DailyParser()
paras.feed(html_text)
id_count = len(paras.data)
print("▶▶-->找到" + str(id_count) + "个插画ID")
for i in range(id_count):
    print("▶▶▶-->进度[" + str(i) + '/' + str(id_count) + "]-->" + paras.data[i])
    illust_id = re.match("\\d{8}", paras.data[i])   # str中获取id
    utils.save_pixiv_pic(illust_id[0], save_dir + "\\")
