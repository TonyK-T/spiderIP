# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpideripItem(scrapy.Item):
    # define the fields for your item here like:
    category = scrapy.Field()
    protocol = scrapy.Field()  # 类型 http or https
    ip = scrapy.Field()
    # port = scrapy.Field()
    niming = scrapy.Field()    # 是否匿名
    speed = scrapy.Field()      # 速度
    connect_time = scrapy.Field() # 链接时间
    alive_time = scrapy.Field()  # 存活时间
    prove_time = scrapy.Field()     # 验证时间


