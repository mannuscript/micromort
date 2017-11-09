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
        self.collection = None
        self.urls_seen = None
        self.unique_index = None

    def process_item(self, item, pipeline):
        print item
        if item[self.unique_index] not in self.urls_seen:
            self.urls_seen.append(item[self.unique_index])
            return item
        else:
            raise DropItem("Duplicate news item found with article url {0}".format(item[self.unique_index]))

    def open_spider(self, spider):
        self.collection = spider.collection
        self.unique_index = spider.unique_index
        self.urls_seen = self.collection.distinct(self.unique_index)

    def close_spider(self, spider):
        self.client.close()


class MongoDBPipeline(object):

    def __init__(self):
        self.collection = None
        self.client = None

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        log.msg('Summary information is added to the database {0}'.format(item['article_url']))
        return item

    def open_spider(self, spider):
        self.collection = spider.collection
        self.client = spider.client

    def close_spider(self, spider):
        self.client.close()
