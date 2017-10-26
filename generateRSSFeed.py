import sys

sys.path.append("./data_stores")
sys.path.append("./utils")
from logger import logger
from mysql import db, cursor
from mongodb import mongo_collection_articles
from time import strftime, gmtime

class GenerateRSSFeed:
    def __init__(self):
        self.mongoClient = mongo_collection_articles
        self.db = db
        self.cursor = cursor
    
    def getUrlsAndCounts(self, hours, counts):
        
        self.cursor.execute(
            """SELECT au.url, asms.counts FROM article_urls au INNER JOIN article_social_media_shares asms ON au.id = asms.url_id WHERE au.created_at > NOW() - INTERVAL %s HOUR ORDER BY asms.counts DESC LIMIT %s;""", [hours, counts])
        return cursor.fetchall()

    def getTitleOfUrls(self, urls):
        articles = self.mongoClient.find({"link":{ "$in" : urls}})
        urls_title = dict()
        for a in articles:
            urls_title[a["link"]] = a["title"]
        return urls_title

    def createRssFeed(self, urls_titles, urls_counts):
        itemString = "<item>\
            <title>{}</title>\
            <link>{}</link>\
            <description>\
                # of shares: {}\
            </description>\
            <pubDate>Thu, 1 May 2008 17:03:32 -0800</pubDate>\
        </item>"

        itemsString = '<?xml version="1.0" encoding="utf-8"?>\
                <rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/" \
    xmlns:dc="http://purl.org/dc/elements/1.1/" \
    xmlns:flickr="http://flickr.com/services/feeds/">\
    <channel>\
        <title>Trending News! What people are talking about!</title>\
        <link>http://mannuscript.com/</link>\
        <description>This Rss feed does some magic and fetches the URLs of the news articles (only Singapore based) which are shared most on facebook!</description>\
        <pubDate>{}</pubDate>\
        <lastBuildDate>{}</lastBuildDate>\
        <generator>http://mannuscript.com/</generator>'.format(strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()), strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))


        for url_count in urls_counts:
            print url_count[1]
            try: 
                itemsString += itemString.format(str(urls_titles[url_count[0]]).encode('ascii',errors='ignore'), url_count[0], url_count[1]).encode('ascii', 'ignore')
            except Exception as ex:
                print ex

        itemsString += '</channel></rss>'
        #print itemsString


if __name__ == "__main__":
    ob = GenerateRSSFeed()
    urls_counts = ob.getUrlsAndCounts(10, 100)
    # create array of urls to feed into mongo
    urls = []
    for url in urls_counts:
        urls.append(url[0])
    urls_titles = ob.getTitleOfUrls(urls)
    ob.createRssFeed(urls_titles, urls_counts)