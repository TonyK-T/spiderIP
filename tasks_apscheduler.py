#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = '80022068'
__mtime__ = '2019/8/9'
# qq:2456056533


"""
import os
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess

'''apscheduler 定时
   
   注：apscheduler or celery 定时执行 异步库[aiohttp,scrapy,grequests] 会出现线程间异常，
       需借助 subprocess 拉起一个新进程来执行
   
    
'''

scheduler = BlockingScheduler()

curre_path = os.path.abspath(os.path.dirname(__file__))

py_path = str(os.path.join(curre_path, 'run_spiders.py'))
print(py_path)


@scheduler.scheduled_job(trigger='cron', id='task_run_all', minute='*/40')
def task_run_all():
    cmd = 'python {}'.format(py_path)
    print('----ip爬取 ----------', cmd)
    subprocess.Popen(cmd, shell=True)


@scheduler.scheduled_job(trigger='cron', id='task_run_dbIPCheck', minute='*/10')
def task_run_dbIPCheck():
    '''win 下不会执行函数，因为 grequests 库gevent导致，Linux正常'''
    cmd = 'python {}'.format(str(os.path.join(curre_path, 'run_dbCheck.py')))
    print('-----ip校验--------', cmd)
    subprocess.Popen(cmd, shell=True)


# 监听
def listen_task(event):
    if event.exception:
        print('**********启动出错*********')
    else:
        print('**********启动任务*********')


scheduler.add_listener(listen_task, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

scheduler.start()

'''

step-1： 修改 model.py  mysql连接
setp-2:  nohup python -u tasks_apscheduler.py &


'''
