import os
import datetime
from bson.objectid import ObjectId

from micromort.share_metrics.shares_getter import SharesGetter
from micromort.share_metrics.newsfeedcrawler import NewsFeedCrawler
from micromort.scrapers.newspaper_scraper import Newspaper_scraper
from micromort.utils.logger import logger
from micromort.data_stores.mongodb import getConnection

class Pipeline:
    def __init__(self):
        file_path = os.getcwd() + '/share_metrics/news-sites-rss-feed-links-sg.txt'
        self.news_feed_crawler = NewsFeedCrawler(file_path)
        self.share_getter = SharesGetter()
        self.scraper = Newspaper_scraper()
        self.mongoClient = getConnection("rss", "articles")
        pass

    def getUrlsToCrawl(self, d=1):
        now = datetime.datetime.now()
        today = datetime.datetime(now.year, now.month, now.day)
        from_date = today + datetime.timedelta(days=-d)
        to_date = today + datetime.timedelta(days=-d + 1)
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
        self.news_feed_crawler.start_crawling()
        urls = self.getUrlsToCrawl(day)
        self.share_getter.main(urls)
        self.scraper.main(urls)


    
if __name__ == "__main__":
    pipeline = Pipeline()
    pipeline.run(1)