# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from spiderIP.items import SpideripItem

xici_spider = 'xici'

class XiciSpider(scrapy.Spider):
    name = xici_spider
    allowed_domains = ['xicidaili.com']
    page_num = 45                            # 页数, 越往后 ip西刺[验证时间]越老

    def start_requests(self):
        urls = ['http://www.xicidaili.com/wt/','http://www.xicidaili.com/wn/']    # http,https  # 'http://www.xicidaili.com/wn/'

        for url in urls:
            for i in range(1,self.page_num):
                u = url+str(i)
                yield scrapy.Request(u,meta={'cate':'xici'},callback=self.parse)

    def parse(self, response):
        category = response.meta['cate']
        ip_list = response.xpath('//table[@id="ip_list"]')
        tr_list = ip_list.xpath('tr')

        for i in range(1,len(tr_list)):  #
            item = SpideripItem()
            item['category'] = category
            ip = tr_list[i].xpath('td[2]/text()').extract_first()
            port = tr_list[i].xpath('td[3]/text()').extract_first()
            item['ip'] = ip+':'+port

            item['niming'] = tr_list[i].xpath('td[5]/text()').extract_first()
            item['protocol'] = tr_list[i].xpath('td[6]/text()').extract_first().lower()
            item['speed'] = tr_list[i].xpath('td[7]/div/div/@style').extract_first()[-3:-1]
            item['connect_time'] = tr_list[i].xpath('td[8]/div/div/@style').extract_first()[-3:-1]
            item['alive_time'] = tr_list[i].xpath('td[9]/text()').extract_first()
            item['prove_time'] = tr_list[i].xpath('td[10]/text()').extract_first()
            yield item


