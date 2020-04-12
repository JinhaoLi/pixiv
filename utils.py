import json
import os
from urllib import request

from IllustParser import IllustParser

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/79.0.3945.117 Safari/537.36 '
}


def get_file_name_from_url(url):
    # https://i0.hdslb.com/bfs/album/d5d9ab822599b8365a20e71bba364812c0ae4eae.jpg
    url_split = url.split("/")
    return url_split[len(url_split) - 1]


def get_html_utf8_text_with_cookie(url, headers):
    req = request.Request(url, headers=headers)
    with open("cookie", "rb")as f:
        cookie = f.read().decode("utf-8")
    req.add_header("Cookie", cookie)
    try:
        resp = request.urlopen(req, timeout=10).read()
    except:
        print("获取{}超时".format(url))
        return "null"
    text = resp.decode("utf-8")
    return text


def get_html_utf8_text(url, headers):
    req = request.Request(url, headers=headers)
    try:
        resp = request.urlopen(req, timeout=10).read()
    except:
        print("获取{}超时".format(url))
        return "null"
    text = resp.decode("utf-8")
    return text


def get_html_soure(url, headers=None, timeout=20):
    req = request.Request(url, headers=headers)
    resp = request.urlopen(req, timeout=timeout)
    return resp


def get_html_soure_with_cookie(url, headers=None):
    req = request.Request(url, headers=headers)
    with open("cookie", "rb")as f:
        cookie = f.read().decode("utf-8")
    req.add_header("Cookie", cookie)
    try:
        resp = request.urlopen(req, timeout=10)
    except:
        print("获取{}超时".format(url))
        return "null"
    return resp


# 保存图片的函数
def save_img(img_url, file_name, dir_path):
    # 打开图片链接获取图片
    pic = get_html_soure(img_url, headers)

    print("准备下载{}".format(img_url))
    # 保存到file_path文件路径下
    try:
        with open(dir_path + "/" + file_name, 'wb')as file:
            file.write(pic.read())
    except:
        print("下载失败")

    # 打印提示
    print("{}>>>>>>>>>下载成功!".format(file_name + "\t\t" + img_url))
    pass


def get_resp_len(resp):
    """
        获取response的大小，单位mb，类型float，保留两位小数
    """
    lenght = int(resp.info()['content-length'])
    lenght_mb = round(lenght / (1024 * 1024), 2)
    return lenght_mb


def get_resp_info(resp):
    """
    获取response的信息，换行符(\n)分割
    """
    url = '当前url:' + resp.geturl()
    resp_type = 'HTTPResponse类型:' + resp.getcode()
    more_info = '响应头相关的信息：' + resp.info()
    return url + "\n" + resp_type + "\n" + more_info + "\n"


# pixiv专用
def save_pixiv_pic(illust_id, save_dir):
    if not save_dir.endswith("\\"):
        save_dir = save_dir + "\\"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    illust_url_temp = "https://www.pixiv.net/artworks/"
    illust_page_text = get_html_utf8_text(illust_url_temp + str(illust_id), headers)
    if illust_page_text == "null":
        return
    second_paras = IllustParser()
    second_paras.feed(illust_page_text)
    illust_json = json.loads(second_paras.json_text)
    pic_count = illust_json.get("illust").get(str(illust_id)).get("pageCount")
    original_url = illust_json.get("illust").get(str(illust_id)).get("urls").get("original")
    split_url = original_url.split("_")
    print("▶▶共" + str(pic_count) + "张图")
    for i in range(pic_count):
        pic_url = split_url[0] + "_p" + str(i) + "." + split_url[1].split(".")[1]
        print("▶▶▶-->正在下载["+str(i)+"]：" + pic_url)
        req = request.Request(pic_url, headers=headers)
        req.add_header("referer", "https://www.pixiv.net/")
        try:
            resp = request.urlopen(req, timeout=20)
            print("▶▶▶-->图片大小：", "{}MB\t----->".format(get_resp_len(resp)), end="\t")
            with open(save_dir + get_file_name_from_url(pic_url), "wb")as pic:
                pic.write(resp.read())
            print("✔下载成功")
        except IOError as e:
            print("✘下载失败" + e)
    print("=================================================▶")
    pass
