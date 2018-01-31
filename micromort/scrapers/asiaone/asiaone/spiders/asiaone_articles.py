import scrapy
from micromort.resources.configs.mongodbconfig import mongodb_config
from micromort.scrapers.asiaone.asiaone.items import AsiaoneArticlesItem
import pymongo
import logging
import os
from scrapy.utils.log import configure_logging

import micromort.constants as constants
PATHS = constants.PATHS
LOGS_DIR = os.path.join(PATHS['LOGS_DIR'], 'asiaone_spider')
from newspaper import Article


class AsiaoneNewsArticles(scrapy.Spider):
    name = 'asiaone_articles'
    allowed_domains = ['asiaone.com']
    asiaone_base_url = 'http://asiaone.com'
    custom_settings = {
        'ITEM_PIPELINES': {
            'micromort.scrapers.asiaone.asiaone.pipelines.DuplicateNewsPipeline': 100,
            'micromort.scrapers.asiaone.asiaone.pipelines.MongoDBPipeline': 200,
        }
    }

    configure_logging(settings={
        'LOG_LEVEL': 'INFO'
    })
    logging.basicConfig(
        filename=os.path.join(LOGS_DIR, 'log.txt'),
        level=logging.INFO,
        filemode='a'
    )

    def __init__(self, *args, **kwargs):
        self.MONGODB_URL = mongodb_config['host']
        self.MONGODB_PORT = mongodb_config['port']
        self.MONGODB_DB = mongodb_config['db']
        self.ARTICLE_COLLECTION = mongodb_config['asiaone_article_collection']
        self.HEADLINE_COLLECTION = mongodb_config['asiaone_headlines_collection']
        self.client = pymongo.MongoClient(self.MONGODB_URL, self.MONGODB_PORT)
        self.db = self.client[self.MONGODB_DB]
        self.collection = self.db[self.ARTICLE_COLLECTION]
        self.headlines_collection = self.db[self.HEADLINE_COLLECTION]
        self.article_urls = self.headlines_collection.distinct('article_url')
        self.unique_index = 'article_url'  # used to check the duplicates in the collection
        super(AsiaoneNewsArticles, self).__init__(*args, **kwargs)

    def parse(self, response):
        article = Article(response.url)

        article.download()
        article.parse()
        article.nlp()

        text = article.text
        date = article.publish_date
        url = response.url
        summary = article.summary
        if date:
            date_string = str(date.year) + "-" + str(date.month) + "-" + str(date.day)

        if text and date:
            item = AsiaoneArticlesItem(
                article_text=text,
                article_url=url,
                article_summary=summary,
                article_date=date_string
            )

            yield item

    def start_requests(self):
        """
        This will generate the urls from mongodb to scrape the main article page
        """
        for url in self.article_urls:
            url = self.asiaone_base_url + '/' + url
            yield scrapy.http.Request(url, callback=self.parse)
