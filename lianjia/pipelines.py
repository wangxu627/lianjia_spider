# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from datetime import datetime
import pymongo


class LianjiaJsonLinePipeline:
    def process_item(self, item, spider):
        return item


class LianjiaMongoDBPipeline:
    def __init__(self, mongo_uri, mongo_db, mongo_collection):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection

    @classmethod
    def from_crawler(cls, crawler):
        # 从 settings 中读取配置
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
            mongo_collection=crawler.settings.get('MONGO_COLLECTION'),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.mongo_collection]

    def close_spider(self, spider):
        # 在爬虫结束时关闭连接
        self.client.close()

    def process_item(self, item, spider):
        doc = {
            **dict(item),
            # 'area': clean_number_with_chinese(item["area"]),
            # 'unit_price': clean_number_with_chinese(item["unit_price"]),
            # 'total_price': clean_number_with_chinese(item["total_price"]),
            # 'star_count': clean_number_with_chinese(item["star_count"]),
            "created_at": datetime.now()
        }
        self.collection.insert_one(doc)
        return item
    
