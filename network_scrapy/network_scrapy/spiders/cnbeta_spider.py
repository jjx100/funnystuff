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

import re

class DmozSpider(CrawlSpider):
    name = "cnbeta"
    allowed_domains = ["cnbeta.com"]
    start_urls = [
        "http://www.cnbeta.com/"
    ]
    rules = (Rule(LinkExtractor(allow=['http://www.cnbeta.com/articles/\d+.htm']), callback='parse_article'),)

    def parse_article(self, response):
        print('response url', response.url)

        item = CnbetaItem()
        item['uid'] = response.url.split('/')[-1][:-4]
        #print('uid = ', item['uid'])


        item['title'] = response.xpath('/html/head/meta[5]/@content').extract()[0].encode('utf-8')
        print('title = ', item['title'])

        xpath_article_date = response.xpath('/html/body/section[@class="wrapper"]//section[@class="main_content_left"]//div[@class="title_bar"]/span[@class="date"]')
        article_date = xpath_article_date.xpath('./text()').extract()[0].encode('utf-8')
        item['publish_date'] = article_date        
        print(item['publish_date'])

        xpath_article_content = response.xpath('/html/body/section[@class="wrapper"]//section[@class="main_content_left"]/article/div/section[@class="article_content"]')
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

        #Parse javascript code to get token and SN.
        #Token and SN will be used as form data in post request to retrieve comments data.
        token_js = response.xpath('//script[@type="text/javascript"]/text()').extract()[0]
        token_pattern = re.compile('TOKEN:"(.*)"')        
        match_token = re.search(token_pattern, token_js) 
        if match_token:
            item['token'] = match_token.group(1)
            print('token: ', item['token'])

        sn_js = response.xpath('//script[@type="text/javascript" and @charset="utf-8"]/text()').extract()[2]        
        sn_pattern = re.compile('SN:"(.*)"')
        match_sn = re.search(sn_pattern, sn_js)
        if match_sn:
            item['SN'] = match_sn.group(1)
            print('SN: ', item['SN'])

        yield item
