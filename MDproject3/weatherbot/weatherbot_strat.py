from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from apscheduler.schedulers.twisted import TwistedScheduler
from weatherbot.spiders.weatherbot import WeatherbotsSpider

process = CrawlerProcess(get_project_settings())
scheduler = TwistedScheduler()
scheduler.add_job(process.crawl, 'cron', args=[StockbotsSpider], minute='0,5,10,15,20,25,30,35,40,45,50,55') 
scheduler.start()
process.start(False)