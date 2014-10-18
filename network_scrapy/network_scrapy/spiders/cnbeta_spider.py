#!/usr/bin/python
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
#from __future__ import unicode_literals

import scrapy
from network_scrapy.items import CnbetaItem
from scrapy.spider import Spider
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

class DmozSpider(CrawlSpider):
    name = "cnbeta"
    allowed_domains = ["cnbeta.com"]
    start_urls = [
        "http://www.cnbeta.com/"
    ]
    rules = (Rule(LinkExtractor(allow=['http://www.cnbeta.com/articles/\d+.htm']), callback='parse_article'),)

    def parse_article(self, response):
        print('parse_article invoked: response url', response.url)

        item = CnbetaItem()
        item['uid'] = response.url.split('/')[-1][:-4]
        #print('uid = ', item['uid'])

        item['title'] = response.xpath('/html/head/meta[5]/@content').extract()[0].encode('utf-8')
        print('title = ', item['title'])

        xpath_article_content = response.xpath('/html/body/div[@class="wrapper"]/section[@class="main_content"]/section[@class="main_content_left"]/article/div/section[@class="article_content"]')
        introduction_text = xpath_article_content.xpath('./div[@class="introduction"]//p//text()').extract()
        print('Introduction:')
        text=''
        for text_seg in introduction_text:
            text += text_seg
        item['introduction'] = text
        print(item['introduction'])
        print()

        content_text = xpath_article_content.xpath('./div[@class="content"]//p//text()').extract()
        print('Content:')
        text=''
        for text_seg in content_text:
            text += text_seg
        item['content'] = text
        print(item['content'])
        print()

