#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'stringk'
__mtime__ = '2018/6/20'
# qq:2456056533

佛祖保佑  永无bug!

"""

import scrapy
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess
from spiderIP.items import SpideripItem

w66_spider ='w66'

class W66Spider(scrapy.Spider):
    name = w66_spider
    allowed_domains = ['66ip.cn']
    num = 1000

    def start_requests(self):

        urls =['http://www.66ip.cn/mo.php?sxb=&tqsl={}&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea='.format(self.num)]
        for url in urls:
            yield scrapy.Request(url,meta={'cate':'w66'},callback=self.parse)

    def parse(self, response):
        category = response.meta['cate']
        soup = BeautifulSoup(response.text, 'lxml')
        for br in soup.find_all('br'):
            ip = br.next.strip()

            item = SpideripItem()
            item['category'] = category
            item['ip'] = ip
            item['niming'] = '透明'
            item['protocol'] = 'http'
            item['speed'] = ''
            item['connect_time'] = ''
            item['alive_time'] = ''
            item['prove_time'] = ''
            yield item

# if __name__ == '__main__':
#
#     process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
#     # process = CrawlerProcess(get_project_settings())
#     process.crawl(W66Spider)
#     process.start()