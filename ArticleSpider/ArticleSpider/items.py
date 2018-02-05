# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose, Join
import re
import datetime
from scrapy.loader import ItemLoader

# 字符串转换时间方法
def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()

    return create_date


# 获取字符串内数字方法
def get_nums(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums


# 去除标签中提取的评论方法
def remove_comment_tags(value):
    if "评论" in value:
        return ""
    else:
        return value


# 直接获取值方法
def return_value(value):
    return value

# 排除none值


def exclude_none(value):
    if value:
        return value
    else:
        value = "无"
        return value
class ArticleItemLoader(ItemLoader):
    #自定义itemloader
    default_output_processor = TakeFirst()


class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field(
        input_processor=MapCompose(date_convert),
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field(
        # 使用自定义的outprocessor覆盖原始的take first 使得image_url是一个列表。
        output_processor=MapCompose(return_value)
    )
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        # list使用逗号连接
        output_processor=Join(",")
    )
    content = scrapy.Field()
    #crawl_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
               insert into jobbole_article(title, url, create_date, fav_nums, front_image_url, front_image_path,
               praise_nums, comment_nums, tags, content)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE content=VALUES(fav_nums)
           """

        fron_image_url = ""
        # content = remove_tags(self["content"])

        if self["front_image_url"]:
            fron_image_url = self["front_image_url"][0]
        params = (self["title"], self["url"], self["create_date"], self["fav_nums"],
                  fron_image_url, self["front_image_path"], self["praise_nums"], self["comment_nums"],
                  self["tags"], self["content"])
        return insert_sql, params



# class JobBoleArticleItem(scrapy.Item):
#     title = scrapy.Field()
#     create_date = scrapy.Field()
#     url = scrapy.Field()
#     url_object_id= scrapy.Field()
#     front_image_url = scrapy.Field()
#     front_image_path = scrapy.Field()
#     praise_nums = scrapy.Field()
#     comment_nums = scrapy.Field()
#     fav_nums = scrapy.Field()
#     tags = scrapy.Field()
#     content = scrapy.Field()
#
#     def get_insert_sql(self):
#         insert_sql = """
#             insert into jobbole_article(title, url, url_object_id,create_date, fav_nums, front_image_url, front_image_path,
#             praise_nums, comment_nums, tags, content)
#             VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE fav_nums=VALUES(fav_nums),praise_nums=VALUES(praise_nums),comment_nums=VALUES(comment_nums)
#         """
#         params = (
#             self["title"],
#             self["url"],
#             self["url_object_id"],
#             self["create_date"],
#             self["fav_nums"],
#             self["front_image_url"],
#             self["front_image_path"],
#             self["praise_nums"],
#             self["comment_nums"],
#             self["tags"],
#             self["content"],
#         )
#         return insert_sql, params



