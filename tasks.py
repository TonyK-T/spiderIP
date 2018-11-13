#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'stringk'
__mtime__ = '2018/11/12'
# qq:2456056533

"""
import sys

# 必须改写这个路径才可定时
sys.path.append('/home/stringk/scrapyproject/spiderIP/')

from celery import Celery

from run import run_dbIPCheck, run_all

app = Celery('celery_task', broker='redis://127.0.0.1:6379')

app.config_from_object('celerysetting')


@app.task
def task_run_all():
    run_all()


@app.task
def task_run_dbIPCheck():
    run_dbIPCheck()


if __name__ == '__main__':
    app.start()


    # celery -A tasks beat
    # celery -A tasks worker -l info -P eventlet        # win10下 使用 eventlet 定时跑 莫名不会执行方法,(linux 下不需要-P eventlet 正常)

    # from tasks import task_run_dbIPCheck      # 手动测试调用
    # s = task_run_dbIPCheck.delay()
    # s.get()

    # nohup ./beat.sh &     # 每次重新发布定时任务之前，都需要删除 celerybeat.pid celerybeat-schedule.dir celerybeat-schedule.bak celerybeat-schedule.dat,不然会报错
    # nohup ./worker.sh &   # 后台执行