"""
This module is for aggregating and pre-processing the human annotated dataset.
This can be further used in pytorch or tensorflow as required
"""
import micromort.constants as constants
import csv
import os
from micromort.resources.configs.mongodbconfig import mongodb_config
from micromort.utils.general_utils import save_pickle, load_pickle
import pymongo
from tqdm import tqdm
from pydash.collections import pluck
from pydash.arrays import flatten_deep
from collections import Counter
from operator import itemgetter

import spacy

FILE_PATHS = constants.PATHS
DATA_DIR = FILE_PATHS['DATA_DIR']
OUTPUTS_DIR = FILE_PATHS['OUTPUTS_DIR']
LANG_NEWS_ARTICLES_PATH = os.path.join(OUTPUTS_DIR, 'lang_news_articles')


class RiskAnnotatedBase:
    def __init__(self, use_headlines_only=True,
                 max_words=3000,
                 lowercasing=True,
                 lemmatization=True,
                 stop_word_removal=True):
        self.MONGODB_URL = mongodb_config['onespace_host']
        self.MONGODB_PORT = mongodb_config['port']
        self.DB = mongodb_config['db']
        self.ASIAONE_LABELING_COLLECTION = mongodb_config['asiaone_labeling_collection']
        self.BUSINESSTIMES_LABELING_COLLECTION = mongodb_config[
            'businesstimes_labeling_collection']
        self.CHANNELNEWSASIA_LABELING_COLLECTION = mongodb_config[
            'channelnewsasia_labeling_collection']
        self.STRAITSTIMES_LABELING_COLLECTION = mongodb_config[
            'straitstimes_labeling_collection']
        self.use_headlines_only = use_headlines_only
        self.max_words = max_words
        self.lowercasing = lowercasing
        self.lemmatization = lemmatization
        self.stop_word_removal = stop_word_removal

        # load the spacy nlp
        self.spacy_nlp = spacy.load('en')

        self.mongo_client = pymongo.MongoClient(self.MONGODB_URL, self.MONGODB_PORT)
        self.db = self.mongo_client[self.DB]

        self.asiaone_labeling_collection = self.db[self.ASIAONE_LABELING_COLLECTION]
        self.businesstimes_labeling_collection = self.db[
            self.BUSINESSTIMES_LABELING_COLLECTION]
        self.channelnewsasia_labeling_collection = self.db[
            self.CHANNELNEWSASIA_LABELING_COLLECTION]
        self.straitstimes_labeling_collection = self.db[
            self.STRAITSTIMES_LABELING_COLLECTION]

        # the combine labeling collection
        self.labeling_collection = self.get_labeling_collection()
        self.annotated_data = self.prepare_data()
        self.risk_values_to_categories = self.get_risk_categories()

        # tokenize the text
        self.tokenized_article_texts, self.tokenized_article_headlines = \
            self.pre_process()

        # build the vocab
        self.words_to_idx = self.build_vocab()
        self.idx_to_words = {v: k for k, v in self.words_to_idx.items()}

        # Get the label information for all the data
        self.risk_labels, self.sentiment_labels = self.get_labels()

        self.labels = self.get_labels()

        print("The size of the vocab {0}".format(self.get_vocab_size()))

    @staticmethod
    def get_risk_categories():
        categories = ['health', 'safety_security', 'environment',
                      'social_relations', 'meaning_in_life', 'achievement',
                      'economics', 'politics', 'not_applicable', 'skip']
        category_values = list(range(91, 100)) + [-1]

        return dict(zip(categories, category_values))

    def prepare_data(self):
        # get the article url and article text for the urls in the database dump
        data_pickle_file = os.path.join(LANG_NEWS_ARTICLES_PATH, 'data.pkl')
        if not os.path.isfile(data_pickle_file):
            data = []
            with open(os.path.join(DATA_DIR, 'risk_annotated.csv')) as fp:
                lines = [line for line in fp]
                num_lines = len(lines)
                csvreader = csv.reader(lines, delimiter=',')
                for row in tqdm(csvreader, total=num_lines,
                                desc="Reading the human annotated file"):
                    article_id = row[0]
                    article_url = row[1]
                    sentiment_category = int(row[2])
                    risk_category = row[3]
                    risk_category = list(set(risk_category.split(",")))
                    risk_category = map(lambda category: int(category), risk_category)
                    risk_category = list(risk_category)

                    if -1 in risk_category:
                        continue

                    # get the corresponding article_text and headline
                    doc = self.labeling_collection.find_one({'url': article_url})

                    if not doc:
                        raise ValueError('there is no labeling article with '
                                         'this url: {0}'.format(article_url))

                    article_headline = doc['title']
                    article_text = doc['text']
                    data.append({
                        'article_id': article_id,
                        'risk_category': risk_category,
                        'sentiment_category': sentiment_category,
                        'article_headline': article_headline,
                        'article_text': article_text
                    })

            save_pickle(data, data_pickle_file)

        else:
            print("Loading the human annotated data from pickle file")
            data = load_pickle(data_pickle_file)

        return data

    def get_labeling_collection(self):
        labeling_collection = self.db['news_labeling']

        if labeling_collection.count() == 0:
            print("Combining all the data that is prepared for labeling into "
                  "a collection")
            # read all the documents from the collection
            asiaone_docs = self.read_documents(self.asiaone_labeling_collection)
            businesstimes_docs = self.read_documents(
                self.businesstimes_labeling_collection)
            channelnewsasia_docs = self.read_documents(
                self.channelnewsasia_labeling_collection)
            straitstimes_docs = self.read_documents(self.straitstimes_labeling_collection)

            labeling_docs = asiaone_docs + businesstimes_docs + \
                            channelnewsasia_docs + straitstimes_docs

            labeling_collection.insert_many(labeling_docs)

        return labeling_collection

    @staticmethod
    def read_documents(collection):
        documents = collection.find(no_cursor_timeout=True)
        documents = [document for document in documents]
        print("Read {0} documents from the collection {1}".format(len(documents),
                                                                  collection.name))
        return documents

    def build_vocab(self):

        words_to_idx_filename = os.path.join(LANG_NEWS_ARTICLES_PATH, 'word_to_idx.pkl')

        if not os.path.isfile(words_to_idx_filename):
            words_to_idx = {
                '<UNK>': 0,
                '<SOS>': 1,
                '<EOS>': 2,
                '<PAD>': 3

            }
            article_headline_tokens = flatten_deep(self.tokenized_article_headlines)
            article_text_tokens = flatten_deep(self.tokenized_article_texts)

            if self.use_headlines_only:
                tokens = article_headline_tokens
            else:
                tokens = article_headline_tokens + article_text_tokens

            tokens_counter = Counter(tokens)

            tokens_counter_sorted = sorted(tokens_counter.items(), reverse=True,
                                           key=itemgetter(1))

            tokens_most_frequent = tokens_counter_sorted[:self.max_words]

            for idx, (word, freq) in enumerate(tokens_most_frequent):
                words_to_idx[word] = idx + 4

            print("Storing word to idx in a pickle file")
            save_pickle(words_to_idx, words_to_idx_filename)

        else:
            print("Loading words_to_idx from pickle file")
            words_to_idx = load_pickle(words_to_idx_filename)

        return words_to_idx

    def pre_process(self):

        news_articles_tokens_filename = os.path.join(LANG_NEWS_ARTICLES_PATH,
                                                     'news_articles.tokens')

        news_headlines_tokens_filename = os.path.join(LANG_NEWS_ARTICLES_PATH,
                                                      'news_headlines.tokens')

        if not os.path.isfile(news_articles_tokens_filename) \
                or not os.path.isfile(news_headlines_tokens_filename):

            article_texts = pluck(self.annotated_data, 'article_text')

            tokenized_article_texts = [self.tokenize(self.spacy_nlp(article_text)) for
                                       article_text in tqdm
                                       (article_texts, total=len(article_texts),
                                        desc="Pre Processing the article texts")]

            article_headlines = pluck(self.annotated_data, 'article_headline')

            tokenized_article_headlines = [self.tokenize(self.spacy_nlp(article_headline))
                                           for article_headline
                                           in tqdm(article_headlines,
                                                   total=len(article_headlines),
                                                   desc="Pre "
                                                        "Processing the article headlines")]

            save_pickle(tokenized_article_texts, news_articles_tokens_filename)
            save_pickle(tokenized_article_headlines, news_headlines_tokens_filename)

        else:
            print("Loading the tokens from the token files")
            tokenized_article_texts = load_pickle(news_articles_tokens_filename)
            tokenized_article_headlines = load_pickle(news_headlines_tokens_filename)

        return tokenized_article_texts, tokenized_article_headlines

    def get_vocab_size(self):
        return len(set(self.words_to_idx.values()))

    def get_labels(self):
        risk_labels = pluck(self.annotated_data, 'risk_category')
        sentiment_labels = pluck(self.annotated_data, 'sentiment_category')

        return risk_labels, sentiment_labels

    def tokenize(self, spacy_doc):
        tokens = []
        for token in spacy_doc:
            if self.stop_word_removal and token.is_stop:
                continue
            if self.lemmatization:
                token_mod = token.lemma_
            else:
                token_mod = token.text
            if self.lowercasing:
                token_mod = token_mod.lower()

            tokens.append(token_mod)

        return tokens


if __name__ == '__main__':
    risk_dataset = RiskAnnotatedBase()
