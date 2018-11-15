#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'stringk'
__mtime__ = '2018/11/15'
# qq:2456056533

"""
import scrapy

from spiderIP.items import SpideripItem

w89_spider = 'w89'


class W89Spider(scrapy.Spider):
    name = w89_spider
    allowed_domains = ['89ip.cn']

    page = 1

    def start_requests(self):

        urls = ['http://www.89ip.cn/index_1.html']  # 免费http
        for url in urls:
            yield scrapy.Request(url, meta={'cate': 'w89'}, callback=self.parse_detail)

    def parse_detail(self, response):
        category = response.meta['cate']
        _ip = ''
        for tr in response.xpath('//tbody/tr'):
            item = SpideripItem()
            _ip = tr.xpath('td[1]/text()').extract_first().replace('\t', '').replace('\n', '')
            _port = tr.xpath('td[2]/text()').extract_first().replace('\t', '').replace('\n', '')
            _protocol = 'http'

            item['category'] = category
            item['ip'] = _protocol+'://' +_ip + ':' + _port
            item['niming'] = ''
            item['protocol'] = _protocol
            item['speed'] = ''
            item['connect_time'] = ''
            item['alive_time'] = ''
            item['prove_time'] = tr.xpath('td[5]/text()').extract_first().replace('\t', '').replace('\n', '')
            yield item
            # print(item)

        # 页数
        if _ip:
            self.page += 1
            yield scrapy.Request('http://www.89ip.cn/index_{page}.html'.format(page=self.page), meta={'cate': 'w89'},
                                 callback=self.parse_detail)
