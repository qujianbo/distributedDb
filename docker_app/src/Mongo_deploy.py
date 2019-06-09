import pymongo
import os
import datetime
# Connection to Mongo DB

MONGODB_CONFIG = {
    # 'host': ['192.168.0.106','192.168.0.105'],
    'db_name': ['db_bj', 'db_hk'],
    'username': None,
    'password': None
}


class MongoConn():

	def __init__(self, region):
		if region == "Beijing":
			self.conn = pymongo.MongoClient(host='127.0.0.1', port=27017)
			self.db = self.conn['db_bj']

		elif region == "Hong Kong":
			self.conn = pymongo.MongoClient(host='127.0.0.1', port=27016)
			self.db = self.conn['db_hk']

		self.region = region
	def get_collection(self, collection_name):
		return self.db[collection_name]

	def insert_document(self, collection_name, post):
		insert_result = self.db[collection_name].insert_one(post)
		return insert_result

	# get the first document from the collection
	def get_single_doc(self, collection_name, query=''):
		if query == '':
			return self.db[collection_name].find_one()
		else:
			return self.db[collection_name].find_one(query)

	def bulk_insert(self, collection_name, new_posts):
		result = self.db[collection_name].insert_many(new_posts)
		return result

	# Querying for More Than One Document
	def get_posts(self, collection_name, query=''):
		if query == '':
			cursor_iter = self.db[collection_name].find()
		else:
			cursor_iter = self.db[collection_name].find(query)
		return cursor_iter

	def get_count(self, collection_name, query=''):
		if query == '':
			return self.db[collection_name].count_documents({})
		else:
			return self.db[collection_name].count_documents(query)

	# def increase_one_doc(self,collection_name,field=''):
	# 	if field == '':
	# 		return
	# 	else:
	# 		self.db[collection_name].find_one_and_update({'$inc': {field: 1})