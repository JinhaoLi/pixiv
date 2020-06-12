import json
import os
import zipfile
from io import BytesIO
from urllib import request
import threading
import imageio

from IllustParser import IllustParser

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/79.0.3945.117 Safari/537.36 '
}


def get_file_name_from_url(url):
    """
        从url获取文件名称
    :param url:
    :return: 文件名
    """
    # https://i0.hdslb.com/bfs/album/d5d9ab822599b8365a20e71bba364812c0ae4eae.jpg
    url_split = url.split("/")
    return url_split[len(url_split) - 1]


def get_html_utf8_text_with_cookie(url, headers):
    """
        带cookie发起请求并编码接收到的响应为utf8
        :param url:
        :param headers:
        :return:
    """
    req = request.Request(url, headers=headers)
    with open("cookie", "rb")as f:
        cookie = f.read().decode("utf-8")
    req.add_header("Cookie", cookie)
    try:
        resp = request.urlopen(req, timeout=20).read()
    except Exception as e:
        print("获取{}超时:".format(url)+'\n'+e.__str__())
        return None
    text = resp.decode("utf-8")
    return text


def get_html_utf8_text(url, headers):
    """
    发起请求并编码接收到的响应为utf8
    :param url:
    :param headers:
    :return:
    """
    req = request.Request(url, headers=headers)
    try:
        resp = request.urlopen(req, timeout=10).read()
    except:
        print("获取{}超时".format(url))
        return None
    text = resp.decode("utf-8")
    return text


def get_html_soure(url, headers=None, timeout=20):
    """
    发起请求并接收响应
    :param url:
    :param headers:
    :param timeout:
    :return:
    """
    req = request.Request(url, headers=headers)
    resp = request.urlopen(req, timeout=timeout)
    return resp


