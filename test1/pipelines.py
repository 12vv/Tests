# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import MySQLdb

from scrapy.pipelines.images import ImagesPipeline
# use scrapy's function to handle json
from scrapy.exporters import JsonItemExporter

class Test1Pipeline(object):
# class JsonWriterPipeline(object):
#
#     def __init__(self):
#         self.file = codecs.open('items.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        # line = json.dumps(dict(item)) + "\n"
        # self.file.write(line.decode('unicode_escape'))
        return item


class JsonWithEncodingPipeline(object):
    # 自定义导出json文件
    def __init__(self):
        self.file = codecs.open('article_s.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        print lines
        return item

    def spider_closed(self, spider):
        self.file.close()


class JsonExporterPipeline(object):
    # 调用scrapy提供的json exporter导出json文件
    def __init__(self):
        # 二进制方式打开文件
        self.file = open('article.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('localhost', 'Garrick', 'Akashi12', 'article_spider', charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into article(title, url, url_object_id, date_t, content)
            VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item['title'], item['url'], item['url_object_id'], item['date_t'], item['content']))
        self.conn.commit()


# image process
class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for p, value in results:
            image_file_path = value['path']
        item["front_image_path"] = image_file_path

        return item
