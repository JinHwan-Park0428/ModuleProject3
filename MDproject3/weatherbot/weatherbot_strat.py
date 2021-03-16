from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from apscheduler.schedulers.twisted import TwistedScheduler
from weatherbot.spiders.weatherbot import WeatherbotsSpider

process = CrawlerProcess(get_project_settings())
scheduler = TwistedScheduler()
scheduler.add_job(process.crawl, 'interval', args=[WeatherbotsSpider], seconds=10)
scheduler.start()
process.start(False)