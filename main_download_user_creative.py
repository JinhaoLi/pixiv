import json
import utils
'''
    下载画师全部插画创作
'''
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36 '
}

root_dir = "I:\\pixiv\\user_264932"
json_text_url = "https://www.pixiv.net/ajax/user/264932/profile/all?lang=zh_tw"
json_text = utils.get_html_utf8_text_with_cookie(json_text_url, headers)
json_obj = json.loads(json_text)
illusts = json_obj.get('body').get('illusts')
for illust in illusts:
    utils.save_pixiv_pic(illust, root_dir)
