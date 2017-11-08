# -*- coding: utf-8 -*-
import scrapy
import time
import json
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
            print response.urljoin(threadUrl)
        next_page_url = response.css('#content > div:nth-child(5) > table > tr > td:nth-child(1) > div:nth-child(1) > div.float_left > div > a.pagination_next::attr(href)').extract_first()
        next_page_url = response.urljoin(next_page_url)
        if next_page_url:
            print "going to", next_page_url
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parseThreads(self, response):
        
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
            print "going to", next_page_url
            yield scrapy.Request(url=next_page_url, callback=self.parseThreads)