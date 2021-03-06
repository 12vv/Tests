# -*- coding: utf-8 -*-
import scrapy
import uniout
from scrapy.http import Request
import urlparse
import datetime
from test1.items import ArticleItem

from scrapy.loader import ItemLoader

from test1.utils.common import get_md5

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
        date_t = response.xpath('/html/body/div[3]/div[2]/div[3]/div[1]/span[1]/text()').extract_first("")
        content = response.xpath('//*[@id="font_class"]/div').extract_first("")
        print title, date_t
        # fill value
        article_item["url_object_id"] = get_md5(response.url)
        article_item["title"] = title
        try:
            date_t = datetime.datetime.strptime(date_t, "%Y-%m-%d %H:%M").date()
        except Exception as e:
            date_t = datetime.datetime.now().date()
        article_item["date_t"] = date_t
        article_item["content"] = content
        article_item["front_image_url"] = [front_image_url]
        # article_item["front_image_path"] = front_image_path
        article_item["url"] = response.url

        # 通过ItemLoader加载item
        # item_loader = ItemLoader(item=ArticleItem(), response=response)
        # # item_loader.add_css("title", "")
        # item_loader.add_xpath("title", '/html/body/div[3]/div[2]/div[3]/h2/text()')
        # item_loader.add_value("url", response.url)
        # item_loader.add_value("url_object_id", get_md5(response.url))
        #
        # article_item = item_loader.load_item()

        yield article_item
