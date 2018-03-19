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

        mongo_db = mongodb_config['dbs']['news_websites']['db']
        collection =  mongodb_config['dbs']['news_websites']['collection']
        logger.debug("Creating mongo connection with db: " + mongo_db + " collection: " + collection)
        self.mongo_connection = getConnection(mongo_db, collection)


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
        summary = ""
        published = ""
        try:
            summary = rssData.get("summary", "")
            published = rssData.get("published", "")
        except Exception:
            summary = ""
            published = ""
        ob = {
            "url" : url,
            "title" : article.title,
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
        Returns the array of json with article's details and predicted labels
    """

    def main(self, urls, store=True):

        data = []
        for _url in urls:
            #url = _url[0].strip()
            url = _url.strip()
            
            logger.info("scrapping :" + url)
            item = self.scrape(url)
            if item != -1:
                data.append(item)
                if self.classify:
                    item["labels"] = self.classifier.predict_single(item["title"] + " " + item["text"], True)
                    logger.info("Predicted labels:" + str(item["labels"]))
                if store:
                    self.storeInMongo(self.mongo_connection, item)
        return data


if __name__ == "__main__":
    ob = Newspaper_scraper(classify=False)
    #urls = ob.getUrls()
    #print "going to work on: " + str(len(urls)) + "urls"
    #ob.main(urls)
    #print ob.getRssData("http://www.straitstimes.com/world/united-states/raccoon-sized-dinosaur-with-bandit-mask-amazes-scientists")
    d = ob.main(["http://www.channelnewsasia.com/news/singapore/singapore-passport-becomes-most-powerful-in-the-world-9341920"],store=False)

    for _ in d:
        print _["url"], ",", _["title"]