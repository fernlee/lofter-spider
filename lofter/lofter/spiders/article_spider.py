# -*- coding:utf-8 -*-
"""

__author__ = "zhangyu"

"""
import logging

from scrapy import Spider, Request

from lofter.items import LofterItem

import requests as req
import time

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("lofter")


class Lofter(Spider):
    name = "lofter"

    start_urls = ["http://www.lofter.com/tag/%E5%8F%B6%E5%91%A8/total?page=9"]
    def parse(self, response):
        # 获取下一页
        next_page = response.xpath("//a[@class='w-sbtn w-sbtn-1']/@href").extract_first()
        if next_page:
            # page_number = next_page.split('=')[1]
            # if int(page_number)%5 == 0:
            # print("start timer at page: " + next_page)
            # time.sleep(10) 

            next_url = response.urljoin(next_page)
            logger.info("下一页的链接地址:{}".format(next_url))
            yield Request(next_url, callback=self.parse)

        # 获取文章title url
        # title_urls = response.xpath("//div[@class='text']/h2/a/@href").extract()
        # 获取tag页面的文章title url
        title_urls = response.xpath("//a[@class='isayc']/@href").extract()
        authors = response.xpath("//div[@class='w-who']/a[@class='ptag']/text()").extract()
        
        # 归档页面文章title url
        # title_urls = response.xpath("//li[@class='text']/a/@href").extract()
        # title_urls = ["http://napolundeqiancengmian.lofter.com/post/1ed5586b_112a2d38"]
        for i in range(len(title_urls)):
            logger.info("当前访问的文章地址:{}".format(title_urls[i]))
            print(authors[i])
            yield Request(title_urls[i], callback=self.save_article, meta={'author': authors[i]})

    def save_article(self, response):
        title = response.xpath("//h2/a/text()").extract_first()
        author = response.meta['author']
        if title != None:
            title = author + '-' + title
        else:
            # date = response.xpath("//a[@class='date']/text()").extract_first()
            # if date == None:
            #     date = response.xpath("//div[@class='date']/a/text()").extract_first()
            title_prefix = 'img-' + author

            description = response.xpath("//div[@class='text']/p/text()").extract_first()
            if description == None:
                tags = (' ').join(response.xpath("//a[@class='tag']/text()").extract())
                title = title_prefix + '-' + tags
            else:
                title = title_prefix + '-' + description
        title = title.replace('/','|');
        title_url = response.url
        
        content = req.get(title_url).content
        lofter_item = LofterItem()
        lofter_item['title'] = title
        lofter_item['content'] = content
        yield lofter_item
