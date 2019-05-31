# -*- coding: utf-8 -*-
import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['example.py']
    start_urls = ['http://example.py/']

    def parse(self, response):
        pass
