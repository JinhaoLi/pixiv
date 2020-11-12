import json
import time
import os
import utils

'''
    同步
    下载画师全部插画创作
'''
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36 '
}
start = time.time()
user_id = 3115085
root_dir = "D:\\pixiv\\user_{}".format(user_id)
json_text_url = "https://www.pixiv.net/ajax/user/{}/profile/all?lang=zh_tw".format(user_id)
json_text = utils.get_html_utf8_text_with_cookie(json_text_url, headers, use_proxy=True)
json_obj = json.loads(json_text)
illusts = json_obj.get('body').get('illusts')
utils.log("▶▶▶▶▶▶寻找到{}个作品ID".format(len(illusts)))
for illust in illusts:
    if os.path.exists(root_dir+"/{}_p0.jpg".format(illust)):
        utils.log("{}已存在！".format(illust))
        continue
    # 不分类型
    utils.save_pixiv_pic(illust, root_dir, 1)
    # 只下动图
    # utils.save_pixiv_pic_only_gif(illust, root_dir, 1)

utils.log('总计：{:.2f}s'.format(time.time() - start))
os.system("shutdown -s -t 60")
