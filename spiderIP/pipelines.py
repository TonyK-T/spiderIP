# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from queue import Queue

from scrapy.exceptions import DropItem
from spiderIP.model import IPModel, create_newtable, engine, get_sqlsession
from spiderIP.ipcheck import IPCheck


class BaseSpiderPipeline(object):
    def __init__(self):
        self.queue = Queue()
        self.new_queue = Queue()
        create_newtable(engine)
        self.session = get_sqlsession(engine)

    def process_item(self, item, spider):
        # print('*********入队：', item)
        if spider.name == 'xici':
            speed = item['speed']
            connect_time = item['connect_time']
            if int(speed) > 40 and int(connect_time) > 50:  # 筛选 速度70，链接时间80
                self.queue.put(item)
            else:
                raise DropItem()
        elif spider.name == 'kuaidaili':
            # 无需筛选
            self.queue.put(item)

        elif spider.name == 'w66':
            # 无筛选
            self.queue.put(item)

        elif spider.name == 'w89':
            # 无筛选
            self.queue.put(item)

        else:
            self.queue.put(item)

        return item

    def close_spider(self, spider):
        
        IPCheck().run_ip_check(self.queue, self.new_queue)

        while not self.new_queue.empty():
            item = self.new_queue.get(timeout=2)
            _item = IPModel.db_distinct(self.session, IPModel, item, item['ip'])
            IPModel.save_mode(self.session, IPModel(), _item)

        # 关闭db连接
        self.session.close()
