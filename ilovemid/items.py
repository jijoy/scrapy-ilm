# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IlovemidItem(scrapy.Item):
    embed_urls = scrapy.Field()
    title = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    posted_date_time = scrapy.Field()
    tags = scrapy.Field()
    url = scrapy.Field()
    season = scrapy.Field()
    image_url = scrapy.Field()
    image_path = scrapy.Field()
