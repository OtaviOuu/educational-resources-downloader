# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EducationalresourcesdownloaderItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    edition = scrapy.Field()
    cover = scrapy.Field()
    pass
