#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = '80022068'
__mtime__ = '2019/8/9'
# qq:2456056533


"""
from multiprocessing import Process
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from apscheduler.schedulers.blocking import BlockingScheduler

from run_dbCheck import run_dbIpCheck
from run_spiders import run_all

scheduler = BlockingScheduler()


@scheduler.scheduled_job(trigger='date', id='task_run_all', run_date='2019-12-12 16:30:01')
# @scheduler.scheduled_job(trigger='cron', id='task_run_all', minute='*/40')
def task_run_all():
    pro = Process(target=run_all)
    pro.start()
    pro.join()
    pro.terminate()


@scheduler.scheduled_job(trigger='date', id='task_run_dbIPCheck', run_date='2019-12-11 17:06:01')
# @scheduler.scheduled_job(trigger='cron', id='task_run_dbIPCheck', minute='*/10')
def task_run_dbIPCheck():
    pass
    # Process(target=run_dbIpCheck).start()


# 监听
def listen_task(event):
    if event.exception:
        print('**********执行任务出错*********')
    else:
        print('**********执行任务成功*********')


scheduler.add_listener(listen_task, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

print('**********启动定时任务*********')
scheduler.start()

'''

step-1： 修改 model.py  mysql连接
setp-2:  nohup python -u tasks_apscheduler.py &


'''
