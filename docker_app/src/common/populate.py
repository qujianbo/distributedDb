'''
@author: qujb
@contact: 15210825203@163.com
@file: populate.py
@time: 6/3/19 4:36 AM
@desc:
'''

from src.common.funOfMongo import *

# import pprint
# from src.common.genTable import pop_path,beRead_path
# import json
def update_be_read():

    generate_be_read(t1,t2)
    generate_be_read(t2,t1)

#
def update_pop():
    generate_pop(t1)
    generate_pop(t2)

