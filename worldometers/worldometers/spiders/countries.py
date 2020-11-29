import scrapy
import logging

class CountriesSpider(scrapy.Spider): # it inherit from scrapy.Spider!
    # name must be UNIQUE, two spiders can't have the same name
    name = 'countries' 
    # URL never must have http:// or https://, Scrapy uses http protocol by default
    allowed_domains = ['www.worldometers.info']
    # by default, this URL is created with http://, in this case we'll scrap an httpS web, we add it
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    # parse() method receives the response of the http request
    def parse(self, response):
        # pass -> to do nothing, Python migth need a return in any method because doesn't has types to be 'void'
        countries = response.xpath('//td/a')

        for country in countries:
            # VIDEO 1: get country name and link
            country_name = country.xpath('.//text()').getall()[0] # use xpath fuctions with an object (not a response): .// not //
            country_link = country.xpath('.//@href').getall()[0] # attributes don't need text(): they're always text!
            
            # VIDEO 2: follow each country link -> generator of Requests!

            # absolute_url = f"http://www.worldometers.info{country_link}"
            # absolute_url = response.urljoin(country_link)
            # yield scrapy.Request(url = asolute_url)
            # yield response.follow(url = country_link)

            # VIDEO 3: fetaching data from the secondary response of every followed link
            yield response.follow(url = country_link, 
                                  callback=self.parse_country, 
                                  meta={'country_name' : country_name})

    def parse_country (self, response):
        # logging.info(response.url)
        population_table = response.xpath("(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]//tr")
        country_name = response.request.meta['country_name']
        for row in population_table:
            year = row.xpath('.//td[1]/text()').get()
            population = row.xpath('.//td[2]//text()').get()
            yield {
                'country_name' : country_name,
                'year' : year,
                'population' : population
            }