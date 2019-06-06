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
# 根据传进来的连接生成be_read表
def generate_be_read(t2,t):

    Be_read1 = []
    Be_read2 = []

    # 这里根据读取read表和airticle 表生成be-read 表
    read_collection = t2.get_collection('read')
    article_collection = t2.get_collection('article')

    for article_item in article_collection.find():
        # print(type(item))
        # belong to db_bj t1
        # if article_item["category"] == "science":
        # 找出所有文章id一致的read_item list
        read_item = read_collection.find(dict(aid=article_item["aid"]))


        one_read = {}
        one_read["readNum"] = 0
        one_read["commentNum"] = 0
        one_read["agreeNum"] = 0
        one_read["shareNum"] = 0

        # one_read["timestamp"] = timestamp

        one_read["readUidList"] = []
        one_read["commentUidList"] = []
        one_read["agreeUidList"] = []
        one_read["shareUidList"] = []

        for single_read in list(read_item):

            if single_read:

                one_read["aid"] = single_read["aid"]
                one_read["timestamp"] = single_read["timestamp"]
                one_read["readNum"] = one_read["readNum"] + 1
                one_read["readUidList"].append(single_read["uid"])

                if single_read["commentOrNot"] == "1":
                    one_read["commentUidList"].append(single_read["uid"])
                    one_read["commentNum"] = one_read["commentNum"] + 1

                if single_read["agreeOrNot"] == "1":
                    one_read["agreeUidList"].append(single_read["uid"])
                    one_read["agreeNum"] = one_read["agreeNum"] + 1

                if single_read["shareOrNot"] == "1":
                    one_read["shareUidList"].append(single_read["uid"])
                    one_read["shareNum"] = one_read["shareNum"] + 1
        if one_read["readNum"]:
            if article_item["category"] == "science":
                Be_read1.append(one_read)
                Be_read2.append(one_read)
            else:
                Be_read2.append(one_read)


    # 往表中插入这条数据
    if t2.region == 'Beijing':
        t2.bulk_insert("be_read", Be_read1)
        t.bulk_insert("be_read", Be_read2)

    if t2.region == 'Hong Kong':
        t2.bulk_insert("be_read", Be_read2)
        t.bulk_insert("be_read", Be_read1)

def generate_pop(t2):

    daily_rank = {}
    week_rank = {}
    month_rank = {}

    be_read_collection = t2.get_collection('be_read')
    cur_timestamp = int(time.time())

    daily_rank["temporalGranularity"] = "daily"
    daily_rank["timestamp"] = cur_timestamp

    month_rank["temporalGranularity"] = "monthly"
    month_rank["timestamp"] = cur_timestamp

    week_rank["temporalGranularity"] = "weekly"
    week_rank["timestamp"] = cur_timestamp

    daily_rank["articleList"] = []
    week_rank["articleList"] = []
    month_rank["articleList"] = []

    for be_read_item in be_read_collection.find():

        article_item = {}
        timestamp = int(be_read_item["timestamp"])
        article_item["readNum"] = be_read_item["readNum"]
        article_item["commentNum"] = be_read_item["commentNum"]
        article_item["agreeNum"] = be_read_item["agreeNum"]
        article_item["shareNum"] = be_read_item["shareNum"]
        article_item["aid"] = be_read_item["aid"]

        if is_cur_day(timestamp):
            daily_rank["articleList"].append(article_item)

        if is_cur_week(timestamp):
            week_rank["articleList"].append(article_item)

        if is_cur_month(timestamp):
            month_rank["articleList"].append(article_item)
    # 默认按照阅读量排序
    sort_list(daily_rank["articleList"], '1')
    sort_list(week_rank["articleList"], '1')
    sort_list(month_rank["articleList"], '1')

    t2.get_collection("pop_rank").update({"temporalGranularity": "daily"}, daily_rank, upsert=True)
    t2.get_collection("pop_rank").update({"temporalGranularity": "weekly"}, week_rank, upsert=True)
    t2.get_collection("pop_rank").update({"temporalGranularity": "monthly"}, month_rank, upsert=True)
