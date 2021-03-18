# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WeatherbotItem(scrapy.Item):

    temper = scrapy.Field()
    humid= scrapy.Field()
    low_temp = scrapy.Field()
    high_temp = scrapy.Field()
    title = scrapy.Field()
    wind = scrapy.Field()
    weather = scrapy.Field()

