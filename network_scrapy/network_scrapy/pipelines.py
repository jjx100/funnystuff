# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#!/usr/bin/python
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
#from __future__ import unicode_literals

from scrapy.exceptions import DropItem

class CnbetaPipeline(object):
    def process_item(self, item, spider):
        print('cnbeta pipeline reached')
        return DropItem('Stop processing.')
