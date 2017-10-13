import sys
from pymongo import MongoClient

sys.path.append("./resources/configs/")
from mongodbconfig import mongodb_config

mongo_client = MongoClient( mongodb_config['host'], mongodb_config['port'])
mongo_db_singhose = mongo_client[mongodb_config['db']] # set to your db name
mongo_collection_articles = mongo_db_singhose[mongodb_config['collection']] # set to you collection name