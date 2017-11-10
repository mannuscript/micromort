# -*- coding: utf-8 -*-
import scrapy
import re
from micromort.scrapers.asiaone.asiaone.items import AsiaOneHeadlineItem
from micromort.resources.configs.mongodbconfig import mongodb_config
import pymongo


class AsiaoneNewsSpider(scrapy.Spider):
    name = 'asiaone_headline'
    allowed_domains = ['www.asiaone.com']
    categories = ['singapore', 'malaysia', 'china', 'asia', 'world',
                  'business', 'showbiz', 'travel', 'digital', 'food', 'health',
                  'women']
    start_urls = map(lambda category: 'http://www.asiaone.com/' + category, categories)
    get_page_pattern = re.compile('.*\?page=([0-9]*)')
    custom_settings = {
        'ITEM_PIPELINES': {
            'micromort.scrapers.asiaone.asiaone.pipelines.DuplicateNewsPipeline': 300,
            'micromort.scrapers.asiaone.asiaone.pipelines.MongoDBPipeline': 400
        }
    }

    def __init__(self, *args, **kwargs):
        self.MONGODB_URL = mongodb_config['host']
        self.MONGODB_PORT = mongodb_config['port']
        self.MONGODB_DB = mongodb_config['db']
        self.MONGODB_COLLECTION = mongodb_config['asiaone_headlines_collection']
        self.client = pymongo.MongoClient(self.MONGODB_URL, self.MONGODB_PORT)
        self.db = self.client[self.MONGODB_DB]
        self.collection = self.db[self.MONGODB_COLLECTION]
        self.unique_index = 'article_url'
        super(AsiaoneNewsSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        url = response.url
        cards = response.css('div.card')
        headline_items = self.get_cards_info(cards)
        for headline_item in headline_items:
            yield headline_item

        match = self.get_page_pattern.search(url)
        page = 0 if not match else 1
        if page == 0:
            next_url = url + '?page=1'
        else:
            next_page = str(int(match.groups()[0]) + 1)
            next_url = list(url.partition('page='))
            next_url[2] = next_page
            next_url = ''.join(next_url)

        print 'next url to be scraped %s' % (next_url,)
        yield scrapy.http.Request(next_url, callback=self.parse)

    def get_cards_info(self, cards):
        headline_items = []
        for card in cards:
            headline_item = self.get_card_info(card)
            if headline_item:
                headline_items.append(headline_item)

        return headline_items

    @staticmethod
    def get_card_info(card):
        article_url = card.css('a.header::attr(href)').extract_first()

        # parse only the original asia one content
        # otherwise skip it
        if article_url and not article_url.startswith('http'):
            headline_text = card.css('a.header::text').extract_first()
            image_url = card.css('picture.img-responsive>source::attr(data-srcset)').extract_first()
            asiaone_item = AsiaOneHeadlineItem(
                headline_text=headline_text,
                image_url=image_url,
                article_url=article_url
            )
            return asiaone_item
        else:
            return None
