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

from run_spiders import run_dbIPCheck

'''apscheduler 定时'''

scheduler = BlockingScheduler()

curre_path = os.path.abspath(os.path.dirname(__file__))

py_path = str(os.path.join(curre_path, 'run_spiders.py'))
print(py_path)


@scheduler.scheduled_job(trigger='cron', id='task_run_all', minute='*/30')
def task_run_all():
    cmd = 'python {}'.format(py_path)
    print('--------------', cmd)
    subprocess.Popen(cmd, shell=True)


@scheduler.scheduled_job(trigger='cron', id='task_run_dbIPCheck', minute='*/15')
def task_run_dbIPCheck():
    run_dbIPCheck()  # win 下不会执行函数，因为 grequests 库gevent导致，Linux正常


# 监听
def listen_task(event):
    if event.exception:
        print('**********启动出错*********')
    else:
        print('**********启动任务*********')


scheduler.add_listener(listen_task, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

scheduler.start()
