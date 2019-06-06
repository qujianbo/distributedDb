'''
@author: qujb
@contact: 15210825203@163.com
@file: common.py
@time: 2019/6/6 上午12:32
@desc:
'''
import time
import operator
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

'''
对受欢迎程度按照不同角度进行一个排序
1.阅读数   2.评论    3.点赞
4.分享
可以传入一个list，按照先后顺序进行排序
这里留作后续实现
'''
def sort_list(article_list,key):
    if key == '1':
        article_list.sort(key=lambda item:item.get("readNum"), reverse = True)

    if key == '2':
        article_list.sort(key=lambda item: item.get("commentNum"), reverse=True)

    if key == '3':
        article_list.sort(key=lambda item: item.get("agreeNum"), reverse=True)

    if key == '4':
        article_list.sort(key=lambda item: item.get("shareNum"), reverse=True)
