import scrapy
from stockscraper.items import StockscraperItem

class StockbotsSpider(scrapy.Spider):
    name = 'stockbots'
    custom_settings = {'JOBDIR': 'crawl_my_stock_bots1'}
    allowed_domains = ['finance.yahoo.com/quote/BTC-USD?p=BTC-USD&.tsrc=fin-srch',
                       'finance.yahoo.com/quote/ETH-USD?p=ETH-USD&.tsrc=fin-srch',
                       'finance.yahoo.com/quote/LTC-USD?p=LTC-USD&.tsrc=fin-srch']
    start_urls = ['https://finance.yahoo.com/quote/BTC-USD?p=BTC-USD&.tsrc=fin-srch',
                  'https://finance.yahoo.com/quote/ETH-USD?p=ETH-USD&.tsrc=fin-srch',
                  'https://finance.yahoo.com/quote/LTC-USD?p=LTC-USD&.tsrc=fin-srch']

    def parse(self, response):
        quantity = response.xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[4]/td[2]/span/text()').extract()
        Price = response.xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div/span[1]/text()').extract()
        days_range = response.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[3]/td[2]/text()').extract()
        title = response.xpath('//*[@id="quote-header-info"]/div[2]/div[1]/div[1]/h1/text()').extract()
        ratio = response.xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div/span[2]/text()').extract()
        open_price = response.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[2]/td[2]/span/text()').extract()

        for row in zip(quantity, Price, days_range,  title,ratio, open_price):
            item = StockscraperItem()
            item['quantity'] = row[0]
            item['Price'] = row[1]
            item['days_range'] = row[2]
            item['title'] = row[3]
            item['ratio'] = row[4]
            item['open_price'] = row[5]

            yield item