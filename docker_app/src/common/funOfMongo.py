'''
@author: qujb
@contact: 15210825203@163.com
@file: funOfMongo.py
@time: 2019/6/6 上午12:32
@desc:
'''
import time
import operator
from src.common.genTable import ARTICLES_NUM
from random import random

from src.Mongo_deploy import MongoConn
from src.common.common import is_cur_month,is_cur_week,is_cur_day,stamp_2_str
from src.common.genTable import gen_an_user,gen_an_read

t1 = MongoConn("Beijing")
t2 = MongoConn("Hong Kong")

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

    # 先删除当前be_read表
    t2.get_collection("be_read").drop()
    Be_read1 = []
    Be_read2 = []

    # 这里根据读取read表和airticle 表生成be-read 表
    read_collection = t2.get_collection('read')
    article_collection = t2.get_collection('article')

    for article_item in article_collection.find():
        # print(type(item))
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
            # 这里三个list需要去重
            from functools import reduce
            func = lambda x, y: x if y in x else x + [y]
            one_read["readUidList"] = reduce(func, [[], ] + one_read["readUidList"])
            one_read["commentUidList"] = reduce(func, [[], ] + one_read["commentUidList"])
            one_read["agreeUidList"] = reduce(func, [[], ] + one_read["agreeUidList"])
            one_read["shareUidList"] = reduce(func, [[], ] + one_read["shareUidList"])
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

    # 删除旧表
    t2.get_collection("pop_rank").drop()
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

        #print(type(be_read_item))
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
    # upsert create if not exist
    t2.insert_document("pop_rank",daily_rank)
    t2.insert_document("pop_rank",week_rank)
    t2.insert_document("pop_rank",month_rank)


def register_user(t,id):
    import re

    if bool(re.search('[a-z]', id)):
        print('请输入纯数字的id')
        return 0
    while True:
        region = input('''所属地区
        1.北京
        2.香港
        ''')
        if region=='1':
            t = t1
        else:
            t = t2
        break
    doc = t.get_single_doc('user',{'uid':id})
    if doc is None:
        user = gen_an_user(int(id))
        user["region"] = t.region
        t.insert_document('user',user)
        return user
    else:
        return None

def validate_user(name):
    # 先到redis里找

    doc1 = t1.get_single_doc('user',{'name':name})
    doc2 = t2.get_single_doc('user', {'name': name})
    if doc1 is None:
        if doc2 is None:
            return None,None,False
        else:
            return doc2,t2,True
    else:
        return doc1,t1,True

def turn_2_user(t,name):

    print('以下是您的个人信息：')
    user_doc = t.get_single_doc('user',{'name':name})
    print('''
    用户id：{id}
    用户名：{name}
    性别：{sex}
    邮箱：{email}
    电话：{phone}
    所属区域：{region}
    创建时间：{time}
    '''.format(id=user_doc["uid"],name=user_doc["name"],sex=user_doc["gender"],email=user_doc["email"]
                ,phone=user_doc["phone"],region=user_doc["region"],time=stamp_2_str(int(user_doc["timestamp"]))))
    while True:
        selection = input('''
        1.热榜推荐
        2.随机推送
        3.文章搜索
        4.q退回主界面
        ''')
        if selection == '1':
            get_top5(t)
        elif selection == '2':
            article_title = "title" + str(int(random()*ARTICLES_NUM))
            show_article(t,article_title,name)
        elif selection == '3':
            article_title = input("选择要阅读的文章标题：(q回退)")
            if article_title == 'q':
                continue
            show_article(t,article_title,name)
        elif selection == 'q':
            return
        else:
            print("少年,请正常输入,不要为难为我")

def show_article(t,article_title,user_name):

    article_doc = t.get_single_doc("article",{"title":article_title})
    if article_doc is None:
        if t.region == "Beijing":
            article_doc = t2.get_single_doc("article",{"title":article_title})
        else:
            article_doc = t1.get_single_doc("article", {"title": article_title})
        if article_doc is None:
            print("查询不到相应文章,请重新输入！")
            return None
    aid = article_doc["aid"]

    read_item = gen_an_read(int(aid))
    read_item["aid"] = aid
    read_item["uid"] = t.get_single_doc('user',{'name':user_name})["uid"]
    t.insert_document("read",read_item)
    print('''
    文章信息：
    标题：{title} 类别：{category} 标签：{tags} 语言：{en}
    作者：{author}
    摘要：{abstract}
    正文：{content} 
    '''.format(title=article_doc["title"],category=article_doc["category"],tags=article_doc["articleTags"],
               en=article_doc["language"],author=article_doc["authors"],abstract=article_doc["abstract"],
               content=article_doc["text"]))
    return article_doc
def get_top5(t):

    daily = t.get_single_doc("pop_rank",{"temporalGranularity": "daily"})["articleList"]
    week = t.get_single_doc("pop_rank",{"temporalGranularity": "weekly"})["articleList"]
    month = t.get_single_doc("pop_rank", {"temporalGranularity": "monthly"})["articleList"]
    d_len = 5 if len(daily) >=5 else len(daily)
    w_len = 5 if len(week) >= 5 else len(week)
    m_len = 5 if len(month) >= 5 else len(month)
    print("最受欢迎阅读前五如下：")
    print("当日统计")
    for i in range(d_len):
        print('''
        书名：{id} 阅读量：{read} 评论量：{comment} 点赞数：{agree} 分享数：{share}
        '''.format(id=daily[i]["aid"],read=daily[i]["readNum"],comment=daily[i]["commentNum"],
                   agree=daily[i]["agreeNum"],share=daily[i]["shareNum"]))

    print("每周统计")
    for i in range(w_len):
        print('''
        书名：{id} 阅读量：{read} 评论量：{comment} 点赞数：{agree} 分享数：{share}
        '''.format(id=week[i]["aid"],read=week[i]["readNum"],comment=week[i]["commentNum"],
                   agree=week[i]["agreeNum"],share=week[i]["shareNum"]))

    print("当月统计")
    for i in range(m_len):
        print('''
        书名：{id} 阅读量：{read} 评论量：{comment} 点赞数：{agree} 分享数：{share}
        '''.format(id=month[i]["aid"],read=month[i]["readNum"],comment=month[i]["commentNum"],
                   agree=month[i]["agreeNum"],share=month[i]["shareNum"]))
# 提供给redis往mongo存入数据的接口
def R2M(r,name,o):
    if r.region == t1.region:
        t1.insert_document(name,o)
    else:
        t2.insert_document(name,o)