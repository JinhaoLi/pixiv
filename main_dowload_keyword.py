import json
import urllib.parse as parse
import utils
"""
根据关键词下载
"""
base_url = 'https://www.pixiv.net/ajax/search/illustrations/' \
           '{}?'
param = {
    'word': "R-18",
    'mode': 3,
    'p': 2,
    's_mode': 's_tag_full',
    'type': 'illust_and_ugoira',
    'lang': 'zh_tw',
    'order': 'date_d'
}
wait_to_download = []


def found_illust(page=1):
    param['p'] = page
    encode_param = parse.urlencode(param)
    print(encode_param)
    start_url = base_url.format(param['word']) + encode_param
    print(start_url)
    json_text = utils.proxy_get_html_utf8_text(start_url, utils.headers)
    if json_text is None:
        found_illust(page+1)
        return
    json_obj = json.loads(json_text)
    id_list = json_obj['body']['illust']['data']

    for id_illust in id_list:
        root_obj = utils.json_obj_from_id(id_illust['id'], True)
        if root_obj is None:
            continue
        _j_obj = root_obj['illust'][id_illust['id']]
        bookmarkCount = _j_obj['bookmarkCount']
        viewCount = _j_obj['viewCount']
        likeCount = _j_obj['likeCount']

        print('==================================================')
        print('▶▶▶插画地址：\t{}'.format(_j_obj['extraData']['meta']['canonical']))
        print('▶▶▶标题：{}'.format(_j_obj['illustTitle']))
        print('▶▶▶书签计数：{}'.format(bookmarkCount))
        print('▶▶▶观看计数：{}'.format(viewCount))
        print('▶▶▶喜欢计数：{}'.format(likeCount))

        if bookmarkCount > 5000 or viewCount > 20000:
            wait_join =json.dumps(root_obj)
            wait_to_download.append(wait_join)

    if len(wait_to_download) > 0:
        with open('wait_to_download\\R18_viewCount_5000.json', 'w') as f:
            f.write(json.dumps(wait_to_download))
    found_illust(page + 1)


try:
    found_illust(1)
except Exception as e:
    print('异常退出(尝试保存数据)：'+e.__str__())
    json_list = json.dumps(wait_to_download)
    with open('wait_to_download\\R18_viewCount_5000_Exception.json', 'a') as f:
        f.write(json_list)
