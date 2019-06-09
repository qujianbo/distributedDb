'''
@author: qujb
@contact: 15210825203@163.com
@file: funcOfRedis.py
@time: 2019/6/9 上午12:49
@desc:
'''
import json
from src.common.genTable import ARTICLES_NUM
from src.Redis_deploy import Redis
from src.common.genTable import gen_an_read
from random import random
from src.common.common import str_2_dict
from src.common.common import stamp_2_str
r1 = Redis('127.0.0.1',port=6379,db=0,region="Beijing")

r2 = Redis('127.0.0.1',port=6380,db=0,region="Hong Kong")

def save_2_redis(r,key,o):
    r.set(key,o)

def getFromRedis(r,key):
    return str_2_dict(r.get(key))

# 根据mongo的查询键设置为name
def validate_user(name):
    # 先到redis里找

    doc1 = getFromRedis(r1,name)
    doc2 = getFromRedis(r2,name)
    if doc1 is None:
        if doc2 is None:
            return None,None,False
        else:
            return doc2,r2,True
    else:
        return doc1,r1,True

def turn_2_user(t,name):

    print('以下是您的个人信息：')
    user_doc = getFromRedis(t,name)
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

# 这里如果read表的主键为“READ”+uid，存储article list
# 如果主键为“READ”+uid+aid，存储具体的内容
def show_article(t,article_title,user_name):

    article_doc = getFromRedis(t,article_title)
    if article_doc is None:
        if t.region == "Beijing":
            article_doc = getFromRedis(r2,article_title)
        else:
            article_doc = getFromRedis(r1,article_title)
        if article_doc is None:
            print("查询不到相应文章,请重新输入！")
            return
    aid = article_doc["aid"]

    read_item = gen_an_read(int(aid))
    read_item["aid"] = aid
    read_item["uid"] = getFromRedis(t,user_name)["uid"]
    main_key = "READ" + read_item["uid"] + aid
    main_key_ = "READ" + read_item["uid"]
    save_2_redis(t,main_key,read_item)
    t.lpush(main_key_,aid)

    print('''
    文章信息：
    标题：{title} 类别：{category} 标签：{tags} 语言：{en}
    作者：{author}
    摘要：{abstract}
    正文：{content} 
    '''.format(title=article_doc["title"],category=article_doc["category"],tags=article_doc["articleTags"],
               en=article_doc["language"],author=article_doc["authors"],abstract=article_doc["abstract"],
               content=article_doc["text"]))

# 主键设置为Key: “Popular_Rank” + temporalGranularity
def get_top5(t):

    query_keyD = "Popular_Rank" + "daily"
    query_keyW = "Popular_Rank" + "weekly"
    query_keyM = "Popular_Rank" + "monthly"
    daily = getFromRedis(t,query_keyD)
    if daily is None:
        # 这是不允许的，除非mongo里没有
        print("暂无热榜")
    week = getFromRedis(t,query_keyW)
    month = getFromRedis(t,query_keyM)

    print("最受欢迎阅读前五如下：")
    print("当日统计")
    for i in range(5):
        print('''
        书名：{id} 阅读量：{read} 评论量：{comment} 点赞数：{agree} 分享数：{share}
        '''.format(id=daily[i]["aid"],read=daily[i]["readNum"],comment=daily[i]["commentNum"],
                   agree=daily[i]["agreeNum"],share=daily[i]["shareNum"]))

    print("每周统计")
    for i in range(5):
        print('''
        书名：{id} 阅读量：{read} 评论量：{comment} 点赞数：{agree} 分享数：{share}
        '''.format(id=week[i]["aid"],read=week[i]["readNum"],comment=week[i]["commentNum"],
                   agree=week[i]["agreeNum"],share=week[i]["shareNum"]))

    print("当月统计")
    for i in range(5):
        print('''
        书名：{id} 阅读量：{read} 评论量：{comment} 点赞数：{agree} 分享数：{share}
        '''.format(id=month[i]["aid"],read=month[i]["readNum"],comment=month[i]["commentNum"],
                   agree=month[i]["agreeNum"],share=month[i]["shareNum"]))