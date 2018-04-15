#from micromort.pipeline import Pipeline
from micromort.utils.logger import logger
from micromort.data_stores.mongodb import getConnection
from micromort.resources.configs.twitter_getter_config import twitter_getter_config
from micromort.resources.configs.mongodbconfig import mongodb_config

from TwitterSearch import TwitterSearchOrder, TwitterSearchException, TwitterSearch

class TweetGetter:
    def __init__(self):
        mongo_db_name = mongodb_config["dbs"]["news_tweets"]["db"] 
        mongo_collection_name = mongodb_config["dbs"]["news_tweets"]["collection"]
        self.mongoClient = getConnection(mongo_db_name, mongo_collection_name)
        try:
            self.ts = TwitterSearch(
                consumer_key = twitter_getter_config["key_sets"][0]["APP_KEY"],
                consumer_secret = twitter_getter_config["key_sets"][0]["APP_SECRET"],
                access_token = twitter_getter_config["key_sets"][0]["OAUTH_TOKEN"],
                access_token_secret = twitter_getter_config["key_sets"][0]["OAUTH_TOKEN_SECRET"]
            )
        except TwitterSearchException as e:
            print(e)


    def get_since_id(self, url):
        doc = list(self.mongoClient.find({"news_article_url" : url}).sort([("id",-1)]).limit(1))
        if doc is None or len(doc) == 0:
            return 1
        else:
            return doc[0]["id"]

    
    def get_tweets(self, url):
        since_id = self.get_since_id(url)
        tso = TwitterSearchOrder()
        tso.set_keywords([url])
        print("setting id as ",  since_id)
        tso.set_since_id(since_id)
        return list(self.ts.search_tweets_iterable(tso))



    def main(self, urls):
        for url in urls:
            tweets = self.get_tweets(url)
            for tweet in tweets:
                tweet["news_article_url"] = url
                self.storeInMongo(tweet)


    def storeInMongo(self, item):
    
        tweet_id = item["id"]
        self.mongoClient.update({ 
            "id"  : tweet_id
            } 
        , dict(item),  True)
        logger.debug("Article added to MongoDB database!")



if __name__ == "__main__":
    logger.info("------------- Get number of shares/likes -----------")
    #ob = Pipeline()
    day = 1
    tweet_getter = TweetGetter()

    try:
        for i in range(1, day+1):
            tweet_getter.main(["http://www.foxnews.com/politics/2018/04/14/largest-syrian-american-group-hails-trump-after-military-action.html"])#ob.getUrlsToCrawl(i))
    except Exception as ex:
        logger.error(ex)