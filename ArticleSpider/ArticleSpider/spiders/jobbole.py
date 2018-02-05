# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import ArticleItem
from ArticleSpider.utils.common import get_md5
import datetime


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
            1获取文章列表页的url并交给scrapy下载后进行解析
            2获取下一页url，交给scrapy下载，下载完成后交给parse
        """
        #解析列表中所有文章url，并交给scrapy
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first()
            post_url = post_node.css("::attr(href)").extract_first()
            yield Request(url=parse.urljoin(response.url,post_url),meta={"front_image_url":image_url},callback=self.parse_detail)

        #提取下一页并交给scrapy
        next_urls = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_urls:
            pass
            #yield Request(url=parse.urljoin(response.url, next_urls), callback=self.parse)



    def parse_detail(self,response):
        article_item = ArticleItem()
        front_image_url = response.meta.get("front_image_url", "")  # 文章封面图
        title = response.css('div.entry-header h1::text').extract_first()
        create_data = response.css('p.entry-meta-hide-on-mobile::text').extract_first().strip().replace("·","").strip()
        praise_nums = response.css('span.vote-post-up h10::text').extract_first()
        fav_nums = response.css(".bookmark-btn::text").extract_first()
        match_re = re.match(".*?(\d+).*", fav_nums)
        if match_re:
            fav_nums = int(match_re.group(1))
        else:
            fav_nums = 0
        comment_nums = response.css("a[href='#article-comment'] span::text").extract_first()
        match_re = re.match(".*?(\d+).*", comment_nums)
        if match_re:
            comment_nums = int(match_re.group(1))
        else:
            comment_nums = 0
        content = response.css('div.entry').extract_first()
        tag_list = response.css('p.entry-meta-hide-on-mobile a::text').extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = ",".join(tag_list)

        article_item['url_object_id'] = get_md5(response.url)
        article_item['title'] = title
        article_item['url'] = response.url
        try:
            create_data = datetime.datetime.strptime(create_data, "%Y/%m/%d").date()
        except Exception as e:
            create_data = datetime.datetime.now().date()
        article_item['create_date'] = create_data
        article_item['front_image_url'] = [front_image_url]
        article_item['praise_nums'] = praise_nums
        article_item['comment_nums'] = comment_nums
        article_item['fav_nums'] = fav_nums
        article_item['tags'] = tags
        article_item['content'] = content
        yield article_item

