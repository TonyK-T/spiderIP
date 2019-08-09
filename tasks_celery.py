# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# """
# __title__ = ''
# __author__ = 'stringk'
# __mtime__ = '2018/11/12'
# # qq:2456056533
#
# """
# import sys
#
# from celery import Celery, platforms
# from run_spiders import run_dbIPCheck, run_all
#
# ''' celery 定时任务-还需借助redis '''
#
#
# # 须改写这个路径
# sys.path.append('/home/stringk/scrapy_pro/spiderIP/')
#
# platforms.C_FORCE_ROOT = True  # 解决Linux root用户执行问题
#
# app = Celery('celery_task', broker='redis://127.0.0.1:6379')
#
# app.config_from_object('celerysetting')
#
#
# @app.task
# def task_run_all():
#     # run_all()    # celery 直接调用 scrapy 会出错
#     import subprocess
#     subprocess.Popen('python run_spiders.py')
#
#
# @app.task
# def task_run_dbIPCheck():
#     run_dbIPCheck()  # win 下不会执行函数，因为 grequests 库gevent导致，Linux正常
#
#
# if __name__ == '__main__':
#     app.start(argv='celery -A tasks beat')
#
#     # celery -A tasks beat
#     # celery -A tasks worker -l info -P eventlet        # win10下 使用 eventlet-定时 情况下莫名不会执行方法,(linux 下正常且不需要-P eventlet)
#
#     # from tasks import task_run_dbIPCheck      # 手动测试调用
#     # s = task_run_dbIPCheck.delay()
#     # s.get()
#
#     # nohup ./beat.sh &     # 每次重新发布定时任务之前，都需要删除 celerybeat.pid celerybeat-schedule.dir celerybeat-schedule.bak celerybeat-schedule.dat,不然会报错
#     # nohup ./worker.sh &   # 后台执行
