# -*- coding: utf-8 -*-
import scrapy
import time
import json
import re
import sys

regex4XX5XX = re.compile("[4|5][0-9][0-9]")
consecutive400s = 0
pagesCrawled = 0
pagesToBeCrawl = 10

def handleNon200():
    global consecutive400s
    consecutive400s += 1
    if consecutive400s == 42:
        raise scrapy.exceptions.CloseSpider("42 consecutive 4XX/5XX, terminating the spider!")

class SgtalkSpider(scrapy.Spider):
    name = 'sgtalk'
    allowed_domains = ['sgtalk.org']
    start_urls = ['http://sgtalk.org/mybb/']
    custom_settings = {
    }

    def parse(self, response):
        threads =  response.css('#content > div:nth-child(5) > table >  tr > td:nth-child(1) > table > tr')
        for thread in threads:
            threadUrl = thread.css('span > a::attr(href)').extract_first()
            yield scrapy.Request(url=response.urljoin(threadUrl), callback=self.parseThreads)
        next_page_url = response.css('#content > div:nth-child(5) > table > tr > td:nth-child(1) > div:nth-child(1) > div.float_left > div > a.pagination_next::attr(href)').extract_first()
        
        #Terminate if we have crawled ten pages!
        global pagesCrawled
        pagesCrawled += 1

        next_page_url = response.urljoin(next_page_url)
        if next_page_url and pagesCrawled < pagesToBeCrawl:
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parseThreads(self, response):
        
        if regex4XX5XX.match(str(response.status)) is not None:
            handleNon200()
            return
        global consecutive400s
        consecutive400s = 0

        title = response.css("#forum_name::text").extract_first()
        category = response.css("#content > div.navigation > span > a:nth-child(3)::text").extract_first()
        thread_url = response.url
        #remove the page id from url
        thread_url[: thread_url.find("?page=")]
        posts_json = []
        posts = response.css("#posts > table")
        for post in posts:
            item = {
                #Thread specific stuff (to identify the meta data)
                "title": title,
                "category": category,
                "updated_at": time.strftime("%d-%m-%Y %H:%M:%S"),
                "thread_url": thread_url,
                #Post specific stuff
                "user" : {
                    "name": post.css("tr:nth-child(2) > td:nth-child(1) > span::text").extract_first(),
                    "id" : post.css("tr:nth-child(2) > td:nth-child(1) > strong > span > a::text").extract_first(),
                    "url" : post.css("tr:nth-child(2) > td:nth-child(1) > strong > span > a::attr(href)").extract_first(),
                    "reputation" : post.css("tr:nth-child(2) > td:nth-child(1) > span > a:nth-child(5) > strong::text").extract_first()
                },
                "post": {
                    "post_time" : post.css("tr:nth-child(1) > td:nth-child(1) > span::text").extract_first(),
                    "content" : post.css("table > tr:nth-child(2) > td:nth-child(2) > table > tr > td").extract_first(),
                    "post_number" : post.css("tr:nth-child(1) > td:nth-child(2) > div > span > strong > a::text").extract_first(),
                    "post_url" : post.css("tr:nth-child(1) > td:nth-child(2) > div > span > strong > a::attr(href)").extract_first()
                }
            }
            yield item
        
        next_page_url = response.css('#content > table > tr > td:nth-child(1) > div:nth-child(7) > div > a.pagination_next::attr(href)').extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parseThreads)