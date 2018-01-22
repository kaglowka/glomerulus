from links_spider import LinksSpider
from glomerulus.io import FileStorage
import os

from scrapy.crawler import CrawlerProcess

fs = FileStorage()
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'FEED_FORMAT': 'json',
    'FEED_URI': os.path.join(fs.get_data_path(), 'articles.json')
})

process.crawl(LinksSpider)
process.start() # the script will block here until the crawling is finished
