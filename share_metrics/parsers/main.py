'''
Created on Sep 8, 2017

@author: chris
'''


import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import datetime
from bson.objectid import ObjectId
import sys
import os

#Import project files
from straitstimes import get_straitstimes_a2a_counts
from channelnewsasia import get_shares_counts as channelnewsasia_share_counts

# Get data stores
sys.path.append("./data_stores")
from mysql import db, cursor
from mongodb import mongo_collection_articles

# Get logger from utils
sys.path.append("./utils/")
from logger import logger


class Parser:

    def __init__(self):
        #Start mongodb client
        self.mongoClient = mongo_collection_articles
        self.driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
        self.driver.set_page_load_timeout(45)
        
        self.db = db
        self.cursor = cursor
    
    #
    # List of newswebsite support:
    # straitstimes, ...
    #
    def __get_shares(self, article_url):
        try:
            self.driver.get(article_url)
        except TimeoutException:
            self.driver.execute_script("window.stop();")
            print "Page load time out -- try again later"
            return None
        
        if "http://www.straitstimes.com" in url:
            caller = get_straitstimes_a2a_counts
        else if "http://www.channelnewsasia.com" in url:
            caller = channelnewsasia_share_counts
        else:
            caller = self.default_caller

        return caller(article_url, self.driver.page_source, "Facebook")

    def default_caller(url, source, media):
        logger.error("Parser not found :O for url: ", url)

    #Get urls from mongodb which were inserted d (default 15) days ago
    def __getUrlsToCrawl(self, d=1):
        
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
    
    def dumpIntoMysql(self, url, count, socialMediaChannel):
        #Pain of normalization: run 2 insert query:
        #insert into article_urls and get the insert id
        self.cursor.execute("""INSERT IGNORE INTO article_urls(url) values(%s)""", [url])
        #insert into article_social_media_shares
        self.cursor.execute(
            """INSERT IGNORE INTO article_social_media_shares(url_id, social_media_channel, counts)
             values(%s, %s, %s)""",[self.db.insert_id(), socialMediaChannel, count])
        

    def main(self):
        urls = self.__getUrlsToCrawl(0)
        
        logger.info(" Main function called, going to work on " \
                     + str(len(urls)) + " url(s)")
        logger.debug(" list of urls: " + str(urls))

        for url in urls:
            count = self.__get_shares(url)
            logger.info("count for url: " + url + " is: " + str(count))
            self.dumpIntoMysql(url, count, "Facebook")
            #print url, count
        #we must call the quite function to kill phantomjs process
        self.driver.quit()
        return urls


if __name__ == "__main__":
    parser = Parser()
    #parser.main();
    print get_shares("http://www.straitstimes.com/lifestyle/anger-over-influencers-sponsored-wedding", "straitstimes")