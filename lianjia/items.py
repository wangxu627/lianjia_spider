# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    lj_action_resblock_id = scrapy.Field()
    lj_action_housedel_id = scrapy.Field()
    detail_url = scrapy.Field()
    title = scrapy.Field()
    total_price = scrapy.Field()
    unit_price = scrapy.Field()
    good_house_tag = scrapy.Field()
    block = scrapy.Field()
    region = scrapy.Field()
    layout = scrapy.Field()
    area = scrapy.Field()
    orientation = scrapy.Field()
    renovation = scrapy.Field()
    floor = scrapy.Field()
    year = scrapy.Field()
    build_type = scrapy.Field()
    star_count = scrapy.Field()
    release_date = scrapy.Field()
