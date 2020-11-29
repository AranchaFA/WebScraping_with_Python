import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']
    # start_urls = ['https://www.imdb.com/search/title/?groups=top_250&sort=user_rating']
    domain_url = 'https://www.imdb.com/search/title/?groups=top_250&sort=user_rating'
    # to assigns user agent, we need to set it not only in start_request method (because it's applied only at first)
    # but also in rules we'll define (with process_request we can execute a custom method in which we can redefine
    # custom parameters for our requests, such as header's user agent!)
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'

    # to set an allowed valid user-agent, overide start_requests method
    def start_requests(self):
        # this time we don't pass any callback
        yield scrapy.Request(url=self.domain_url, headers={'User-Agent':self.user_agent})

    # LinkExtractor(allow=r'Items/') -> allow expresions that contain 'Items/' (r'...' means reg.exp.)
    # LinkExtractor(deny=r'Items/') 
    # LinkExtractor(restrict_xpaths=('//a[@class="active"/@href'))
    # LinkExtractor(restrict_css=('CSSExpression')) 
    # ORDER AFFECTS THE BEHAVE!! If we place first the Rule to follow the next page, it'll be executed automatically
    # at the begining -> navigate to second page -> execute second Rule -> scrap all data in second page -> and so on...
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3[@class='lister-item-header']/a"), callback='parse_item', follow=True,
                            process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="(//a[@class='lister-page-next next-page'])[2]"), 
                            process_request='set_user_agent')
    )

    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        yield {
            'title' : response.xpath("//div[@class='title_wrapper']/h1/text()").get().strip(),
            'year' : response.xpath("//span[@id='titleYear']/a/text()").get(),
            'duration' : response.xpath("normalize-space((//time)[1]/text())").get(),
            'genre' : response.xpath("(//div[@class='subtext']/a)[1]/text()").get(),
            'rating' : response.xpath("//div[@class='ratingValue']/strong/@title").get(),
            'movie_url' : response.url
            # ,'user-agent' : response.request.headers['User-Agent']
        }
        '''
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        return item
        '''
