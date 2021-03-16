from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from apscheduler.schedulers.twisted import TwistedScheduler
from stockscraper.spiders.stockbots import StockbotsSpider

process = CrawlerProcess(get_project_settings())
scheduler = TwistedScheduler()
scheduler.add_job(process.crawl, 'interval', args=[StockbotsSpider], seconds=10)
scheduler.start()
process.start(False)
