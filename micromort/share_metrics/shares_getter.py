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

#Helper functions
def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


class SharesGetter:
    def __init__(self):
        self.mongoClient = mongo_collection_articles
        self.db = db
        self.cursor = cursor

    def getUrlsToCrawl(self, d=1):
        now = datetime.datetime.now()
        today = datetime.datetime(now.year, now.month, now.day)
        from_date = today + datetime.timedelta(days=-d)
        to_date = today + datetime.timedelta(days=-d + 1)
        from_id = ObjectId.from_datetime(from_date)
        to_id = ObjectId.from_datetime(to_date)

        urls = []
        print "Getting urls from ", from_date, " to ", to_date
        articles = self.mongoClient.find({"_id": {"$gt": from_id, "$lt": to_id}})
        for article in articles:
            urls.append(article["link"])
        return urls

    @staticmethod
    def getFBData(urls):
        urls_string = ','.join(map(str,urls))
        urls_string = urllib.quote(urls_string)
        access_token = share_metricconfig["app_access_token"]
        api = share_metricconfig["fb_graph_api"].format( urls_string,access_token)
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

    def __get_fb_shares(self, urls):
        res = self.getFBData(urls)
        if res and res.status_code == 200:
            try:
                respJsons = json.loads(res.text)
                result = []
                for url in respJsons:
                    result.append({
                        "url" : url,
                        "type" :  "Facebook_comment_count",
                        "count" :  respJsons[url]["engagement"]["comment_count"]
                    })
                    result.append( {
                        "url" : url,
                        "type" : "Facebook_share_count", 
                        "count" : respJsons[url]["engagement"]["share_count"]
                    } )
                    result.append( {
                        "url" : url,
                        "type" : "Facebook_reaction_count",
                        "count" : respJsons[url]["engagement"]["reaction_count"]
                    } )
                    
                return result
            except Exception as ex:
                logger.error("Failed to load count for url: " + url)
                return -1
        else:
            return -1

    """
        @day: picks (from mongo) url fetched during given day
            0: today
            1: yesterday
            and so on
    """
    def main(self, urls):
        #urls = self.getUrlsToCrawl(day)

        logger.info(" Main function called, going to work on " \
                    + str(len(urls)) + " url(s)")
        logger.debug(" list of urls: " + str(urls))

        url_chunks = batch(urls, 10)

        for url_chunk in url_chunks:
            # Get fb counts
            fb_counts = self.__get_fb_shares(url_chunk)
            for row in fb_counts:
                url = row["url"]
                countType = row["type"]
                count = row["count"]
                logger.info(countType + " for url: " + url + " is: " + str(count))
                self.dumpIntoMysql(url, count,  countType)

                
            for url in url_chunk:
                # Get linkedin counts
                linkedIn_count = self.get_linkedIn_shares(url)
                logger.info("linkedin shares for url: " + url + " is: " + str(linkedIn_count))
                self.dumpIntoMysql(url, linkedIn_count,  "LinkedIn")

    def dumpIntoMysql(self, url, count, socialMediaChannel):
        # Pain of normalization: run 2 insert query:
        # insert into article_urls and get the insert id
        try:
            """
                Ok, next few steps are going to be little confusing... 
                grab some popcorn and sit tight!

                We first do an "insert ignore" into article_urls (url field has unique index 
                constraint), as no point of inserting same url twice.
                Then use lastrowid to get the id of last insertion,
                However consider the case when the row is not inserted (Reapted),
                Now according to this fellow:
                https://stackoverflow.com/questions/6291405/mysql-after-insert-ignore-get-primary-key
                LAST_INSERT_ID would be zero for ignored case,
                Bingo! just a select in such cases to get the url_id.

                then:
                With socialMediachannel, counts, urlId: Do an "insert, on duplicate update" in 
                article_social_media_shares table, if the effected rows are not zero (either 
                new entry of change in th counts) create a new entry in 
                article_social_media_shares_history
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
            effectedRows = self.cursor.execute(
                """INSERT INTO article_social_media_shares(url_id, social_media_channel, counts)
                values(%s, %s, %s) ON DUPLICATE KEY UPDATE counts=%s """, [urlId, socialMediaChannel, count, count])
            
            if effectedRows and count != -1:
                self.cursor.execute(
                    """INSERT IGNORE INTO  article_social_media_shares_history(url_id,  
                        social_media_channel, counts) values(%s, %s, %s)
                    """,  [urlId, socialMediaChannel, count])

        except Exception as ex:
            logger.error(ex)


if __name__ == "__main__":
    ob = SharesGetter()
    #run them for last 30 days (including today)! 30 ? :O (This has to be stopped)
    #for i in range(0,30):
    #    ob.main(i)
    ob.main(1)
    #urls = ob.getUrlsToCrawl(1)
    #for url in urls:
    #    print url
    #url = " http://www.straitstimes.com/tech/audio/beats-studio3-wireless-review-a-great-pair-of-headphones-for-ios-devices"
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
    #ob.dumpIntoMysql(url,0, 'Facebook')
    # url = "http://stylehatch.co"
    # count = ob.get_linkedIn_shares(url)

    # logger.info("linkedin shares for url: " + url + " is: " + str(count))
    # self.dumpIntoMysql(url, count, "LinkedIn")
