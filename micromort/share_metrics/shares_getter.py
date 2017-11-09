"""
Refer git meta data for creation details :)
"""

import requests
import urllib
import datetime
import json
from bson.objectid import ObjectId

from micromort.data_stores.mongodb import mongo_collection_articles
from micromort.data_stores.mysql import db, cursor
from micromort.utils.logger import logger
from micromort.resources.configs.share_metricconfig import share_metricconfig


class SharesGetter:
    def __init__(self):
        self.mongoClient = mongo_collection_articles
        self.db = db
        self.cursor = cursor

    def __getUrlsToCrawl(self, d=-1):
        now = datetime.datetime.now()
        today = datetime.datetime(now.year, now.month, now.day)
        from_date = today + datetime.timedelta(days=-d)
        to_date = today + datetime.timedelta(days=-d + 1)
        from_id = ObjectId.from_datetime(from_date)
        to_id = ObjectId.from_datetime(to_date)

        urls = []
        articles = self.mongoClient.find({"_id": {"$gt": from_id, "$lt": to_id}})
        for article in articles:
            urls.append(article["link"])
        return urls

    @staticmethod
    def getFBData(url):
        url = urllib.quote(url)
        access_token = share_metricconfig["app_access_token"]
        api = share_metricconfig["fb_graph_api"].format(access_token, url)
        headers = share_metricconfig["headers"]
        r = requests.get(api, headers=headers)
        return r

    def get_linkedIn_shares(self, url):
        res = self.__getLinkedInData(url)
        if res and res.status_code == 200:
            try:
                return json.loads(res.text)["count"]
            except Exception as ex:
                logger.exception("Failed to load count for url: " + url)
                return -1
        else:
            return -1

    @staticmethod
    def __getLinkedInData(url):
        api = share_metricconfig["linkedIn_share_api"].format(url)
        return requests.get(api)

    def __get_fb_shares(self, url):
        res = self.getFBData(url)
        if res and res.status_code == 200:
            try:
                return json.loads(res.text)["og_object"]["engagement"]["count"]
            except Exception as ex:
                logger.error("Failed to load count for url: " + url)
                return -1
        else:
            return -1

    def main(self):
        urls = self.__getUrlsToCrawl(1)

        logger.info(" Main function called, going to work on " \
                    + str(len(urls)) + " url(s)")
        logger.debug(" list of urls: " + str(urls))

        for url in urls:
            # Get fb count
            count = self.__get_fb_shares(url)
            logger.info("facebook shares for url: " + url + " is: " + str(count))
            self.dumpIntoMysql(url, count, "Facebook")
            # Get linkedin counts
            count = self.get_linkedIn_shares(url)
            logger.info("linkedin shares for url: " + url + " is: " + str(count))
            self.dumpIntoMysql(url, count, "LinkedIn")

    def dumpIntoMysql(self, url, count, socialMediaChannel):
        # Pain of normalization: run 2 insert query:
        # insert into article_urls and get the insert id
        try:
            """
                Ok, Next few steps are going to be a little confusing... you 
                should grab some popcorn and sit tight!

                We first do an insert ignore into article_urls, as
                no point of inserting same url twice.
                Then use LAST_INSERT_ID to get the "last insert id" (obviously),
                But consider the case when insert was ignored, 
                there were no insert hence no Last_insert_id
                
                Now according to this fellow:
                https://stackoverflow.com/questions/6291405/mysql-after-insert-ignore-get-primary-key

                LAST_INSERT_ID would be zero for ignored case,
                Bingo! just do a select if you find this case.
            """

            self.cursor.execute("""INSERT IGNORE INTO article_urls(url) values(%s)""", [url])
            urlId = self.cursor.lastrowid
            if not urlId:
                self.cursor.execute(
                    """SELECT id FROM article_urls WHERE url=%s""",
                    [url]
                )
                urlId = cursor.fetchone()[0]
            # insert into article_social_media_shares
            self.cursor.execute(
                """INSERT INTO article_social_media_shares(url_id, social_media_channel, counts)
                values(%s, %s, %s) ON DUPLICATE KEY UPDATE counts=%s """, [urlId, socialMediaChannel, count, count])
        except Exception as ex:
            logger.error(ex)


if __name__ == "__main__":
    ob = SharesGetter()
    # counter = 0;
    # while(True):
    #     res = ob.getFBData("http://www.straitstimes.com/sport/football/football-vialli-says-england-struggle-to-handle-pressure")
    #     #"https://stackoverflow.com/questions/5607551/how-to-urlencode-a-querystring-in-python"
    #     print "res: ", res.text 
    #     if(200 != res.status_code):
    #         break
    #     counter = counter + 1;
    #     print counter
    #
    ob.main()
    # url = "http://stylehatch.co"
    # count = ob.get_linkedIn_shares(url)

    # logger.info("linkedin shares for url: " + url + " is: " + str(count))
    # self.dumpIntoMysql(url, count, "LinkedIn")
