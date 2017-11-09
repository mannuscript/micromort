# -*- coding: utf-8 -*-
import scrapy
from micromort.scrapers.straitstimes.straitstimes.items import StraitsTimesHeadlinesItem
from micromort.resources.configs.mongodbconfig import mongodb_config
import pymongo
import re


class StraitstimesNewsSpider(scrapy.Spider):
    name = 'straitstimes_news'
    allowed_domains = ['straitstimes.com']
    straitstimes_base_url = 'http://straitstimes.com'
    categories = ['politics', 'asia', 'world', 'multimedia', 'lifestyle', 'forum', 'opinion',
                  'business', 'sport', 'tech']
    start_urls = map(lambda category: 'http://www.straitstimes.com/' + category + '/latest', categories)
    get_page_pattern = re.compile('.*\?page=([0-9]*)')
    custom_settings = {
        'ITEM_PIPELINES': {
            'micromort.scrapers.straitstimes.straitstimes.pipelines.DuplicateNewsPipeline': 300,
            'micromort.scrapers.straitstimes.straitstimes.pipelines.MongoDBPipeline': 400
        }
    }

    def __init__(self, *args, **kwargs):
        self.MONGODB_URL = mongodb_config['host']
        self.MONGODB_PORT = mongodb_config['port']
        self.MONGODB_DB = mongodb_config['db']
        self.MONGODB_COLLECTION = mongodb_config['straitstimes_headlines_collection']
        self.client = pymongo.MongoClient(self.MONGODB_URL, self.MONGODB_PORT)
        self.db = self.client[self.MONGODB_DB]
        self.collection = self.db[self.MONGODB_COLLECTION]
        self.unique_index = 'article_url'
        super(StraitstimesNewsSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        # The latest news is available at http://www.straitstimes.com/<category>/latest[?page=[1, 2, 3]]
        url = response.url
        print "response url", url

        # scrap the leading page and yield requests for more pages
        headline_items = self.parse_headline_page(response)

        for headline_item in headline_items:
            yield headline_item

        # get the page that is getting parsed now and replace it with the next page
        match = self.get_page_pattern.search(url)
        page = 0 if not match else 1
        if page == 0:
            next_url = url + '?page=1'
        else:
            next_page = str(int(match.groups()[0]) + 1)
            next_url = list(url.partition('page='))
            next_url[2] = next_page
            next_url = ''.join(next_url)

        print 'next url to be scraped %s' % (next_url, )
        yield scrapy.http.Request(next_url, callback=self.parse)

    @staticmethod
    def parse_headline_page(response):
        # parse the headlines page and return the item to be stored
        views_row_even = response.css('div.views-row-even')
        views_row_odd = response.css('div.views-row-odd')

        if len(views_row_even) + len(views_row_odd) == 0:
            return

        headlines_card = views_row_even + views_row_odd
        headline_items = []
        for headline_card in headlines_card:
            image_url = headline_card.css('noscript>img::attr(src)').extract_first()
            headline = headline_card.css('span.story-headline>a::text').extract_first()
            article_url = headline_card.css('span.story-headline>a::attr(href)').extract_first()
            date_posted_string = headline_card.css('div.node-postdate::attr(data-lapsevalue)').extract_first()
            headline_items.append(StraitsTimesHeadlinesItem(
                headline=headline,
                image_url=image_url,
                article_url=article_url,
                date=date_posted_string,
            ))

        return headline_items
