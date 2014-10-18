# -*- coding: utf-8 -*-

# Scrapy settings for network_scrapy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'network_scrapy'

SPIDER_MODULES = ['network_scrapy.spiders']
NEWSPIDER_MODULE = 'network_scrapy.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
DOWNLOAD_DELAY = 0.25
RANDOMIZE_DOWNLOAD_DELAY = True
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'

