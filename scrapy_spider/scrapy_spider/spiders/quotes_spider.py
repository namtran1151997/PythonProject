# -*- coding: utf-8 -*-
import scrapy


class QuotesSpiderSpider(scrapy.Spider):
    name = 'insta_crawl'
    start_urls = ['https://www.instagram.com/vox.ngoc.traan/']

    def parse(self, response):
        yield {
            "response" : response
        }
