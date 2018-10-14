# coding=utf-8
import requests
from lxml import html
import re
import time
import random
from pymongo import MongoClient
from wordcloud import WordCloud
import matplotlib.pyplot as plt

'''
爬取51job合肥软件工程师职位，使用mongodb保存，并根据职位生成云图
'''

class job51():
    def __init__(self):
        self.base_url = 'https://search.51job.com/list/150200,000000,0000,00,9,99,{search},2,{page}.html'.format(search='软件工程师',page=1)
        self.headers={
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        }
        self.client = MongoClient(host='127.0.0.1',port=27017)
        self.db = self.client['51job']
        self.collection = self.db['softEng']

    def get_pages(self):
        page_list = []
        rsp = requests.get(self.base_url,headers=self.headers)
        selector = html.fromstring(rsp.content.decode('gbk'))
        totals = selector.xpath('//div[@class="p_in"]/span[@class="td"]/text()')
        match = re.compile(r'\d+')
        total = match.search(totals[0]).group()
        for i in range(1,int(total)+1):
            url = 'https://search.51job.com/list/150200,000000,0000,00,9,99,{search},2,{page}.html'.format(search='软件工程师',page=i)
            page_list.append(url)
        # print(page_list)
        return page_list

    def get_details(self,url):
        rsp = requests.get(url,headers=self.headers)
        selector = html.fromstring(rsp.content.decode('gbk'))
        div_list = selector.xpath('//div[@class="dw_table"]/div[@class="el"]')

        for div in div_list:
            name = div.xpath('p/span/a/text()')[0].strip()
            company = div.xpath('span/a/text()')[0]
            area = div.xpath('span[@class="t3"]/text()')[0]
            salary = div.xpath('span[@class="t4"]/text()')
            pub_time = div.xpath('span[@class="t5"]/text()')[0]
            detail_url = div.xpath('p/span/a/@href')[0]
            salary = salary[0] if salary else '面议'
            if(self.collection.find_one({'url':detail_url})):
                print(u'已经爬取,跳过！！')
            else:
                self.collection.insert_one({'职位':name,'公司':company,'区域':area,'工资范围':salary,'发布时间':pub_time,'url':detail_url})

    def run(self):
        for page in self.get_pages():
            self.get_details(page)
            time.sleep(random.uniform(1,2))
        print(u'爬取完成！')

    def yuntu(self):
        jobname = []
        for job in self.collection.find():
            jobname.append(job['职位'])
        job_name = ''.join(jobname)
        my_wordcloud = WordCloud(max_words=100,width=1600,height=800,font_path=r"C:\Windows\Fonts\msyh.ttf",random_state=30).generate(job_name)
        my_wordcloud.to_file('softEng.png')
        plt.imshow(my_wordcloud)
        plt.axis('off')
        plt.show()




job = job51()
# job.get_pages()
job.run()
# job.yuntu()