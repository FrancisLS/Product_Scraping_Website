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
        urls = ['https://www.amazon.com/s?',
                'https://www.walmart.com/search?']
        # urls = ['https://www.amazon.com/s?']
        #urls = ['https://www.walmart.com/search?']
        for i in urls:
            if i == 'https://www.amazon.com/s?':
                url = 'https://www.amazon.com/s?' + urlencode({'k': self.query})    # self.query for passing param in ScrapyRT
                yield scrapy.Request(url=get_url(url), callback=self.parse_keyword_responses)
            elif i == 'https://www.walmart.com/search?':
                url = 'https://www.walmart.com/search?' + urlencode({'q': self.query})
                yield scrapy.Request(url=get_url(url), callback=self.walmart_parse_keyword_responses)

    def parse_keyword_responses(self, response):
        products = response.xpath('//*[@data-asin]')
        for product in products:
            asin = product.xpath('@data-asin').extract_first()
            product_url = f'https://www.amazon.com/dp/{asin}'
            yield scrapy.Request(url=get_url(product_url), callback=self.parse_product_page, meta={'asin': asin})
        #next_page = response.xpath('//li[@class="a-last"]/a/@href').extract_first()
        next_page = response.css('a.s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator::attr(href)').extract_first()
        if next_page and 'page=3' not in next_page:   # only scrape 1 page if available
            url = urljoin("https://www.amazon.com", next_page)
            yield scrapy.Request(url=get_url(url), callback=self.parse_keyword_responses)

    def walmart_parse_keyword_responses(self, response):
        #products_url = response.css('a.absolute.w-100.h-100.z-1::attr(href)').extract()[2:] # get every product href
        # links. Exclude first two with trackers.
        products_url = []
        for url in response.css('a.absolute.w-100.h-100.z-1::attr(href)').extract():
            if 'photos3.walmart' in url:    # this one sometimes first in search result. Ignore it
                continue
            url = url.split('/ip')  # remove trackers by separating it with '.../ip/<product name>
            products_url.append(url[-1])    # only get the element in list with '/<product name>'
        for product_url in products_url:
            product_url = f'https://www.walmart.com/ip{product_url}'
            yield scrapy.Request(url=get_url(product_url), callback=self.walmart_parse_product_page, meta={'product_url': product_url})
        '''
        next_page = response.css('a.sans-serif.ph1.pv2.w4.h4.border-box.bg-white.br-100.b--solid.ba.mh2-m.db.tc.'
                                 'no-underline.b--light-gray::attr(href)').extract()
        page_limit = 0
        if page_limit != 1 and next_page:   # only scrape 1 page if available
            url = urljoin('https://walmart.com/', next_page)
            page_limit += 1
            yield scrapy.Request(url=get_url(url), callback=self.walmart_parse_product_page)
        '''

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

    def walmart_parse_product_page(self, response):
        title = response.css('h1.f3.b.lh-copy.dark-gray.mt1.mb2::text').extract_first()
        image = response.css('img.db::attr(src)').extract()[-1]
        rating = response.css('span.f7.rating-number::text').extract_first()  # format is '(x.x)'
        number_of_reviews = response.css('a.f7.dark-gray.pl1.underline::text').extract_first()    # format is 'x review'
        price = response.css('span[itemprop]::text').extract()[-1]  # formal is '$x.x'
        temp = ''
        sizes = []
        colors = []
        bullet_points = ''
        url = response.meta['product_url']
        yield {'Title': title, 'MainImage': image, 'Rating': rating, 'NumberOfReviews': number_of_reviews,
               'Price': price, 'AvailableSizes': sizes, 'AvailableColors': colors, 'BulletPoints': bullet_points,
               'URL': url}
