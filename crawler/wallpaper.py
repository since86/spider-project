# coding=utf-8
import requests
import os
import time
from bs4 import BeautifulSoup
from multiprocessing import Pool


url_host = 'http://wallpaperswide.com'

headers = {
    'UserAgent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.21 Safari/537.36',
    'Connection': 'keep-alive'
}

headers2 = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0",
    "Host": "wallpaperswide.com",
    "Upgrade-Insecure-Requests": 1
}

proxies = {'HTTP': '123.56.28.196:8888'}


def get_image_links(page_url):
    # print('get_image_links starts')
    wb_data = requests.get(page_url, headers=headers, proxies=proxies, timeout=10)
    time.sleep(1)
    if wb_data.status_code == 200:
        soup = BeautifulSoup(wb_data.text, 'lxml')
        if soup.find('div', 'pagination'):
            img_links = soup.select('#content > ul > li > div > a')
            # print(img_links)
            for link in img_links:
                data = {
                    'link': link.get('href'),
                    'title': link.get('title')
                }
                get_imgs(data)
        else:
            print('last page')
    else:
        print('<Response [%s]>' % wb_data.status_code)


def get_imgs(data):
    # print('get_imgs starts')
    img_url = '{}{}'.format(url_host, data['link'])
    wb_data = requests.get(img_url, headers=headers)

    if wb_data.status_code == 200:
        soup = BeautifulSoup(wb_data.text, 'lxml')
        download_titles = soup.select('#wallpaper-resolutions > a')
        for title in download_titles:
            if title.get('title').find('1920 x 1080') != -1:
                download_img(title.get('href'))
            else:
                pass
                # print('not found')
    else:
        return '<Response: [%s]>' % wb_data.status_code


def download_img(download_url):
    print('download_img starts')
    d_url = '{}{}'.format(url_host, download_url)
    r = requests.get(d_url, headers=headers2, proxies=proxies, timeout=10)

    base_dir = os.path.dirname(__file__)  # 获取当前文件夹的绝对路径
    file_path = os.path.join(base_dir, 'papers')  # 获取当前文件夹内的Test_Data文件
    # print(file_path)

    target = '{}/{}'.format(file_path, d_url.split('/')[4])
    print(d_url.split('/')[4])
    with open(target, "wb") as fs:
        fs.write(r.content)


def get_cates_link(host_url):
    cates_link = []
    wb_data = requests.get(host_url, headers=headers, proxies=proxies, timeout=10)
    if wb_data.status_code == 200:
        soup = BeautifulSoup(wb_data.text, 'lxml')
        cate_links = soup.select('ul.side-panel.categories > li > a')
        for cate in cate_links:
            cates_link.append(cate.get('href'))
        return cates_link
    else:
        print('<Response [%s]>' % wb_data.status_code)


if __name__ == '__main__':
    # http://wallpaperswide.com/girls-desktop-wallpapers/page/2
    url_withoutpages = ['{}{}/page/'.format(url_host, cate) for cate in get_cates_link(url_host)]

    url_finals = []
    for url in url_withoutpages:
        for i in range(1, 31):
            url_withpage = '{}{}'.format(url, str(i))
            url_finals.append(url_withpage)
    # print(url_finals)

    pool = Pool()
    pool.map(get_image_links, url_finals)
    pool.close()
    pool.join()