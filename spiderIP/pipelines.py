# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from queue import Queue

from redis import Redis
from scrapy.exceptions import DropItem
import asyncio
from spiderIP.model import IPModel, create_newtable, engine, get_sqlsession
from spiderIP.ipcheck import IPCheck, IPcheckRedis
from spiderIP.settings import IP_REDIS


class BaseSpiderPipeline(object):
    def __init__(self):
        self.queue = Queue()
        self.new_queue = Queue()
        create_newtable(engine)
        self.session = get_sqlsession(engine)
        self.loop = asyncio.get_event_loop()

    def process_item(self, item, spider):
        if spider.name == 'xici':
            speed = item['speed']
            connect_time = item['connect_time']
            if int(speed) > 50 and int(connect_time) > 70:  # 筛选 速度70，链接时间80
                self.queue.put(item)
            else:
                raise DropItem()
        elif spider.name == 'kuaidaili':
            # 无需筛选
            self.queue.put(item)

        elif spider.name == 'w66':
            # 无筛选
            self.queue.put(item)

        return item

    def close_spider(self, spider):
        '''
        三个spider,三个IPCheck()对象,六个线程,N个协程
        '''
        IPCheck().run_ip_check(self.loop, self.queue, self.new_queue)

        while not self.new_queue.empty():
            item = self.new_queue.get(timeout=5)
            _item = IPModel.db_distinct(self.session, IPModel, item, item['ip'])
            IPModel.save_mode(self.session, IPModel(), _item)


        self.session.close()
        # self.loop.close() # loop无需手动关闭,见源码: finally: _run_until_complete_cb



class RedisPipline:
    '''
    另一种实现：通过 redis 代替 Queue, ip校验失败嘤嘤嘤
    '''
    redis = Redis(host=IP_REDIS)
    redis_key ='ip:requests'
    redis_key2 = 'ip:save'

    def __init__(self):
        create_newtable(engine)
        self.session = get_sqlsession(engine)
        self.loop = asyncio.get_event_loop()

    def process_item(self, item, spider):
        self.redis.sadd(self.redis_key,item)
        return item

    def close_spider(self,spider):
        IPcheckRedis().run_ip_check(self.loop, self.redis, self.redis_key,self.redis_key2)
        while True:

            item = self.redis.spop(self.redis_key2)
            if not item:break
            _item = eval(item.decode('utf-8'))
            _item = IPModel.db_distinct(self.session, IPModel, _item, _item['ip'])

            IPModel.save_mode(self.session, IPModel(), _item)

        self.session.close()
