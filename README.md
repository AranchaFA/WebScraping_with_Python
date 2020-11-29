# WebScraping_with_Python
Some examples scraping websites mainly using Scrapy framework, in addition to Splash and Selenium.

I have worked with Anaconda along all this projects (more information here: https://www.anaconda.com/products/individual).
We must have Scrapy installed in the Anaconda's environment we will work in (how to install here: https://docs.scrapy.org/en/latest/intro/install.html).


Crawling with a spider:
Placed in the folder which contains scrapy.cfg: 
  scrapy crawl spider_name -o output_file_name.extension
(we can storage data into .json, .xml, .csv, and others)

Placed on WebScraping_Udemy\worldometers exdecute:
  scrapy crawl countries -o dataset_file.json

Placed on WebScraping_Udemy\tinydeals exdecute:
  scrapy crawl special_offers -o dataset_file.json
