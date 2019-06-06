'''
@author: qujb
@contact: 15210825203@163.com
@file: populate.py
@time: 6/3/19 4:36 AM
@desc:
'''
from src.Mongo_deploy import MongoConn
from src.common.common import is_cur_day,is_cur_month,is_cur_week
import time
# import pprint
from src.common.genTable import pop_path,beRead_path
import json
def update_be_read():

    # t1 = MongoConn('Beijing')
    t2 = MongoConn('Hong Kong')
    Be_read = []


    # timestamp = str(int(time.time()))

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
            Be_read.append(one_read)
            # json.dump(one_read, f)
            # f.write("\n")

            # 往表中插入这条数据
    t2.bulk_insert("be_read", Be_read)


#
def update_pop():
    with open(pop_path,'w+') as f:
        t2 = MongoConn('Hong Kong')
        pop_rank = []
        daily_rank = {}
        week_rank = {}
        month_rank = {}

        d_articleAidList = []
        w_articleAidList = []
        m_articleAidList = []
        article_item = {}
        be_read_collection = t2.get_collection('be_read')
        cur_timestamp = int(time.time())

        daily_rank["temporalGranularity"] = "daily"
        daily_rank["timestamp"] = cur_timestamp

        month_rank["temporalGranularity"] = "monthly"
        month_rank["timestamp"] = cur_timestamp

        week_rank["temporalGranularity"] = "weekly"
        week_rank["timestamp"] = cur_timestamp

        for be_read_item in be_read_collection.find():

            timestamp = int(be_read_item["timestamp"])
            article_item["readNum"] = be_read_item["readNum"]
            article_item["commentNum"] = be_read_item["commentNum"]
            article_item["agreeNum"] = be_read_item["agreeNum"]
            article_item["shareNum"] = be_read_item["shareNum"]
            article_item["aid"] = be_read_item["aid"]

            if is_cur_day(timestamp):

                d_articleAidList.append(article_item)

            if is_cur_week(timestamp):

                w_articleAidList.append(article_item)

            if is_cur_month(timestamp):

                m_articleAidList.append(article_item)

        daily_rank["articleList"] = d_articleAidList
        week_rank["articleList"] = w_articleAidList
        month_rank["articleList"] = m_articleAidList

        json.dump(daily_rank, f)
        f.write("\n")

        json.dump(week_rank, f)
        f.write("\n")
        json.dump(month_rank, f)
        f.write("\n")
        pop_rank.append(daily_rank)
        pop_rank.append(week_rank)
        pop_rank.append(month_rank)