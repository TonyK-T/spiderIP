#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'stringk'
__mtime__ = '2018/11/15'
# qq:2456056533

"""

import grequests
import requests
def __grequests():
    url ='https://www.baidu.com/'
    # url = 'http://news.163.com/latest/'

    # http代理只能校验http_url ,否则会使用本地ip(https同理,须对应)
    # proxies ={
    #     'http':'http://117.21.182.14:89'    # {'http':'117.21.182.14:80'} 这种也行 ==>  grequests
    # }
    proxies = {'https': 'https://218.60.8.98:3129'}
    rf = grequests.get(url,proxies=proxies)
    resp = grequests.map([rf])
    for r in resp:
        print(r.status_code)
        # print(r.text)

def __requests():

    url = 'https://www.baidu.com/'

    # http代理只能校验http_url ,否则会使用本地ip(https同理,须对应)
    proxies = {'https': 'https://218.60.8.98:3129'}     # requests 库  value 须加上 http://

    # HTTP Basic Auth 密码认证
    #proxies = {"http": "http://user:pass@10.10.1.10:3128/", }

    # 代理混合写法
    # proxies = {"http": "http://10.10.1.10:3128", "https": "https://10.10.1.10:1080", }

    resp = requests.get(url,proxies=proxies)
    print(resp.status_code)



if __name__ == '__main__':
    __grequests()
    #__requests()