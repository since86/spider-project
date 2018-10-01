# coding=utf-8
#爬取wallheaven上的图片
'''
未解决访问图片页面出现403的问题
'''
import os
import requests
import time
import random
from lxml.html import etree

keyword = input(f"{'input the keywords that you want to download :'}")

class Spider():
    def __init__(self):
        self.headers={
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        }
        self.filePath = (r'e:/spider/'+keyword+'/')

    def create_file(self):
        filePath = self.filePath
        if not os.path.exists(filePath):
            os.makedirs(filePath)

    def get_pagenum(self):
        total = ''
        url = ("https://alpha.wallhaven.cc/search?q={}&categories=111&purity=100&sorting=relevance&order=desc").format(keyword)
        html = requests.get(url)
        selector = etree.HTML(html.text)
        pageInfo = selector.xpath('//header[@class="listing-header"]/h1[1]/text()')
        string = str(pageInfo[0])
        numlist = list(filter(str.isdigit,string))#
        for item in numlist:
            total += item
        totalPagenum = int(total)
        return totalPagenum

    def main_function(self):
        self.create_file()
        count = self.get_pagenum()
        print('we have found: {} images'.format(count))
        times = int(count/24 +1)
        j = 1
        for i in range(times):
            pic_urls = self.getLinks(i+1)
            for item in pic_urls:
                self.download(item,j)
                j += 1

    def getLinks(self,num):
        url = ("https://alpha.wallhaven.cc/search?q={}&categories=111&purity=100&sorting=relevance&order=desc&page={}").format(keyword,num)
        try:
            html = requests.get(url)
            selector = etree.HTML(html.text)
            pic_linklist = selector.xpath('//a[@class="jsAnchor thumb-tags-toggle tagged"]/@href')
        except Exception as e:
            print(repr(e))

        return pic_linklist

    def download(self,url,count):
        string = url.strip('/thumbTags').strip('https://alpha.wallheaven.cc/wallpaper/')
        #   https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-115343.jpg
        html = 'https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-'+string + '.jpg'
        pic_path = (self.filePath+keyword+str(count)+'.jpg')
        try:
            pic = requests.get(html,headers = self.headers)
            with open(pic_path,'wb') as f:
                f.write(pic.content)
            print('Image: {} has been download!'.format(count))
            time.sleep(random.uniform(0,2))#
        except Exception as e:
            print(repr(e))

spider = Spider()
spider.main_function()
