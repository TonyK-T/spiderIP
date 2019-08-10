#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = '80022068'
__mtime__ = '2019/8/9'
# qq:2456056533

佛祖保佑  永无bug!

"""
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from spiderIP.items import SpideripItem

xila_spider = 'xila'


class Xila(scrapy.Spider):
    name = xila_spider
    page_count = 50
    ursl = ['http://www.xiladaili.com/http/{page}', 'http://www.xiladaili.com/gaoni/{page}',
            'http://www.xiladaili.com/https/{page}']

    def start_requests(self):
        for url in self.ursl:  # 调试
            _url = url.format(page=1)
            yield scrapy.Request(_url, callback=self.parse_list)

            # 翻页
            for i in range(self.page_count):
                _url = url.format(page=i)
                yield scrapy.Request(_url, callback=self.parse_list)

    def parse_list(self, response):
        # print(response.text)
        trs = response.xpath('//table[@class="fl-table"]/tbody/tr')
        for tr in trs:  # 调试
            cate = 'xila'
            ip_num = tr.xpath('td/text()').extract_first()
            protocol = tr.xpath('td[2]/text()').extract_first()
            if protocol:
                protocol = protocol.replace('代理', '').lower()

                niming = tr.xpath('td[3]/text()').extract_first()
                speed = tr.xpath('td[5]/text()').extract_first()
                alive_time = tr.xpath('td[6]/text()').extract_first()
                prove_time = tr.xpath('td[7]/text()').extract_first()
                item = SpideripItem()
                item['category'] = cate
                item['protocol'] = protocol
                item['ip'] = protocol.split(',')[0] + '://' + ip_num
                item['niming'] = niming
                item['speed'] = speed
                item['connect_time'] = ''
                item['alive_time'] = alive_time
                item['prove_time'] = prove_time
                # print(item)
                yield item


if __name__ == '__main__':
    # process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
    process = CrawlerProcess(get_project_settings())
    process.crawl(Xila)
    process.start()
