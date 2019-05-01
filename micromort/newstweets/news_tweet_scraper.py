import traceback, sys
from newspaper import Article
from micromort.utils.logger import logger

def gen_dict_extract(key, var):
    if hasattr(var, 'items'):
        for k, v in var.items():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in gen_dict_extract(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in gen_dict_extract(key, d):
                        yield result

def getUrl(tweet):
    return gen_dict_extract("expanded_url", tweet)


class News_tweet_scraper:
    def getUrls(tweet):
        try:
            urls = getUrl(tweet)
            tweet_id = tweet["id"]
            filtered_urls = []
            for url in urls:
                if "twitter.com" not in url:
                    filtered_urls.append(url)

            return filtered_urls
        except Exception as e:
            print(e)
            traceback.print_exc()
            return []


    def scrape(self, url, useRssData=True):
        try:
            article = Article(url)
            article.download()
            article.parse()    
        except Exception as ex:
            logger.exception("Failed to load content for: " + url)
            return None
        
        #logging for testing:
        logger.debug("scrapped title: " + article.title)

        #check the content
        #If we dont have article text, then it is useless !
        if len(article.text) < 1:
            return None

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

