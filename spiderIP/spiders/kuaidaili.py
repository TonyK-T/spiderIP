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
from scrapy.crawler import CrawlerProcess

from spiderIP.items import SpideripItem

kuaidaili_spider = 'kuaidaili'

class KuaiSpider(scrapy.Spider):
    name = kuaidaili_spider
    allowed_domains = ['kuaidaili.com']
    page_num = 3                             # 辣鸡,一页都懒得爬

    custom_settings = {

    }

    def start_requests(self):
        urls =['https://www.kuaidaili.com/free/intr/','https://www.kuaidaili.com/free/inha/']        # http,https

        for url in urls:
            for i in range(1,self.page_num):
                u = url+str(i)+'/'
                yield scrapy.Request(u,meta={'cate':'kuaidaili'},callback=self.parse)

    def parse(self, response):
        category = response.meta['cate']
        ip_list = response.xpath('//table[@class="table table-bordered table-striped"]/tbody')
        tr_list = ip_list.xpath('tr')
        for i in range(0,len(tr_list)):
            item = SpideripItem()
            item['category'] = category

            ip = tr_list[i].xpath('td[1]/text()').extract_first()
            port = tr_list[i].xpath('td[2]/text()').extract_first()
            protocol = tr_list[i].xpath('td[4]/text()').extract_first().lower()
            item['ip'] = protocol +'://'+ip + ':' + port
            item['protocol'] = protocol

            item['niming'] = tr_list[i].xpath('td[3]/text()').extract_first()
            item['speed'] = tr_list[i].xpath('td[6]/text()').extract_first()[-3:-1]
            item['connect_time'] = ''
            item['alive_time'] = ''
            item['prove_time'] = tr_list[i].xpath('td[7]/text()').extract_first()
            yield item


if __name__ == '__main__':

    process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
    # process = CrawlerProcess(get_project_settings())
    process.crawl(KuaiSpider)
    process.start()