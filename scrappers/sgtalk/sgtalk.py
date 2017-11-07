# -*- coding: utf-8 -*-
import scrapy


class SgtalkSpider(scrapy.Spider):
    name = 'sgtalk'
    allowed_domains = ['http://sgtalk.org/mybb/']
    start_urls = ['http://sgtalk.org/mybb/']

    def parse(self, response):
        threads =  response.css('#content > div:nth-child(5) > table >  tr > td:nth-child(1) > table > tr')
        for thread in threads:
            threadUrl = thread.css('span > a::attr(href)').extract_first()
            #yield scrapy.Request(url=response.urljoin(threadUrl), callback=parseThreads)
            print response.urljoin(threadUrl)
        yield None
        next_page_url = response.css('#content > div:nth-child(5) > table > tr > td:nth-child(1) > div:nth-child(1) > div.float_left > div > a.pagination_next::attr(href)').extract_first()
        next_page_url = response.urljoin(next_page_url)
        if next_page_url:
            print "going to", next_page_url
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parseThreads(self, response):
        #do something
        pass