def get_html_soure_with_cookie(url, headers=None):
    """
    带cookie发起请求并接收
    :param url:
    :param headers:
    :return:
    """
    req = request.Request(url, headers=headers)
    try:
        with open("cookie", "rb")as f:
            cookie = f.read().decode("utf-8")
            req.add_header("Cookie", cookie)
    except Exception as e:
        print("cookie文件读取失败!"+str(e))
    try:
        resp = request.urlopen(req, timeout=10)
    except:
        print("获取{}超时".format(url))
        return None
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
    获取response的信息
    """
    url = '当前url:' + resp.geturl()
    resp_type = 'HTTPResponse类型:' + resp.getcode()
    more_info = '响应头相关的信息：' + resp.info()
    return url, resp_type, more_info


def save_pixiv_zip(illust_id, save_dir, jump_exist=0):
    """
    保存动图的zip文件
    :param illust_id: 插画id
    :param save_dir: 保存路径
    :param jump_exist: 是否覆盖已存在 1为true
    :return:
    """
    if not save_dir.endswith("\\"):
        save_dir = save_dir + "\\"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    url = "https://www.pixiv.net/ajax/illust/{}/ugoira_meta?lang=zh_tw".format(illust_id)
    json_text = get_html_utf8_text_with_cookie(url, headers)
    json_obj = json.loads(json_text)
    zip_url = json_obj.get("body").get("src")
    print("▶▶▶-->正在下载[动图]：" + zip_url)
    req = request.Request(zip_url, headers=headers)
    req.add_header("referer", "https://www.pixiv.net/")
    try:
        zip_resp = request.urlopen(req, timeout=30)
        print("▶▶▶-->图片大小：", "{}MB\t----->".format(get_resp_len(zip_resp)), end="\t")
        with open(save_dir + get_file_name_from_url(zip_url), "wb") as f:
            f.write(zip_resp.read())
            print("✔下载成功")
    except IOError as e:
        print("✘下载失败" + str(e))
    pass


def save_pixiv_gif(illust_id, save_dir, jump_exist=0, quality=0):
    """
    保存动图
    :param illust_id: 动图id
    :param save_dir: 保存文件夹路径
    :param jump_exist: 是否覆盖已存在 1为true
    :param quality: 质量 1为原图 0为缩略图
    :return:
    """
    if not save_dir.endswith("\\"):
        save_dir = save_dir + "\\"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if quality == 1:
        file_path = save_dir + str(illust_id) + '_full.gif'
    else:
        file_path = save_dir + str(illust_id) + '.gif'
    if jump_exist == 1 and os.path.exists(file_path):
        print("※文件已存在！跳过")
        return
    url = "https://www.pixiv.net/ajax/illust/{}/ugoira_meta?lang=zh_tw".format(illust_id)
    json_text = get_html_utf8_text_with_cookie(url, headers)
    json_obj = json.loads(json_text)
    # 图片质量600*600
    if quality == 1:
        zip_url = json_obj.get("body").get("originalSrc")
    else:
        zip_url = json_obj.get("body").get("src")
    delay = json_obj['body']['frames'][1]['delay']
    fps = 1000 / delay
    print("▶▶▶-->正在下载[动图]：" + zip_url)
    req = request.Request(zip_url, headers=headers)
    req.add_header("referer", "https://www.pixiv.net/")
    try:
        zip_resp = request.urlopen(req, timeout=30)
        print("▶▶▶-->图片大小：", "{}MB\t----->".format(get_resp_len(zip_resp)), end="\t")
        pic_bytes = zip_resp.read()
        t1 = threading.Thread(target=zip_to_gif, args=(pic_bytes, file_path, int(fps)))
        t1.start()
        # zip_to_gif(zip_resp.read(),save_dir+str(illust_id)+'.gif')
    except IOError as e:
        print("✘下载失败" + str(e))
    pass


def zip_to_gif(zip_bytes, file_path, fps=40):
    """
    将zip文件内的图片合成gif
    :param zip_bytes: zip字节流
    :param file_path: gif保存的路径
    :param fps: gif的帧率
    :return:
    """
    fio = BytesIO(zip_bytes)
    myzip = zipfile.ZipFile(fio)
    print('多线程合成zip中的{}张图片到gif'.format(len(myzip.namelist())), end='->')
    frames = []
    for zip_f in myzip.filelist:
        zip_file = BytesIO(myzip.read(zip_f))
        frames.append(imageio.imread(zip_file))
    imageio.mimsave(file_path, frames, 'GIF', fps=fps)
    print('▶▶▶gif合成成功{}'.format(file_path))
    pass


def json_obj_from_id(illust_id):
    """
    获取插画的json 对象
    :param illust_id: 插画id
    :return:
    """
    illust_url_temp = "https://www.pixiv.net/artworks/"
    illust_page_text = get_html_utf8_text(illust_url_temp + str(illust_id), headers)
    if illust_page_text is None:
        return None
    second_paras = IllustParser()
    second_paras.feed(illust_page_text)
    return json.loads(second_paras.json_text)


def json_text_from_id(illust_id):
    """
    获取插画的json文本
    :param illust_id: 插画id
    :return:
    """
    illust_url_temp = "https://www.pixiv.net/artworks/"
    illust_page_text = get_html_utf8_text(illust_url_temp + str(illust_id), headers)
    if illust_page_text is None:
        return None
    second_paras = IllustParser()
    second_paras.feed(illust_page_text)
    return second_paras.json_text


# pixiv专用
def save_pixiv_pic_only_gif(illust_id, save_dir, jump_exist=0):
    """
    下载此illust_id 的插画
    只下载动图
    :param illust_id:
    :param save_dir:   保存位置
    :param jump_exist:  存在是否跳过
    :return:
    """
    if not save_dir.endswith("\\"):
        save_dir = save_dir + "\\"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    illust_url_temp = "https://www.pixiv.net/artworks/"
    illust_page_text = get_html_utf8_text(illust_url_temp + str(illust_id), headers)
    if illust_page_text is None:
        return None
    second_paras = IllustParser()
    second_paras.feed(illust_page_text)
    illust_json = json.loads(second_paras.json_text)
    if illust_json.get("illust").get(str(illust_id)).get('illustType') == 2:
        save_pixiv_gif(illust_id, save_dir, jump_exist)
    else:
        return
    pass


# pixiv专用
def save_pixiv_pic(illust_id, save_dir, jump_exist=0):
    """
    下载此illust_id 的插画
    不分类型
    :param illust_id:
    :param save_dir:   保存位置
    :param jump_exist:  存在是否跳过
    :return:
    """
    if not save_dir.endswith("\\"):
        save_dir = save_dir + "\\"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    illust_json = json_obj_from_id(illust_id)
    if illust_json is None:
        return
    if illust_id is None:
        return
    if illust_json.get("illust").get(str(illust_id)).get('illustType') == 2:
        save_pixiv_gif(illust_id, save_dir, jump_exist)
        return
    pic_count = illust_json.get("illust").get(str(illust_id)).get("pageCount")
    original_url = illust_json.get("illust").get(str(illust_id)).get("urls").get("original")
    split_url = original_url.split("_")
    print("▶▶共" + str(pic_count) + "张图")
    for i in range(pic_count):
        pic_url = split_url[0] + "_p" + str(i) + "." + split_url[1].split(".")[1]
        print("▶▶▶-->正在下载[" + str(i) + "]：" + pic_url)
        illust_file_name = save_dir + get_file_name_from_url(pic_url)
        if jump_exist == 1 and os.path.exists(illust_file_name):
            print("※文件已存在！跳过")
            continue
        req = request.Request(pic_url, headers=headers)
        req.add_header("referer", "https://www.pixiv.net/")
        try:
            resp = request.urlopen(req, timeout=20)
            print("▶▶▶-->图片大小：", "{}MB\t----->".format(get_resp_len(resp)), end="\t")
            with open(illust_file_name, "wb")as pic:
                pic.write(resp.read())
            print("✔下载成功")
        except IOError as e:
            print("✘下载失败" + str(e))
            continue
    print("=================================================▶")
    pass
