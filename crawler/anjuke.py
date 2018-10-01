# coding=utf-8
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

def __init__ (self):
    self.client = MongoClient()
    self.db = self.client['Ayr']
    self.collection = self.db['spider']
    self.jpg_download_list = []
    self.base_url = 'http://www.mzitu.com'

# 网页的请求头
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
}

def get_page(url):
    pass

def get_details(url):
    pass

