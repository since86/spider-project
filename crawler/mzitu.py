# coding=utf-8
import requests
import os
import time
from lxml import html
import random
from pymongo import MongoClient

class mzitu():
    User_Agent = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]

    User_IP = [
        {'https':'36.78.221.132:32848'},
        {'http':'157.65.168.42:3128'},
        {'http':'39.135.10.95:8080'},
        {'https':'47.105.147.162:80'}
    ]

    def __init__ (self):
        self.client = MongoClient(host='127.0.0.1',port=27017)
        self.db = self.client['mzituPic']
        self.collection = self.db['mzitu']
        self.jpg_download_list = []
        self.base_url = 'http://www.mzitu.com'


    def getUser_Agent(self):
        UA = random.choice(self.User_Agent)
        headers = {
            'User-Agent': UA,
            'referer': 'http://www.mzitu.com/'
        }
        return headers

    def getUser_IP(self):
        IP = random.choice(self.User_IP)
        ip = {'IP': IP}
        return ip

    ##获取主页下所有套图的入口
    def getAllPage_location(self,num=1):
        # print(u'开始获取第%s页套图入口地址'%(str(num)))
        jpg_location = []
        now_url = '{}/page/{}'.format(self.base_url,num)
        selector = html.fromstring(self.GetRespon(now_url).text)
        for loc in selector.xpath('//div[@class="postlist"]/ul/li/a/@href'):
            jpg_location.append(loc)
        # print(u'第%s页套图入口地址获取完成'%(str(num)))
        return jpg_location

    ##获取套图下的图片的详细信息，包括标题,图片总数,下载地址
    def getAllJpg_Info(self,url):
        # print(u'开始获取图片下载地址')
        del self.jpg_download_list[:]     ##图片下载地址
        selector = html.fromstring(self.GetRespon(url).text)
        title = selector.xpath('//div[@class="main"]/div[@class="content"]/h2/text()')[0]
        total = selector.xpath('//div[@class="pagenavi"]/a[last()-1]/span/text()')[0]
        for jpgpage in range(1,int(total)+1):
            # now_url = '{}/{}'.format(url,jpgpage)
            # selector = html.fromstring(self.GetRespon(now_url).text)
            # # print(selector.xpath('//div[@class="main-image"]/p/a/img/@src')[0])
            # self.jpg_download_list.append(selector.xpath('//div[@class="main-image"]/p/a/img/@src')[0])
            now_url = '{}/{}'.format(url,jpgpage)
            selector = html.fromstring(self.GetRespon(now_url,10).text)
            try:
                s = selector.xpath('//div[@class="main-image"]/p/a/img/@src')[0]
            except:
                continue
            if self.collection.find_one({'url':s}):
                print(u'这个图片已被爬取，跳过')
            else:
                self.jpg_download_list.append(s)
                self.collection.insert_one({'主题':title,'url':s})
        return title,total

    def download(self,title_total):
        # print(u'开始下载')
        count = 1
        Jpg_Num = title_total[1]
        Jpg_Name = title_total[0]
        dirName = '[%sP]%s'%(Jpg_Num,Jpg_Name)
        dirName = '{}/{}'.format(r'e:/spider/mzitu',dirName)
        isExists = os.path.isdir(dirName)
        if isExists == True:
            return False
        else:
            os.mkdir(dirName)
            for jpg in self.jpg_download_list:
                file_name = '%s/%s.jpg'%(dirName,str(count))
                with open(file_name,"wb") as Jpg:
                    # print(u'开始下载 [%s]P %s 第%s张'%(Jpg_Num,Jpg_Name,str(count)))
                    j = self.GetRespon(jpg)
                    Jpg.write(j.content)
                    time.sleep(0.5)
                count+=1

    #地址,延迟时间,重新尝试次数,代理Ip,
    def GetRespon(self,url,timeout=10,num_retries=4,proxy=None):
        print(u'开始获取地址：',url)
        if proxy == None:
            try:
                return requests.get(url,headers=self.getUser_Agent(),timeout=timeout)
            except:
                if num_retries > 0:
                    print(u'尝试重新连接，等待10S,剩余次数:%s次'%(num_retries))
                    time.sleep(10)
                    return self.GetRespon(url,timeout,num_retries-1)
                else:
                    print(u'我的IP不好使啦，使用代理IP')
                    return self.GetRespon(url,timeout,4,self.getUser_IP())
        else:
            try:
                return requests.get(url,headers=self.getUser_Agent(),proxies=proxy,timeout=timeout)
            except:
                if num_retries > 0:
                    print(u'尝试重新连接，等待10S,剩余次数:%s次'%(num_retries))
                    time.sleep(10)
                    return self.GetRespon(url,timeout,num_retries-1)
                else:
                    print(u'代理Ip有点不好用，取消代理')
                    return self.GetRespon(url,timeout,4,None)

    def run(self,num):
        for i in self.getAllPage_location(num):
            self.download(self.getAllJpg_Info(i))

if __name__ == '__main__':
    mz = mzitu()
    mz.run(1)

