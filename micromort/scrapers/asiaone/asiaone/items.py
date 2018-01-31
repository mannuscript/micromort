# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AsiaOneHeadlineItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    headline_text = scrapy.Field()
    image_url = scrapy.Field()
    article_url = scrapy.Field()


class AsiaoneArticlesItem(scrapy.Item):
    article_url = scrapy.Field()
    article_text = scrapy.Field()
    article_date = scrapy.Field()
    article_summary = scrapy.Field()
