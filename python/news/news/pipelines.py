# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import scrapy
import hashlib

class NewsPipeline(object):
    def process_item(self, item, spider):
        # print unicode(item)
        print "item"
        return item


class MongoDBPipeline(object):
    def __init__(self, host, port, dbname, user, pwd, collection):
        self.__host = host
        self.__port = int(port)
        self.__dbname = dbname
        self.__user = user
        self.__pwd = pwd
        self.__collection = collection

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get("MONGODB_HOST"),
            port=crawler.settings.get("MONGODB_PORT"),
            dbname=crawler.settings.get("MONGODB_DB"),
            user=crawler.settings.get("MONGODB_USER"),
            pwd=crawler.settings.get("MONGODB_PASSWD"),
            collection=crawler.settings.get("MONGODB_COLLECTION", "qqnews")
        )

    def __connect(self):
        """
        连接数据库，操作数据库之前要先调用这个
        """
        try:
            self._connecttion = pymongo.Connection(self.__host, self.__port)
        except Exception as e:
            print 'connection error:', e
        finally:
            if None == self._connecttion:
                print 'connection fail!'
                return None

        try:
            self._destdb = self._connecttion[self.__dbname]
        except Exception as e:
            print 'get destdb error:', e
        finally:
            if None == self._destdb:
                print 'get destdb fail!'
                return None

        try:
            self._destdb.authenticate(self.__user, self.__pwd)
        except Exception as e:
            print 'authenticate error:', e
            return None

        try:
            self._collection_handle = self._destdb[self.__collection]
        except Exception as e:
            print 'get collection_handel error:', e
        return True

    def open_spider(self, spider):
        self.__connect()

    def close_spider(self, spider):
        self._connecttion.close()

    def process_item(self, item, spider):
        collection_name = str.lower(item.__class__.__name__)
        print "collection name:", collection_name

        if self._collection_handle:
            temp_item = dict(item)
            keystr = temp_item["detail_url"]
            if keystr.find("://") > -1:
                keystr = keystr.split("://")[1]

            id = hashlib.md5(keystr).hexdigest()
            temp_item["_id"] = id
            self._collection_handle.insert(temp_item)
        return item

