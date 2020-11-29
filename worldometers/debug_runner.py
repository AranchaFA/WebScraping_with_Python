import scrapy
# to launch process
from scrapy.crawler import CrawlerProcess
# to extract the settings we'll work with
from scrapy.utils.project import get_project_settings
# the class of the spider we'll debug
from worldometers.spiders.countries import CountriesSpider

# 1- DEFINE BREAKPOINTS in CountriesSpider class
# 2- START DEBUGGING this current file as Python file

# create a process with the project's settings and the spider we're going to debug
process = CrawlerProcess(settings=get_project_settings())
process.crawl(CountriesSpider)
# execute crawling process
process.start()