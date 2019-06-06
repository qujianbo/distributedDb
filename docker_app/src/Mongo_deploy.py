import pymongo
import os
import datetime
# Connection to Mongo DB

MONGODB_CONFIG = {
    'host': '127.0.0.1',
    'db_name': ['db_bj', 'db_hk'],
    'username': None,
    'password': None
}

post = {"author": "Mike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow()}

# class MongoDB():
#
# 	def __init__(self, db):
# 		self.db = db
# 		self.posts = db.posts



class MongoConn():

	def __init__(self, region):
		if region == "Beijing":
			self.conn = pymongo.MongoClient(host=MONGODB_CONFIG['host'], port=27017)
			self.db = self.conn['db_bj']
		elif region == "Hong Kong":
			self.conn = pymongo.MongoClient(host=MONGODB_CONFIG['host'], port=27016)
			self.db = self.conn['db_hk']

		self.posts = self.db.posts

	def get_collection(self, collection_name):
		return self.db[collection_name]

	def insert_document(self, collection_name, post):
		insert_result = self.posts[collection_name].insert_one(post)
		return insert_result

	# get the first document from the posts collection
	def get_single_doc(self, collection_name, query=''):
		if query == '':
			return self.posts[collection_name].find_one()
		else:
			return self.posts[collection_name].find_one(query)

	def bulk_insert(self, collection_name, new_posts):
		result = self.posts[collection_name].insert_many(new_posts)
		return result

	# Querying for More Than One Document
	def get_posts(self, collection_name, query=''):
		if query == '':
			cursor_iter = self.posts[collection_name].find()
		else:
			cursor_iter = self.posts[collection_name].find(query)
		return cursor_iter

	def get_count(self, collection_name, query=''):
		if query == '':
			return self.posts[collection_name].count_documents({})
		else:
			return self.posts[collection_name].count_documents(query)

	def get_dbnames(self):
		return self.conn.database_names()

