# WebScraping_with_Python
Some examples scraping websites mainly using Scrapy framework, in addition to Splash and Selenium.

Crawling with a spider:
Placed in the folder which contains scrapy.cfg: 
  scrapy crawl spider_name -o output_file_name.extension
(we can storage data into .json, .xml, .csv, and others)

Placed on WebScraping_Udemy\worldometers exdecute:
  scrapy crawl countries -o dataset_file.json

Placed on WebScraping_Udemy\tinydeals exdecute:
  scrapy crawl special_offers -o dataset_file.json
