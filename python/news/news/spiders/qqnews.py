# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from news.items import NewsItem
import bs4


class QqnewsSpider(scrapy.Spider):
    name = "qqnews"
    allowed_domains = ["news.qq.com"]
    start_urls = (
        'http://news.qq.com/society_index.shtml',
    )

    def parse(self, response):
        html = response.body
        soup = BeautifulSoup(html)
        nodes_list = soup.find(id="listZone").contents

        print len(nodes_list)

        items = []

        for node in nodes_list:
            if bs4.Tag != type(node):
                continue
            print "type:", type(node)
            # print unicode(node)
            # print "value:", str(node)

            tag_image = node.find("img", class_="picto")
            tag_linkto = node.find("a", class_="linkto")
            print "image:", unicode(tag_image)
            print "linkto:", unicode(tag_linkto)
            item = NewsItem()
            item["detail_url"] = unicode(self.allowed_domains[0] + tag_linkto["href"])
            item["pic_url"] = unicode(tag_image["src"])

            item["title"] = unicode(tag_linkto.text)
            item["sub_title"] = unicode(node.p.text)

            # print "item:", unicode(item).decode()
            items.append(item)
        return items

