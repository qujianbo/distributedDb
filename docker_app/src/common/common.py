'''
@author: qujb
@contact: 15210825203@163.com
@file: common.py
@time: 2019/6/9 上午12:53
@desc:
'''
import time
import pickle
import json
from bson.json_util import dumps
from bson.json_util import loads
local_time = time.localtime(time.time())

def stamp_2_str(timeStamp):

    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
    return otherStyleTime

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

def available_value(value):
    """
    判断是否为redis能存储的数据类型： str or bytes
    :param value:
    :return:
    """
    if isinstance(value, str) or isinstance(value, bytes):
        return value
    return dumps(value)

def utc_2_local(t):
    return t.astimezone()

def doc_2_json(doc):
    if doc is None:
        return None
    return dumps(doc)


def str_2_dict(s):
    if s is None:
        return None
    return loads(s)