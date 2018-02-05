# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from MeiZitu.items import MeizituItem

class MeiZituSpider(scrapy.Spider):
    name = 'image'
    allowed_domains = ['meizitu.com']
    start_urls = ['http://www.meizitu.com/tag/keai_64_1.html']

    def parse(self, response):
        nodes = response.css('.wp-list .tit a')
        for node in nodes:
            url = node.css('::attr(href)').extract_first().strip()
            yield Request(url=parse.urljoin(response.url, url), callback=self.parse_detail)

        index = response.css('#wp_page_numbers li a::text').extract()
        if '下一页' in index:
            next_urls = response.css('#wp_page_numbers li a')[-2].css('a::attr(href)').extract_first()
            yield Request(url=parse.urljoin(response.url, next_urls),callback=self.parse)

    def parse_detail(self, response):
        item = MeizituItem()

        name = response.css('.postmeta h2 a::text').extract_first()
        imgs_url = response.css('.postContent p img::attr(src)').extract()
        item['name'] = name
        item['imgs_url'] = imgs_url
        item['url'] = response.url
        yield item