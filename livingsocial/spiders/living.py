#! -*- coding: utf-8 -*-

"""
Web Scraper Project

Scrape data from a regularly updated website livingsocial.com and
save to a database (postgres).

Scrapy spider part - it actually performs scraping.
"""

from scrapy import Spider
from scrapy.loader.processors import MapCompose, Join
from scrapy.loader import ItemLoader 

from livingsocial.items import LivingSocialDeal


class LivingSocialSpider(Spider):
    """
    Spider for regularly updated livingsocial.com site, San Francisco page
    """
    name = "living"
    allowed_domains = ["livingsocial.com"]
    start_urls = ["https://www.livingsocial.com/cities/15-san-francisco"]

    deals_list_xpath = '//li[@dealid]'
    item_fields = {
        'title': './/a/div[@class="deal-details"]/h2/text()',
        'link': './/a/@href',
        'location': './/a/div[@class="deal-details"]/p[@class="location"]/text()',
        'original_price': './/a/div[@class="deal-prices"]/div[@class="deal-strikethrough-price"]/div[@class="strikethrough-wrapper"]/text()',
        'price': './/a/div[@class="deal-prices"]/div[@class="deal-price"]/text()',
    }

    def parse(self, response):
        """
        Default callback used by Scrapy to process downloaded responses

        Testing contracts:
        @url http://www.livingsocial.com/cities/15-san-francisco
        @returns items 1
        @scrapes title link

        """

        # iterate over deals
        for deal in response.xpath(self.deals_list_xpath):
            l = ItemLoader(item = LivingSocialDeal(), selector = deal)
            l.default_input_processor = MapCompose(lambda p : p.replace('\n          ', ''))
            l.default_output_processor = Join()
            
            # iterate over fields and add xpaths to the loader
            for field, xpath in self.item_fields.items():
                try:
                    l.add_xpath(field, xpath, MapCompose(float))
                except:
                    l.add_xpath(field, xpath)
            yield l.load_item()




