import scrapy
import logging

# THIS WEB SITE DOESN'T ALLOW ROBOT WEB SCRAPPING IF WE DON'T SPECIFY AN ALLOWED USER-AGENT
# (we can obtain browsers user-agent on dev_tools>network>search in any GET request's headers)

# We need to change ROBOTSTXT_OBEY = False in settings.py

# To set a specific user agent FOR THE WHOLE PROJECT, on settings.py:
#    set it in USER_AGENT=... or in DEFAULT_REQUEST_HEADERS = {...,'User-Agent': ..., ...}

# # To set a specific user agent FOR THis single spider:
# 1- overide start_requests method, returning a customized scrapy.Request with a headers parameter containing
#    the apropiate 'User-Agent' value.
# 2- do the same with the scrapy.Request (customize it's headers) when we scrap recursively inside parse() method

class SpecialOffersSpider(scrapy.Spider):
    name = 'special_offers'
    allowed_domains = ['www.cigabuy.com']
    # start_urls = ['https://www.cigabuy.com/consumer-electronics-c-56_75.html']
    domain_url = 'https://www.cigabuy.com/consumer-electronics-c-56_75.html'
    custom_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}

    # to set an allowed valid user-agent, overide start_requests method
    def start_requests(self):
        yield scrapy.Request(url=self.domain_url, callback=self.parse, headers=self.custom_headers)

    def parse(self, response):
        # settings.py -> FEED_EXPORT_ENCODING = 'utf-8'
        for product in response.xpath("//div[@class='p_box_wrapper']"):
            yield {
                'title' : product.xpath(".//a[@class='p_box_title']/text()").get(),
                'url' : response.urljoin(product.xpath(".//a[@class='p_box_title']/@href").get()),
                'discounted_price' : product.xpath(".//div[@class='p_box_price']/span[1]/text()").get(),
                'original_price' : product.xpath(".//div[@class='p_box_price']/span[2]/text()").get()
            }
        # if there is a link (pagination button) to the next page
        next_page = response.xpath("//a[@class='nextPage']/@href").get()
        if (next_page):
            yield scrapy.Request(url=next_page, callback=self.parse, headers= self.custom_headers)