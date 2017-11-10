# -*- coding: utf-8 -*-
import scrapy
import time
import json

class CampusZoneSpider(scrapy.Spider):
    name = 'campus-zone'
    allowed_domains = ['forums.hardwarezone.com.sg']
    start_urls = ['http://forums.hardwarezone.com.sg/nus-305/']

    def parse(self, response):
        threads = response.css('#threadslist > tbody:nth-child(2) > tr')

        for thread in threads:
            threadUrl = thread.css('td:nth-child(3) > div > a::attr(href)').extract_first()
            yield scrapy.Request(url=response.urljoin(threadUrl), callback=self.parseThreads)
        
        next_page_url = response.css('#inlinemodform > table:last-child > tr > td:last-child > div > ul > li:nth-last-child(2) > a::attr(href)').extract_first()
        next_page_url = response.urljoin(next_page_url)
        if next_page_url:
            yield scrapy.Request(url=next_page_url, callback=self.parse)
    

    def parseThreads(self, response):
        
        title = response.css("#forum > h2::text").extract_first()
        category = response.css('#breadcrumbs > li:nth-child(4) > a::text').extract_first()
        thread_url = response.url
        posts = response.css("#posts")
        for post in posts:
            item = {
                #Thread specific stuff (to identify the meta data)
                "title": title,
                "category": category,
                "updated_at": time.strftime("%d-%m-%Y %H:%M:%S"),
                "thread_url": thread_url,
                #Post specific stuff
                "user" : {
                    "id" : post.css('table > tr:nth-child(2) > td:nth-child(1) > div:nth-child(1) > a::text').extract_first(),
                    "url" : post.css('table > tr:nth-child(2) > td:nth-child(1) > div:nth-child(1) > a::attr(href)').extract_first(),
                    "number_of_posts" : post.css('table > tr:nth-child(2) > td:nth-child(1) > div:nth-child(4) >div:nth-child(3)::text').extract_first()
                },
                "post": {
                    "post_time" : " ".join(post.css("div:nth-child(1) >table > tr:nth-child(1) > td:nth-child(1)::text").extract()).strip(),
                    "content" : post.css('table > tr:nth-child(2) > td:nth-child(2)').extract_first(),
                    "post_number" : post.css("div:nth-child(1) >table > tr:nth-child(1) > td:nth-child(2) > a >strong::text").extract_first(),
                    "post_url" : post.css("div:nth-child(1) >table > tr:nth-child(1) > td:nth-child(2) > a::attr(href)").extract_first()
                }
            }
            print json.dumps(item)
            yield item

        next_page_url = response.css("#forum > table:nth-child(15) > tr > td:nth-child(2) > div > ul > li:nth-child(11) > a::attr(href)").extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parseThreads)