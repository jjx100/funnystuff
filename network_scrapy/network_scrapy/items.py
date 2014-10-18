# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CnbetaItem(scrapy.Item):
    # define the fields for your item here like:
    uid = scrapy.Field()
    title = scrapy.Field()
    introduction = scrapy.Field()
    content = scrapy.Field()
