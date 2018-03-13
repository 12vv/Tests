# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# import json
# import codecs

from scrapy.pipelines.images import ImagesPipeline

class Test1Pipeline(object):
# class JsonWriterPipeline(object):
#
#     def __init__(self):
#         self.file = codecs.open('items.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        # line = json.dumps(dict(item)) + "\n"
        # self.file.write(line.decode('unicode_escape'))
        return item

# image process
class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
