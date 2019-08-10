#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'stringk'
__mtime__ = '2018/6/21'
# qq:2456056533

佛祖保佑  永无bug!

"""

# grequests 内部做了处理
# import gevent
# from gevent import monkey
# monkey.patch_all()

import grequests

import functools
import requests
import random

from spiderIP.model import engine, get_sqlsession, IPModel
from spiderIP.ipcheck import http_url, https_url


class DbIPCheck:
    '''
    校验数据库ip是否可用
    '''
    db_session = get_sqlsession(engine)

    def get_ip(self):
        result = []
        try:
            result = self.db_session.query(IPModel.protocol, IPModel.ip).all()
        except Exception as e:
            print(e)
            self.db_session.rollback()
        return result

    def check_ip(self):
        grequests_tasks = []
        useful = []
        useless = []  # 无用proxies
        all_proxies = [x for x in self.get_ip()]  # [('http', 'http://202.101.13.68:80'), ]
        for pro in all_proxies:
            proxy = {pro[0]: pro[1]}
            if 'http' in proxy.keys():
                url = random.choice(http_url)
            else:
                url = random.choice(https_url)
            grequests_tasks.append(grequests.get(url, proxies=proxy,
                                                 callback=functools.partial(self.grequests_callback, proxies=proxy,
                                                                            useful=useful), timeout=1.5))

        resp = grequests.map(grequests_tasks,
                             exception_handler=functools.partial(self.exception_handler, useless=useless))
        if resp:
            return useful, useless

    def exception_handler(self, request, exception, useless):
        '''
        异常请求回调函数
        '''
        proxies = request.__dict__['kwargs']['proxies']
        print('exception_handler:无用ip--', proxies)
        useless.append(proxies)  # {'http': 'http://180.150.191.251:8889'}

    def grequests_callback(self, resp, proxies, useful, *args, **kwargs):
        '''
        请求成功的回调函数, 请求失败的proxies 并不触发此回调,直接返回None，
        '''
        if resp.status_code == 200:
            print('grequests_callback:有用IP--', proxies)
            useful.append(proxies)  # OrderedDict([('http', 'http://94.16.122.115:3128')])

    def del_ip(self):
        useful_proxies, useless_proxies = self.check_ip()
        with IPModel.auto_commit(self.db_session):
            for i in useless_proxies:  # i == {'http': 'http://61.138.33.20:808'} | https
                print('无用ip删除:', i)

                _ip = [x for x in i.values() if x]
                if _ip:
                    ip_model = self.db_session.query(IPModel).filter_by(ip=_ip[0]).all()
                    [self.db_session.delete(ip) for ip in ip_model]

        print('有用的ip数：', len(useful_proxies))
        print('无用的ip数：', len(useless_proxies))

        self.db_session.close()


def single_request():
    '''
    单个 ip 测试
    :return:
    '''
    url = 'http://news.163.com/latest/'
    proxies = {'http': 'http://5.16.11.190:8080'}

    # url = 'https://www.baidu.com/'
    # proxies = {'https': 'https://119.27.177.169:80'}
    try:
        resp = requests.get(url, proxies=proxies, timeout=1)
        print(resp.status_code)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    DbIPCheck().del_ip()
    # single_request()
