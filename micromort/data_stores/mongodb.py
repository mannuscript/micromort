from pymongo import MongoClient
from micromort.resources.configs.mongodbconfig import mongodb_config

mongo_client = MongoClient(mongodb_config['host'], mongodb_config['port'])
mongo_db_singhose = mongo_client[mongodb_config['db']]  # set to your db name
mongo_collection_articles = mongo_db_singhose[mongodb_config['collection']]  # set to you collection name

# Create a unique index on link, as rss feed will be fetching the same
# url again and again.
mongo_collection_articles.create_index("link", unique=True)
