'''
@author: qujb
@contact: 15210825203@163.com
@file: mediator.py
@time: 2019/6/9 上午12:59
@desc: 这里放入mongo和redis交互的内容
'''
from src.common.funcOfRedis import validate_user as r_validate_user
from src.common.funOfMongo import validate_user as m_validate_user
from src.common.funOfMongo import turn_2_user as mturn_2_user
from src.common.funcOfRedis import turn_2_user as rturn_2_user
from src.common.funcOfRedis import get_top5 as rget_top5
from src.common.funOfMongo import get_top5 as mget_top5
from src.Mongo_deploy import MongoConn
from src.Redis_deploy import Redis
from src.common.funcOfRedis import save_2_redis
from src.common.funcOfRedis import r1,r2

def validate_user(name):
    # 首先去redis里找
    doc,r,flag = r_validate_user(name)
    if not flag:
        doc,t,flag = m_validate_user(name)
        # 向redis里插入这条数据
        if t.region == r1.region:
            save_2_redis(r1,name,doc)
        return t,flag
    else:
        return r,flag

def turn_2_user(conn,name):
    if isinstance(conn,Redis):
        rturn_2_user(conn,name)
    if isinstance(conn,MongoConn):
        mturn_2_user(conn,name)

def get_top5(conn):
    if isinstance(conn,Redis):
        rget_top5(conn)
    if isinstance(conn,MongoConn):
        mget_top5(conn)