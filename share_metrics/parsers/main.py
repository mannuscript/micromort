'''
Created on Sep 8, 2017

@author: chris
'''


import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from pymongo import MongoClient
import MySQLdb
import datetime
from bson.objectid import ObjectId
import sys

#Add configs dir into system path to be able to include the configs
##You shld run it from one upper directory.
sys.path.insert(0, '../resources/configs')
#Import project files
from straitstimes import get_straitstimes_a2a_counts
from mysqlconfig import mysql_config
from mongodbconfig import mongodb_config

class Parser:

    def __init__(self):
        #Start mongodb client
        self.mongoClient = self.__getMongoClient()
        self.driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
        self.driver.set_page_load_timeout(45)

        #Start mysql client
        self.db=MySQLdb.connect(
                host=mysql_config["host"],
                db=mysql_config["db"],
                read_default_file="~/.my.cnf")
        self.db.autocommit(True)
        self.cursor = self.db.cursor()

    def __getMongoClient(self):
        mongo_client = MongoClient( mongodb_config['host'], mongodb_config['port'])
        mongo_db_singhose = mongo_client[mongodb_config['db']] # set to your db name
        mongo_collection_articles = mongo_db_singhose[mongodb_config['collection']] # set to you collection name
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
    
    def dumpIntoMysql(self, url, count, socialMediaChannel):
        #Pain of normalization: run 2 insert query:
        #insert into article_urls and get the insert id
        self.cursor.execute("""INSERT IGNORE INTO article_urls(url) values(%s)""",[url])
        #insert into article_social_media_shares
        self.cursor.execute(
            """INSERT IGNORE INTO article_social_media_shares(url_id, social_media_channel, counts)
             values(%s, %s, %s)""",[self.db.insert_id(), socialMediaChannel, count])
        


    def main(self):
        urls = self.__getUrlsToCrawl(1)
        for url in urls:
            count = self.__get_shares(url)
            self.dumpIntoMysql(url, count, "Facebook")
            #print url, count
        #have to call the the close function to kill phantomjs process
        self.driver.quit()
        return urls


if __name__ == "__main__":
    parser = Parser()
    parser.main();
    #print get_shares("http://www.straitstimes.com/lifestyle/anger-over-influencers-sponsored-wedding", "straitstimes")