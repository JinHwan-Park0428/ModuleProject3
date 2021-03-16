import scrapy
from weatherbot.items import WeatherbotItem


class WeatherbotsSpider(scrapy.Spider):
    name = 'weatherbot'
    custom_settings = {'JOBDIR': 'crawl_weatherbots1'}
    allowed_domains = ['yahoo.com/news/weather/south-korea/seoul/seoul-1132599/']
    start_urls = ['https://www.yahoo.com/news/weather/south-korea/seoul/seoul-1132599/']

    def parse(self, response):
        temperature = response.xpath('//*[@id="Lead-1-WeatherLocationAndTemperature"]/div/section[2]/div/div[3]/span[1]/text()').extract()
        humidity = response.xpath('//*//*[@id="weather-detail"]/div/div[1]/div/div[2]/ul/li[2]/div[2]/text()').extract()
        high_temp = response.xpath('//*//*[@id="Lead-1-WeatherLocationAndTemperature"]/div/section[2]/div/div[2]/span[1]/text()').extract()        
        low_temp = response.xpath('//*//*[@id="Lead-1-WeatherLocationAndTemperature"]/div/section[2]/div/div[2]/span[2]/text()').extract()
        title = response.xpath('//*[@id="Lead-1-WeatherLocationAndTemperature"]/div/section[1]/div[1]/div/h1/text()').extract()
        wind = response.xpath('//*[@id="weather-wind"]/div/div[1]/div[2]/div/p/span/text()').extract()
        weather = response.xpath('//*[@id="Lead-1-WeatherLocationAndTemperature"]/div/section[2]/div/div[1]/span[2]/text()').extract()
        sun_rise = response.xpath('//*[@id="weather-sun-moon"]/div/div[2]/div[2]/span[1]/text()').extract()
        sun_set = response.xpath('//*[@id="weather-sun-moon"]/div/div[2]/div[2]/span[2]/text()').extract()

        for row in zip(temperature,humidity,high_temp,low_temp,title,wind,weather,sun_rise,sun_set):
            item = WeatherbotItem()
            item['temperature'] = row[0]              
            item['humidity'] = row[1]    
            item['high_temp'] = row[2]        
            item['low_temp'] = row[3]           
            item['title'] = row[4]   
            item['wind'] = row[5]     
            item['weather'] = row[6] 
            item['sun_rise'] = row[7]
            item['sun_set'] = row[8]

            yield item
