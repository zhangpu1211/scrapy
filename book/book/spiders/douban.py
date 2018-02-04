# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from book.items import BookItem

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['book.douban.com']
    start_urls = ['https://book.douban.com/top250?start=0/']

    def parse(self, response):
        item = BookItem()
        nodes = response.xpath('//div[@class="article"]//tr[@class="item"]')
        for node in nodes:
            name = node.xpath('td[2]/div[1]/a/text()').extract_first().strip()
            summary = node.xpath('td[2]/p[2]/span/text()').extract_first()
            item['name'] = name
            item['summary'] = summary
            yield item
        next_urls = response.xpath('//div[@class="paginator"]//span[@class="next"]/a/@href').extract_first()
        if next_urls:
            yield Request(url=parse.urljoin(response.url, next_urls), callback=self.parse)



