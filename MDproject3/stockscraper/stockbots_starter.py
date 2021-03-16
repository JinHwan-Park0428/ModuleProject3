from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from apscheduler.schedulers.twisted import TwistedScheduler
from stockscraper.spiders.stockbots import StockbotsSpider

process = CrawlerProcess(get_project_settings())
scheduler = TwistedScheduler()
scheduler.add_job(process.crawl, 'cron', args=[StockbotsSpider], minute='0,5,10,15,20,25,30,35,40,45,50,55') #원하는 해당 '분' 입력 ex) '5' -> 매시간 5분마다  
scheduler.start()
process.start(False)
