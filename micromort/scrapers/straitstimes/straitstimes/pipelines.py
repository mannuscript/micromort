# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo
from micromort.resources.configs.mongodbconfig import mongodb_config
from scrapy import log
from scrapy.exceptions import DropItem


class DuplicateNewsPipeline(object):
    def __init__(self):
        self.client = None
        self.collection = None
        self.db = None
        self.urls_seen = None
        self.MONGODB_URL = mongodb_config['host']
        self.MONGODB_PORT = mongodb_config['port']
        self.MONGODB_DB = mongodb_config['db']
        self.MONGODB_COLLECTION = mongodb_config['collection']

    def process_item(self, item, pipeline):
        print item
        if item['article_url'] not in self.urls_seen:
            self.urls_seen.append(item['article_url'])
            return item
        else:
            raise DropItem("Duplicate news item found with article url {0}".format(item['article_url']))

    def open_spider(self, spider):
        MONGODB_URL = self.MONGODB_URL
        MONGODB_PORT = int(self.MONGODB_PORT)
        MONGODB_DB = self.MONGODB_DB
        MONGODB_COLLECTION = self.MONGODB_COLLECTION
        self.client = pymongo.MongoClient(MONGODB_URL, MONGODB_PORT)
        self.db = self.client[MONGODB_DB]
        self.collection = self.db[MONGODB_COLLECTION]
        self.urls_seen = self.collection.distinct('article_url')

    def close_spider(self, spider):
        self.client.close()


class MongoDBPipeline(object):

    def __init__(self):
        self.client = None
        self.collection = None
        self.db = None
        self.MONGODB_URL = mongodb_config['host']
        self.MONGODB_PORT = mongodb_config['port']
        self.MONGODB_DB = mongodb_config['db']
        self.MONGODB_COLLECTION = mongodb_config['collection']

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        log.msg('Summary information is added to the database {0}'.format(item['article_url']))
        return item

    def open_spider(self, spider):
        MONGODB_URL = self.MONGODB_URL
        MONGODB_PORT = int(self.MONGODB_PORT)
        MONGODB_DB = self.MONGODB_DB
        MONGODB_COLLECTION = self.MONGODB_COLLECTION
        self.client = pymongo.MongoClient(MONGODB_URL, MONGODB_PORT)

        self.db = self.client[MONGODB_DB]
        self.collection = self.db[MONGODB_COLLECTION]

    def close_spider(self, spider):
        self.client.close()

