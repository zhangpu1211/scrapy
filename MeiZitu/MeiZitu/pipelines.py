# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request

class MeizituPipeline(object):
    def process_item(self, item, spider):
        return item

class ArticleImagePipeline(ImagesPipeline):
    # 重写该方法可从result中获取到图片的实际下载地址
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        title = item['name']
        image_guid = request.url.split('/')[-1]
        filename = 'full/{0}/{1}'.format(title, image_guid)
        return filename

    def get_media_requests(self, item, info):
        """
        :param item: spider.py中返回的item
        :param info:
        :return:
        """
        for img_url in item['imgs_url']:
            referer = item['url']
            yield Request(img_url, meta={'item': item,
                                         'referer': referer})