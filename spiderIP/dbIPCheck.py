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
#
# monkey.patch_all()

import grequests

import functools
import requests

from spiderIP.model import engine, get_sqlsession, IPModel


class DbIPCheck:
    '''
    校验数据库ip是否可用
    '''
    db_session = get_sqlsession(engine)

    def __del__(self):
        self.db_session.close()

    def get_ip(self):

        result = self.db_session.query(IPModel.protocol, IPModel.ip).all()
        return result

    def check_ip(self):
        grequests_tasks = []
        useful = []
        useless = []  # 无用的ip
        all_proxies = [x for x in self.get_ip()]  # [('http', '202.101.13.68:80'), ]
        for pro in all_proxies:
            proxy = {pro[0]: pro[1]}
            if pro[0] == 'http':
                url = 'http://ip.chinaz.com/getip.aspx'
            else:
                url = 'https://www.baidu.com/'

            grequests_tasks.append(grequests.get(url, proxies=proxy,
                                                 callback=functools.partial(self.grequests_callback, proxies=proxy,
                                                                            useful=useful),
                                                 timeout=1.5))  # proxies = {'http': '101.236.36.31:8866'}
            # grequests_tasks.append(grequests.get(url, proxies=pro, timeout=2))

        resp = grequests.map(grequests_tasks, exception_handler=functools.partial(self.exception_handler,
                                                                                  useless=useless))
        if resp:
            return useful, useless

    def exception_handler(self, request, exception, useless):
        '''
        异常请求回调函数
        :param request: 
        :param exception: 
        :param useless: 
        :return: 
        '''
        ip = request.__dict__['kwargs']['proxies']
        print('exception_handler:无用ip--', ip)
        useless.append(ip)  # {'http': '180.150.191.251:8889'}

    def grequests_callback(self, resp, proxies, useful, *args, **kwargs):
        '''
        请求成功的回调函数
        :param resp: 
        :param proxies: 
        :param useful: 
        :param args: 
        :param kwargs: 
        :return: 
        '''
        if resp.status_code == 200:
            print('grequests_callback:有用IP--', proxies)
            useful.append(proxies)  # OrderedDict([('http', '94.16.122.115:3128')])  有序字典

    def del_ip(self):
        useful_ip, useless_ip = self.check_ip()

        with IPModel.auto_commit(self.db_session):
            for i in useless_ip:  # i == {'http': '61.138.33.20:808'} | https
                print('无用ip删除:', i)
                _ip = [x for x in i.values()]
                ip_model = self.db_session.query(IPModel).filter_by(ip=_ip[0]).all()
                [self.db_session.delete(ip) for ip in ip_model]

        print('有用的ip数：', len(useful_ip))
        print('无用的ip数：', len(useless_ip))

def single_request():
    '''
    # 单 ip 测试
    :return: 
    '''
    url = 'http://ip.chinaz.com/getip.aspx'
    proxies = {'http': '39.135.24.11:80'}
    try:
        resp = requests.get(url, proxies=proxies, timeout=1)
        print(resp.status_code)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    DbIPCheck().del_ip()
    # single_request()
