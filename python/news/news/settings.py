# -*- coding: utf-8 -*-

# Scrapy settings for news project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'news'

SPIDER_MODULES = ['news.spiders']
NEWSPIDER_MODULE = 'news.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'news (+http://www.yourdomain.com)'



ITEM_PIPELINES = ['news.pipelines.MongoDBPipeline', ]

MONGODB_HOST = "ds035723.mongolab.com"
MONGODB_PORT = 35723
MONGODB_DB = "news"
MONGODB_COLLECTION = "qqnews"
MONGODB_USER = "user_news"
MONGODB_PASSWD = "news"