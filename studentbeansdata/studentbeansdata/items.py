# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class StudentbeansdataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Offer_Detail = scrapy.Field()
    Brand_Partner = scrapy.Field()
    Redemption_Type = scrapy.Field()
    Platform = scrapy.Field()



