from datetime import datetime
from newspaper import Article
from micromort.resources.configs.mongodbconfig import mongodb_config
from micromort.data_stores.mysql import db, cursor
from micromort.data_stores.mongodb import getConnection
from micromort.utils.logger import logger
from micromort.models.trained_models.svm_mean_embeddings import Classifier, MeanEmbeddingVectorizer

class Newspaper_scraper:
    def __init__(self, classify=False):
        self.db = db
        self.cursor = cursor
        self.classify = classify

        asiaone_mongo_db = mongodb_config['dbs']['news_websites']['asiaone']['db']
        asiaone_mongo_collection =  mongodb_config['dbs']['news_websites']['asiaone']['collection']
        logger.debug("Creating mongo connection with db: " + asiaone_mongo_db + " collection: " + asiaone_mongo_collection)
        self.asiaone_connection = getConnection(asiaone_mongo_db, asiaone_mongo_collection) 

        businesstimes_mongo_db = mongodb_config['dbs']['news_websites']['businesstimes']['db']
        businesstimes_mongo_collection =  mongodb_config['dbs']['news_websites']['businesstimes']['collection']
        logger.debug("Creating mongo connection with db: " + businesstimes_mongo_db + " collection: " + businesstimes_mongo_collection)
        self.businesstimes_connection = getConnection(businesstimes_mongo_db, businesstimes_mongo_collection) 

        channelnews_mongo_db = mongodb_config['dbs']['news_websites']['channelnews']['db']
        channelnews_mongo_collection =  mongodb_config['dbs']['news_websites']['channelnews']['collection']
        logger.debug("Creating mongo connection with db: " + channelnews_mongo_db + " collection: " + channelnews_mongo_collection)
        self.channelnews_connection = getConnection(channelnews_mongo_db, channelnews_mongo_collection) 

        straitstimes_mongo_db = mongodb_config['dbs']['news_websites']['straitstimes']['db']
        straitstimes_mongo_collection =  mongodb_config['dbs']['news_websites']['straitstimes']['collection']
        logger.debug("Creating mongo connection with db: " + straitstimes_mongo_db + " collection: " + straitstimes_mongo_collection)
        self.straitstimes_connection = getConnection(straitstimes_mongo_db, straitstimes_mongo_collection)

        rss_mongo_db = mongodb_config['dbs']['rss']['db']
        rss_mongo_collection =  mongodb_config['dbs']['rss']['collection']
        logger.debug("Creating mongo connection with db: " + rss_mongo_db + " collection: " + rss_mongo_collection)
        self.rss_connection = getConnection(rss_mongo_db, rss_mongo_collection)


        if classify:
            self.classifier = Classifier()

        pass

    def getRssData(self, url):
        return self.rss_connection.find_one({"link" : url})


    def scrape(self, url):
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
        rssData = self.getRssData(url)

        ob = {
            "url" : url,
            "title" : article.title,
            "text" : article.text,
            "images" : article.images,
            "summary" : rssData.get("summary", ""),
            "published" : rssData.get("published", ""),
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
        Returns the array of json with article's details and predicted labels
    """

    def main(self, urls, store=True):

        collection = ""
        data = []
        for _url in urls:
            #url = _url[0].strip()
            url = _url.strip()
            if "www.businesstimes.com.sg" in url:
                collection = self.businesstimes_connection
            elif "www.straitstimes.com" in url:
                collection = self.straitstimes_connection
            elif "www.channelnewsasia.com" in url:
                collection = self.channelnews_connection
            else:
                collection = self.asiaone_connection
            logger.info("scrapping :" + url)
            item = self.scrape(url)
            if item != -1:
                data.append(item)
                if self.classify:
                    item["labels"] = self.classifier.predict_single(item["title"] + " " + item["text"], True)
                    logger.info("Predicted labels:" + str(item["labels"]))
                if store:
                    self.storeInMongo(collection, item)
        return data


if __name__ == "__main__":
    ob = Newspaper_scraper(classify=True)
    #urls = ob.getUrls()
    #print "going to work on: " + str(len(urls)) + "urls"
    #ob.main(urls)
    #print ob.getRssData("http://www.straitstimes.com/world/united-states/raccoon-sized-dinosaur-with-bandit-mask-amazes-scientists")
    ob.main(["http://www.straitstimes.com/world/united-states/raccoon-sized-dinosaur-with-bandit-mask-amazes-scientists"])