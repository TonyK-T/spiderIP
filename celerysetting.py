#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'stringk'
__mtime__ = '2018/11/12'
# qq:2456056533

"""

from celery.schedules import crontab

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Asia/Shanghai'
enable_utc = True
result_expires = 60 * 60 * 1  # 存储过期时间


beat_schedule = {'everyday-9-14-18':
                     {'task': 'tasks.task_run_all',
                      'schedule': crontab(minute=0,hour='9,14,18'),
                      'args': ()
                      },

                 'everyday-9.30-':
                     {'task': 'tasks.task_run_dbIPCheck',
                      'schedule': crontab(minute=30,hour='9,11,14,18'),
                      'args': ()
                      },
                 }
