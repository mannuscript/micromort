import os
import datetime
from bson.objectid import ObjectId

from micromort.share_metrics.shares_getter import SharesGetter
from micromort.share_metrics.newsfeedcrawler import NewsFeedCrawler
from micromort.scrapers.newspaper_scraper import Newspaper_scraper
from micromort.utils.logger import logger
from micromort.data_stores.mongodb import getConnection
from micromort.resources.configs.mongodbconfig import mongodb_config
from micromort.models.trained_models.svm_mean_embeddings import Classifier, MeanEmbeddingVectorizer

class Pipeline:
    def __init__(self):
        file_path = os.getcwd() + '/share_metrics/news-sites-rss-feed-links-sg.txt'
        self.news_feed_crawler = NewsFeedCrawler(file_path)
        self.share_getter = SharesGetter()
        self.scraper = Newspaper_scraper(True)
        mongo_db = mongodb_config['dbs']['rss']['db']
        collection =  mongodb_config['dbs']['rss']['collection']
        self.mongoClient = getConnection(mongo_db, collection)
        pass

    def getUrlsToCrawl(self, d=1):
        now = datetime.datetime.now()
        from_date = now + datetime.timedelta(days=-d)
        to_date = now + datetime.timedelta(days=-d + 1)
        from_id = ObjectId.from_datetime(from_date)
        to_id = ObjectId.from_datetime(to_date)

        urls = []
        logger.info("Getting urls from " + str(from_date) + " to " + str(to_date))
        articles = self.mongoClient.find({"_id": {"$gt": from_id, "$lt": to_id}})
        for article in articles:
            urls.append(article["link"])
        return urls


    """
        Run the pipeline:
        1. RSS feeder, to get the latest news articles.
        2. shares_getter to get the likes/shares for urls for last one hour.
        3. news_paper scarpper to get the news articles
        4. (TODO): Predict the classes of the news articles
    """
    def run(self, day):
        logger.info("------------- Starting RSS feeder -----------")
        self.news_feed_crawler.start_crawling()
        logger.info("------------- Getting URLS to work upon -----------")
        urls = self.getUrlsToCrawl(day)
        logger.info("------------- Get number of shares/likes -----------")
        self.share_getter.main(urls)
        logger.info("------------- Scrape and predict worry -----------")
        self.scraper.main(urls)


    
if __name__ == "__main__":
    pipeline = Pipeline()
    pipeline.run(1)