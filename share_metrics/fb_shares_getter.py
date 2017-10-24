'''
Refer git meta data for creation details :)
'''

import requests
import urllib
import sys
import datetime
import json
from bson.objectid import ObjectId

sys.path.append("./data_stores")
from mongodb import mongo_collection_articles
from mysql import db, cursor
# Get logger from utils
sys.path.append("./utils/")
from logger import logger
sys.path.append("./resources/configs")
from share_metricconfig import share_metricconfig

class FBSharesGetter:
    def __init__(self):
        self.mongoClient = mongo_collection_articles
        self.db = db
        self.cursor = cursor
    
    def __getUrlsToCrawl(self, d=-1):
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

    def getFBData(self, url):
        url = urllib.quote(url)
        access_token = share_metricconfig["app_access_token"]
        api = share_metricconfig["fb_graph_api"].format(access_token, url)
        headers = share_metricconfig["headers"]
        r = requests.get(api, headers=headers)
        return r
    
    def __get_shares(self, url):
        res = self.getFBData(url)
        if(res and res.status_code == 200):
            try:
                return json.loads(res.text)["og_object"]["engagement"]["count"]
            except Exception as ex:
                logger.error("Failed to load count for url: " + url)
                return -1
        else:
            return -1

    def main(self):
        urls = self.__getUrlsToCrawl(00)
        
        logger.info(" Main function called, going to work on " \
                     + str(len(urls)) + " url(s)")
        logger.debug(" list of urls: " + str(urls))

        for url in urls:
            count = self.__get_shares(url)
            logger.info("count for url: " + url + " is: " + str(count))
            self.dumpIntoMysql(url, count, "Facebook")
            #print url, count

    def dumpIntoMysql(self, url, count, socialMediaChannel):
        #Pain of normalization: run 2 insert query:
        #insert into article_urls and get the insert id
        self.cursor.execute("""INSERT IGNORE INTO article_urls(url) values(%s)""", [url])
        #insert into article_social_media_shares
        self.cursor.execute(
            """INSERT IGNORE INTO article_social_media_shares(url_id, social_media_channel, counts)
             values(%s, %s, %s)""",[self.db.insert_id(), socialMediaChannel, count])


if __name__ == "__main__":
    ob = FBSharesGetter()
    # counter = 0;
    # while(True):
    #     res = ob.getFBData("http://www.straitstimes.com/sport/football/football-vialli-says-england-struggle-to-handle-pressure")
    #     #"https://stackoverflow.com/questions/5607551/how-to-urlencode-a-querystring-in-python"
    #     print "res: ", res.text 
    #     if(200 != res.status_code):
    #         break
    #     counter = counter + 1;
    #     print counter
    ob.main()

