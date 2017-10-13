'''
Created on Aug 8, 2014

@author: christian
'''

import time
import json
import feedparser
import os
from pymongo import MongoClient
import sys

sys.path.insert(0, '../resources/configs')
#Import project files
from mongodbconfig import mongodb_config


class NewsFeedCrawler:

    def __init__(self, feed_urls_file_name):
        self._createMongoDbAndCollection()
        self.rss_feed_urls = []
        self._init_feed_urls(feed_urls_file_name)
    
    def _createMongoDbAndCollection(self):        
        self.mongo_client = MongoClient( mongodb_config['host'], mongodb_config['port'])
        # set to your db name
        self.mongo_db_singhose = self.mongo_client[mongodb_config['db']] 
        # set to you collection name
        self.mongo_collection_articles = self.mongo_db_singhose[mongodb_config['collection']] 
        #Create a unique index on link, as rss feed will be fetching the same 
        # url again and again.
        self.mongo_collection_articles.create_index("link", unique=True)
            
    def start_crawling(self):
        self._fetch_feeds()
            
        
    def _init_feed_urls(self, feed_urls_file_name):
        with open(feed_urls_file_name, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith("#"):
                    continue
                url = line.split('\t')[0]
                self.rss_feed_urls.append(url)


    def _fetch_feeds(self):
        print '_fetch_feeds', self.rss_feed_urls
        for rss_feed_url in self.rss_feed_urls:
            self._fetch_feed(rss_feed_url)
    
    
    def _fetch_feed(self, feed_url):
        print 'FETCH:', feed_url 
        entries = feedparser.parse(feed_url)['entries']
        for entry in entries:
            print entry
            #continue
            # date format conversation needed; otherwise error
            entry_json_string = json.dumps(entry, default=self._to_json)
            entry_json = json.loads(entry_json_string)
            try:
                self.mongo_collection_articles.update(
                    {
                        "link" : entry_json["link"]
                    }, 
                    entry_json, True)
            except Exception as ex:
                #logging.exception("Something awful happened!")
                print "ERROR----------------"
                import traceback
                traceback.print_exc()
                pass # ignore if insert fails (duplicate)
                
    def _to_json(self, python_object):
        if isinstance(python_object, time.struct_time):
            return {'__class__': 'time.asctime',
                    '__value__': time.asctime(python_object)}
        if isinstance(python_object, bytes):
            return {'__class__': 'bytes',
                    '__value__': list(python_object)}
        raise TypeError(repr(python_object) + ' is not JSON serializable')

if __name__ == "__main__":
    file_path = os.getcwd() + '/news-sites-rss-feed-links-sg.txt'
    news_feed_crawler = NewsFeedCrawler(file_path)
    news_feed_crawler.start_crawling()