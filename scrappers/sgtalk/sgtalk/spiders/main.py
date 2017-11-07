# -*- coding: utf-8 -*-
import scrapy

class MainItem(scrapy.item):
    url = Field()
    title = Field()    

class MainSpider(scrapy.Spider):
    name = 'main'
    allowed_domains = ['sgtalk.org']
    start_urls = ['http://sgtalk.org/mybb/']

    def parse(self, response):
        threads =  response.css('#content > div:nth-child(5) > table >  tr > td:nth-child(1) > table > tr')
        for thread in threads:
            threadUrl = thread.css('span > a::attr(href)').extract_first()
            yield scrapy.Request(url=response.urljoin(threadUrl), callback=self.parseThreads)
            #print response.urljoin(threadUrl)
        next_page_url = response.css('#content > div:nth-child(5) > table > tr > td:nth-child(1) > div:nth-child(1) > div.float_left > div > a.pagination_next::attr(href)').extract_first()
        next_page_url = response.urljoin(next_page_url)
        # if next_page_url:
        #     print "going to", next_page_url
        #     yield scrapy.Request(url=next_page_url, callback=None)

    def parseThreads(self, response):
        posts = response.css('#posts')
        item = MainItem()
        item['title'] = ""
        item['url'] = ""
        for post in posts:
            print post.css("table > tr:nth-child(2) > td:nth-child(2) >table > tr >td > div::text ").extract()
        