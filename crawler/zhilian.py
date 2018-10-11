# coding=utf-8
from pymongo import MongoClient
from lxml import html
import requests

base_url = "https://sou.zhaopin.com/?pageSize=60&jl=664&in=10100&jt=23,160000,045&kt=3"

headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

client = MongoClient(connect=False)
db = client['zhilian']
collection = db['zhilian']

def get_page(page=1):
    now_url = '{}{}'.format(base_url,str(page))
    selector = html.fromstring(requests.get(now_url,headers=headers).text)
    #获取工作名称
    jobname = selector.xpath('//table[@class="newlist"]/tr/td/div/a/text()')
    #过滤掉网站上的紧急招聘的多余内容
    jobname = filter(lambda x:x!='\xa0',jobname)
    #获取公司名称
    gsmc = selector.xpath('//table[@class="newlist"]/tr/td[@class="gsmc"]/a/text()')
    #获取职位月薪
    zwyx = selector.xpath('//table[@class="newlist"]/tr/td[@class="zwyx"]/text()')
    #获取工作地点
    gzdd = selector.xpath('//table[@class="newlist"]/tr/td[@class="gzdd"]/text()')
    for job,gs,yx,dd in zip(jobname,gsmc,zwyx,gzdd):
        dict = {
            "职位名称":job,
            "公司名称":gs,
            "月薪":yx,
            "工作地点":dd
        }
        collection.insert(dict)
        print(dict)
        print(u'插入数据库成功')

def run(i):
    get_page(i)

from multiprocessing import Pool

if __name__ == '__main__':
    p = Pool(2)
    for i in range(1,90+1):
        p.apply_async(run,(i,))
    p.close()
    p.join()