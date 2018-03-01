from micromort.resources.configs.mongodbconfig import mongodb_config
import pymongo
from datetime import datetime
import re
import micromort.constants as constants
import os
from tqdm import tqdm
import pickle
import h5py

FILE_PATHS = constants.PATHS
OUTPUTS_DIR = FILE_PATHS['OUTPUTS_DIR']
ARTICLE_LENGTH_THRESHOLD = constants.ARTICLE_LENGTH_PREP


def partition_lists(lst, n):
    """
        given a list it is partitioned into n sub lists
    """
    division = len(lst) / float(n)
    return [lst[int(round(division * i)): int(round(division * (i + 1)))] for i in range(n)]


def prep_asiaone_for_labeling():
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


def save_pickle(obj, filename):
    with open(filename, 'wb') as fp:
        pickle.dump(obj, fp)


def load_pickle(filename):
    with open(filename, 'rb') as fp:
        return pickle.load(fp)


def read_array_from_hdf_file(filepath, object_name):
    """

    Args:
        filepath: The full path of the h5 file
        object_name: The name of the object stored in the file

    Returns: Numpy array strored in the file

    """
    file_handle = h5py.File(filepath, 'r')
    array = file_handle[object_name][:]
    file_handle.close()

    return array


def write_array_to_hdf_file(filepath, objectname, data):
    """

    Args:
        filepath: Full path of the file name where the
        objectname: object name is used to store the object
        data: Numpy array that needs to be stored with object name in the file

    Returns:

    """
    file_handle = h5py.File(filepath, 'w')
    file_handle.create_dataset(objectname, data=data)
    file_handle.close()


if __name__ == '__main__':
    # prep_asione_for_labeling()
    prep_straitstimes_for_labeling()
