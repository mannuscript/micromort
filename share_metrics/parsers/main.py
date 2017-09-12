'''
Created on Sep 8, 2017

@author: chris
'''


import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from pymongo import MongoClient
import datetime
from bson.objectid import ObjectId

from straitstimes import get_straitstimes_a2a_counts

class Parser:

    def __init__(self):
        self.mongoClient = self.__getMongoClient()
        self.driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
        self.driver.set_page_load_timeout(45)

    def __getMongoClient(self):        
        mongo_client = MongoClient('localhost', 27017)
        mongo_db_singhose = mongo_client['rss'] # set to your db name
        mongo_collection_articles = mongo_db_singhose['articles'] # set to you collection name
        return mongo_collection_articles
    
    #
    # List of newswebsite support:
    # straitstimes, ...
    #
    def __get_shares(self, article_url):
        try:
            self.driver.get(article_url);
        except TimeoutException:
            self.driver.execute_script("window.stop();")
            print "Page load time out -- try again later"
            return None
        return get_straitstimes_a2a_counts(self.driver.page_source, "Facebook")

    #Get urls from mongodb which were inserted d (default 15) days ago
    def __getUrlsToCrawl(self, d=15):
        
        now = datetime.datetime.now()
        today = datetime.datetime(now.year, now.month, now.day)
        from_date = today + datetime.timedelta(days=-d)
        to_date = today + datetime.timedelta(days=-d+1)
        from_id = ObjectId.from_datetime(from_date)
        to_id = ObjectId.from_datetime(to_date)

        urls = []
        articles = self.mongoClient.find({"_id": {"$gt": from_id, "$lt" : to_id}})
        for article in articles:
            urls.append(article["link"])
        return urls;
    
    def dumpIntoMysql():
        print "INIT"

    def main(self):
        urls = self.__getUrlsToCrawl(0)
        urls_share_map = {}
        for url in urls:
            urls_share_map[url] = self.__get_shares(url);
            print url, urls_share_map[url]

        return urls


if __name__ == "__main__":
    parser = Parser()
    print parser.main();
    #print get_shares("http://www.straitstimes.com/lifestyle/anger-over-influencers-sponsored-wedding", "straitstimes")