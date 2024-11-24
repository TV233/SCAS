# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MoneybombtestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    SECUCODE = scrapy.Field()
    SECURITY_CODE = scrapy.Field()
    BUSINESS_SCOPE = scrapy.Field()

class StockItem(scrapy.Item):
    stock_id = scrapy.Field()
    stock_name = scrapy.Field()