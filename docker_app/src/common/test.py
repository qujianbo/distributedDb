# from src.Mongo_deploy import MongoConn
# from src.Mongo_deploy import MongoDB
# import pprint
# conn = MongoConn('Hong Kong')
# db = MongoDB(conn.db)
# collection = db.get_collection('article')
# # print(collection)
# for item in collection.find():
#     pprint.pprint(item)
# # print(collection.find())
#
#
# print(db.get_count('article',''))
# iter_list = db.get_posts('article', '')
# for iter in iter_list:
#     pprint.pprint(iter)
# import os
# cur_path = os.path.abspath(os.path.dirname(__file__))
# # dir_path = os.path.dirname(cur_path)
# # print(cur_path, dir_path)
# user_path = os.path.dirname(os.path.dirname(cur_path)) + '/dat/user.dat'
# print(user_path)
# from src.common.populate import update_pop
# from src.common.populate import update_be_read
# update_be_read()
# update_pop()

from functools import reduce
list = ['5','4','5','5']
func = lambda x, y: x if y in x else x + [y]
list = reduce(func, [[], ] + list)
for i in list:
    print(i)