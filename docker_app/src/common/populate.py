'''
@author: qujb
@contact: 15210825203@163.com
@file: populate.py
@time: 6/3/19 4:36 AM
@desc:
'''
from src.Mongo_deploy import MongoConn
from src.common.common import *


# import pprint
# from src.common.genTable import pop_path,beRead_path
# import json
def update_be_read():

    t1 = MongoConn('Beijing')
    t2 = MongoConn('Hong Kong')
    generate_be_read(t1,t2)
    generate_be_read(t2,t1)


#
def update_pop():

    t1 = MongoConn('Beijing')
    t2 = MongoConn('Hong Kong')
    generate_pop(t1)
    generate_pop(t2)

