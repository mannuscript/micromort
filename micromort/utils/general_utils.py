from micromort.resources.configs.mongodbconfig import mongodb_config
import pymongo
from datetime import datetime
import re
import micromort.constants as constants
import os
from tqdm import tqdm


FILE_PATHS = constants.PATHS
OUTPUTS_DIR = FILE_PATHS['OUTPUTS_DIR']
ARTICLE_LENGTH_THRESHOLD = constants.ARTICLE_LENGTH_PREP


def prep_asione_for_labeling():
    MONGO_URL = mongodb_config['host']
    MONGO_PORT = mongodb_config['port']
    MONGO_DB = mongodb_config['db']

    client = pymongo.MongoClient(MONGO_URL, MONGO_PORT)
    db = client[MONGO_DB]

    asiaone_article_collection = db[mongodb_config['asiaone_article_collection']]
    asiaone_headline_collection = db[mongodb_config['asiaone_headlines_collection']]
    asiaone_headlines = asiaone_headline_collection.find(no_cursor_timeout=True)

    with open(os.path.join(OUTPUTS_DIR, 'labeling', 'asiaone_articles.tsv'), 'w') as fp:
        fp.write('\t'.join(['title', 'url', 'category', 'summary', 'date']))
        fp.write('\n')
        for headline in tqdm(asiaone_headlines, total=asiaone_headline_collection.count(),
                             desc="Prepping asia one for labeling"):
            headline_text = headline['headline_text']
            headline_text = headline_text.replace("\n", "").replace("\t", " ")
            headline_url = headline['article_url']

            regex = re.compile('http://www.asiaone.com/(.*)/.*')
            match_obj = regex.match(headline_url)

            if match_obj:
                groups = match_obj.groups()
                category = groups[0]

            else:
                category = 'misc'

            article = asiaone_article_collection.find_one({'article_url': headline_url})

            if article:
                summary = article['article_summary']
                summary = summary.replace("\n", "").replace("\t", " ")
                date = article['article_date']
                utc_time = datetime.strptime(date, '%Y-%M-%d')
                utc_time = str(int(utc_time.timestamp()))

                article_text = article['article_text']

                if len(article_text) > ARTICLE_LENGTH_THRESHOLD:
                    fp.write('\t'.join([headline_text, headline_url, category, summary, utc_time]))
                    fp.write("\n")


def prep_straitstimes_for_labeling():
    MONGO_URL = mongodb_config['host']
    MONGO_PORT = mongodb_config['port']
    MONGO_DB = mongodb_config['db']

    client = pymongo.MongoClient(MONGO_URL, MONGO_PORT)
    db = client[MONGO_DB]

    straitstimes_headline_collection = db[mongodb_config['straitstimes_headlines_collection']]
    straitstimes_article_collection = db[mongodb_config['straitstimes_article_collection']]

    straitstimes_headlines = straitstimes_headline_collection.find()

    with open(os.path.join(OUTPUTS_DIR, 'labeling', 'straitstimes_articles.tsv'), 'w') as fp:
        fp.write('\t'.join(['title', 'url', 'category', 'summary', 'date']))
        fp.write('\n')
        for headline in tqdm(straitstimes_headlines, total=straitstimes_headlines.count(),
                             desc="Prepping straitstimes headline collection"):
            article_url = headline['article_url']

            regex = re.compile('http://www.straitstimes.com/(.*)/.*')
            match_obj = regex.match(article_url)

            if match_obj:
                groups = match_obj.groups()
                category = groups[0]

            else:
                category = 'misc'

            headline_text = headline['headline']
            date = headline['date']

            try:
                utc_time = datetime.strptime(date, "%b %d, %Y, %H:%M %p")
                utc_time = utc_time.timestamp()
                utc_time = str(int(utc_time))
            except ValueError:
                continue

            headline_text = headline_text.replace("\n", "").replace("\t", " ").strip()

            article = straitstimes_article_collection.find_one({'article_url': article_url})

            if article:
                article_text = article['article_text']
                article_text = article_text.replace("\n", "").replace("\t", " ").strip()

                # Getting first 50 words as a summary
                article_summary = article_text.split(" ")
                article_summary = " ".join(article_summary[:50])

                if len(article_text) > ARTICLE_LENGTH_THRESHOLD:
                    fp.write('\t'.join([headline_text, article_url, category, article_summary, utc_time]))
                    fp.write("\n")


if __name__ == '__main__':
    # prep_asione_for_labeling()
    prep_straitstimes_for_labeling()
