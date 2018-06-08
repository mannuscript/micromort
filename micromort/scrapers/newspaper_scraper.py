from datetime import datetime
from newspaper import Article
from micromort.resources.configs.mongodbconfig import mongodb_config
from micromort.data_stores.mysql import db, cursor
from micromort.data_stores.mongodb import getConnection
from multiprocessing.dummy import Pool as ThreadPool 
from micromort.utils.logger import logger
from dateutil import parser
import sys
import numpy as np

class Newspaper_scraper:
    def __init__(self, classify=False):
        self.db = db
        self.cursor = cursor
        self.classify = classify

        mongo_db = mongodb_config['dbs']['news_websites']['db']
        collection =  "newstweets_categorized_news"
        #mongodb_config['dbs']['news_websites']['collection']
        logger.debug("Creating mongo connection with db: " + mongo_db + " collection: " + collection)
        self.mongo_connection = getConnection(mongo_db, collection)


        rss_mongo_db = mongodb_config['dbs']['rss']['db']
        rss_mongo_collection =  mongodb_config['dbs']['rss']['collection']
        logger.debug("Creating mongo connection with db: " + rss_mongo_db + " collection: " + rss_mongo_collection)
        self.rss_connection = getConnection(rss_mongo_db, rss_mongo_collection)


        if classify:
            from micromort.models.trained_models.svm_mean_embeddings import Classifier, MeanEmbeddingVectorizer
            self.classifier = Classifier()

        pass

    def getRssData(self, url):
        return self.rss_connection.find_one({"link" : url})


    def scrape(self, url, useRssData=True):
        try:
            article = Article(url)
            article.download()
            article.parse()    
        except Exception as ex:
            logger.exception("Failed to load content for: " + url)
            return -1
        
        #logging for testing:
        logger.debug("scrapped title: " + article.title)

        #check the content
        #Well if we dont have article text, then it is useless !
        if len(article.text) < 1:
            return -1

        #Get Rss data from mongo (For summary and published date)
        summary = ""
        published = ""
        title = article.title
        if useRssData:
            rssData = self.getRssData(url)
            try:
                summary = rssData.get("summary", "")
                title = rssData.get("title", article.title)
                published = parser.parse(rssData.get("published", ""))
            except Exception:
                summary = ""
                published = ""
        
        
        
        ob = {
            "url" : article.url,
            "original_url" : url,
            "title" : title,
            "text" : article.text,
            "images" : article.images,
            "summary" : summary,
            "published" : published,
            "top_image" : article.top_image,
            "movies" :  article.movies,
            "meta": {
                "updated_at" :  datetime.utcnow(),
            }
        }
        return ob


    def storeInMongo(self,  collection,  item):
        url = item["url"]
        collection.update({ 
            "url"  : url
            } 
        ,  dict(item),  True)
        logger.debug("Article added to MongoDB database!")

    def getUrls(self):
        fromDate = "2017-12-01"
        toDate = "2018-03-01"
        self.cursor.execute(
                    #"""SELECT url FROM article_urls WHERE url like \"%www.asiaone.com%\" or url like \"%abc%\" """,
                    """SELECT url FROM article_urls where created_at between %s and %s""",
                    [fromDate, toDate]
                )
        urls = cursor.fetchall()
        return urls


    """
        @urls : Array of urls to worked upon
        @store : Boolean flag to decide if the scraped data to be stored in mongo
        @useRssData : Boolean flag to decide if (summary, published_data and title)
        is to be used from micromort.rss mongo collection. This should be set 
        to true only for the urls for which RSS fed service is collecting the data
        
        Returns the array of json with article's details and predicted labels
    """

    def main(self, urls, store=True, useRssData=False):
        print "coming here"
        try:
            #data = []
            count=0
            for _url in urls:
                #url = _url[0].strip()
                url = _url.strip()[:1024]
                count=count+1
                if(count%10000 == 0):
                    print "Done:::::::", count
                logger.info("scrapping :" + url)
                item = self.scrape(url, useRssData)
                if item != -1:
                    #data.append(item)
                    if self.classify:
                        item["labels"] = self.classifier.predict_single(item["title"] + " " + item["text"], True)
                        logger.info("Predicted labels:" + str(item["labels"]))
                    if store:
                        self.storeInMongo(self.mongo_connection, item)
        except Exception as e:
            print e
        return 1

def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

if __name__ == "__main__":
    ob = Newspaper_scraper(classify=False)
    urls = []
    file = sys.argv[1]
    with open('/home/mannu/code/work/micromort/data/urls/' + file, 'r') as fp:
        read_lines = fp.readlines()
        for line in read_lines:
            urls.append(line.strip())
    ob.main(urls)
    # batch_len = len(urls)
    # n_threads = 10
    # urls_batch = np.array_split(np.array(urls), n_threads)
    # pool = ThreadPool(n_threads)
    # #print "test", np.asarray(urls_batch)
    # try:
    #     print "coming here?"
    #     results = pool.map(ob.main, np.asarray(urls_batch))
    # except Exception as e:
    #     print e
    # #d = ob.main(urls, store=True, useRssData=False)
    
    # for _ in d:
    #     print _["url"], ",", _["title"]