import json
import re
from urllib.parse import urljoin, urlencode
import scrapy

import scraperConfig


API_KEY = scraperConfig.API_KEY


def get_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url


class AmazonSpider(scrapy.Spider):
    name = 'amazon'

    def start_requests(self):
        url = 'https://www.amazon.com/s?' + urlencode({'k': self.query})    # self.query for passing param in ScrapyRT
        yield scrapy.Request(url=get_url(url), callback=self.parse_keyword_responses)

    def parse_keyword_responses(self, response):
        products = response.xpath('//*[@data-asin]')
        for product in products:
            asin = product.xpath('@data-asin').extract_first()
            product_url = f'https://www.amazon.com/dp/{asin}'
            yield scrapy.Request(url=get_url(product_url), callback=self.parse_product_page, meta={'asin': asin})
        next_page = response.xpath('//li[@class="a-last"]/a/@href').extract_first()
        page_limit = 0
        if page_limit != 1 and next_page:   # only scrape 1 page if available
            url = urljoin("https://www.amazon.com", next_page)
            page_limit += 1
            yield scrapy.Request(url=get_url(url), callback=self.parse_keyword_responses)

    def parse_product_page(self, response):
        asin = response.meta['asin']
        title = response.xpath('//*[@id="productTitle"]/text()').extract_first()
        image = re.search('"large":"(.*?)"', response.text).groups()[0]
        rating = response.xpath('//*[@id="acrPopover"]/@title').extract_first()
        number_of_reviews = response.xpath('//*[@id="acrCustomerReviewText"]/text()').extract_first()
        price = response.xpath('//*[@id="priceblock_ourprice"]/text()').extract_first()
        if not price:
            price = response.xpath('//*[@data-asin-price]/@data-asin-price').extract_first() or \
                    response.xpath('//*[@id="price_inside_buybox"]/text()').extract_first() or \
                    response.xpath('//*[@class="a-offscreen"]/text()').extract_first()  # this new one works

        temp = response.xpath('//*[@id="twister"]')
        sizes = []
        colors = []
        if temp:
            s = re.search('"variationValues" : ({.*})', response.text).groups()[0]
            json_acceptable = s.replace("'", "\"")
            di = json.loads(json_acceptable)
            sizes = di.get('size_name', [])
            colors = di.get('color_name', [])
        bullet_points = response.xpath('//*[@id="feature-bullets"]//li/span/text()').extract()
        url = 'https://www.amazon.com/dp/' + asin
        yield {'Title': title, 'MainImage': image, 'Rating': rating, 'NumberOfReviews': number_of_reviews,
               'Price': price, 'AvailableSizes': sizes, 'AvailableColors': colors, 'BulletPoints': bullet_points,
               'URL': url}
