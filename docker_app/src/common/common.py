'''
@author: qujb
@contact: 15210825203@163.com
@file: common.py
@time: 2019/6/6 上午12:32
@desc:
'''
import time

local_time = time.localtime(time.time())


def is_cur_day(timestamp):
    if time.localtime(timestamp).tm_yday == local_time.tm_yday:
        return 1
    else:
        return 0


def is_cur_week(timestamp):
    if time.localtime(timestamp).tm_yday/7 == local_time.tm_yday/7:
        return 1
    else:
        return 0


def is_cur_month(timestamp):
    if time.localtime(timestamp).tm_mon == local_time.tm_mon:
        return 1
    else:
        return 0
