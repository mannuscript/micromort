"""
Created on Aug 8, 2014

@author: christian
"""

import time
import json
import feedparser
import os
from pymongo import MongoClient
import sys


from micromort.utils.logger import logger
from micromort.data_stores.mongodb import getConnection


class NewsFeedCrawler:
    def __init__(self, feed_urls_file_name):
        self.mongo_collection_articles = getConnection("rss", "articles")
        self.rss_feed_urls = []
        self._init_feed_urls(feed_urls_file_name)
        logger.info("Going to work on " + str(len(self.rss_feed_urls)) + " rss feeds")

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
        for rss_feed_url in self.rss_feed_urls:
            logger.info("Fetching from: " + rss_feed_url)
            self._fetch_feed(rss_feed_url)

    def _fetch_feed(self, feed_url):
        entries = feedparser.parse(feed_url)['entries']
        for entry in entries:
            logger.debug("For entry: " + str(entry))
            # date format conversation needed; otherwise error
            entry_json_string = json.dumps(entry, default=self._to_json)
            entry_json = json.loads(entry_json_string)
            try:
                logger.debug("Dumping following key value in mongo: " + str(entry_json["link"]) + str(entry_json))
                self.mongo_collection_articles.update(
                    {
                        "link": entry_json["link"]
                    },
                    entry_json, True)
            except Exception as ex:
                # logging.exception("Something awful happened!")
                logger.error("ERROR----------------")
                import traceback
                traceback.print_exc()
                pass  # ignore if insert fails (duplicate)

    @staticmethod
    def _to_json(python_object):
        if isinstance(python_object, time.struct_time):
            return {'__class__': 'time.asctime',
                    '__value__': time.asctime(python_object)}
        if isinstance(python_object, bytes):
            return {'__class__': 'bytes',
                    '__value__': list(python_object)}
        raise TypeError(repr(python_object) + ' is not JSON serializable')


if __name__ == "__main__":
    file_path = os.getcwd() + '/share_metrics/news-sites-rss-feed-links-sg.txt'
    news_feed_crawler = NewsFeedCrawler(file_path)
    news_feed_crawler.start_crawling()
