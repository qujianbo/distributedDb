import json
from src.Mongo_deploy import MongoConn
from src.common.genTable import user_path,article_path,read_path

t1 = MongoConn("Beijing")
t2 = MongoConn("Hong Kong")
user_region = {}
with open(user_path, "r") as f:
    for line in f.readlines():
        user_dict = json.loads(line)
        # print(user_dict)
        if user_dict['region'] == 'Beijing':

            t1.get_collection('user').insert(user_dict)
        else:
            t2.get_collection('user').insert(user_dict)
        user_region[user_dict['uid']] = user_dict['region']

with open(article_path, "r") as f:
    for line in f.readlines():
        article_dict = json.loads(line)

        if article_dict['category'] == 'technology':
            t2.get_collection('article').insert(article_dict)
        else:
            t1.get_collection('article').insert(article_dict)
            t2.get_collection('article').insert(article_dict)

with open(read_path, "r") as f:
    for line in f.readlines():
        read_dict = json.loads(line)

        if user_region[read_dict['uid']] == 'Beijing':
            t1.get_collection('read').insert(read_dict)
        else:
            t2.get_collection('read').insert(read_dict)

f.close()