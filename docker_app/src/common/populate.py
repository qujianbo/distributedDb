'''
@author: qujb
@contact: 15210825203@163.com
@file: populate.py
@time: 6/3/19 4:36 AM
@desc:
'''
from src.Mongo_deploy import MongoConn
import time
import pprint
from src.common.genTable import pop_path
import json
def update_pop():



    # t1 = MongoConn('Beijing')
    t2 = MongoConn('Hong Kong')
    Be_read = []


    timestamp = str(int(time.time()))

    # 这里根据读取read表和airticle 表生成be-read 表
    read_collection = t2.get_collection('read')
    article_collection = t2.get_collection('article')
    with open(pop_path, "w+") as f:
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

            one_read["timestamp"] = timestamp

            one_read["readUidList"] = []
            one_read["commentUidList"] = []
            one_read["agreeUidList"] = []
            one_read["shareUidList"] = []

            for single_read in list(read_item):

                if single_read:

                    one_read["aid"] = single_read["aid"]

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
                json.dump(one_read, f)
                f.write("\n")

    # f.write()
    # 往表中插入这条数据
    # t2.bulk_insert("Be_read", Be_read)