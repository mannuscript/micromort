# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class StraitsTimesHeadlinesItem(scrapy.Item):
    # define the fields for your item here like:
    headline = scrapy.Field()
    image_url = scrapy.Field()
    date = scrapy.Field()
    article_url = scrapy.Field()

