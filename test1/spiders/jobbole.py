# -*- coding: utf-8 -*-
import scrapy
import uniout
from scrapy.http import Request
import urlparse
from test1.items import ArticleItem

import sys
reload(sys)
sys.setdefaultencoding('utf8')


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['http://www.gg-robot.com/']
    start_urls = ['http://www.gg-robot.com/news.html']

    def parse(self, response):
        """
        a. get this page's url (all)
        b. get next page's url
        :param response:
        :return:
        """
        # parse all url in this page
        post_urls = response.xpath('/html/body/div[3]/div[3]/div[2]/ul/li')
        for a in post_urls:
            post_url = a.css('h2 a::attr(href)').extract_first("")
            img_url = a.css('img::attr(src)').extract_first("")
            print post_url, img_url
            yield Request(url=urlparse.urljoin(response.url, post_url), callback=self.parse_detail, meta={"front_image_url":urlparse.urljoin(response.url, img_url)}, dont_filter=True)
        # next page
        next_url = response.xpath('/html/body/div[3]/div[3]/div[3]/a[text()=">>"]/@href').extract_first("").encode('utf-8')

        if next_url:
            print next_url.encode('utf-8')
            yield Request(url=urlparse.urljoin(response.url, next_url), callback=self.parse, dont_filter=True)

        # raw_data = response.xpath('//*[@id="post-110287"]/div[2]/p/text()').extract()[0].strip()
        # data = raw_data.encode('utf-8').replace('·', '').strip()

    def parse_detail(self, response):
        article_item = ArticleItem()
        # details in article
        front_image_url = response.meta.get("front_image_url", "")
        title = response.xpath('/html/body/div[3]/div[2]/div[3]/h2/text()').extract_first("")
        data = response.xpath('/html/body/div[3]/div[2]/div[3]/div[1]/span[1]/text()').extract_first("")
        content = response.xpath('//*[@id="font_class"]/div').extract_first("")
        print title, data, content
        # fill value
        article_item["title"] = title
        article_item["data"] = data
        article_item["content"] = content
        article_item["front_image_url"] = [front_image_url]
        # article_item["front_image_path"] = front_image_path
        article_item["url"] = response.url
        yield article_item
