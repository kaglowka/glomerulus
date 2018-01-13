# -*- coding: utf-8 -*-
import scrapy

from glomerulus.config import LINKS_PATH
from glomerulus.io import FileStorage


class LinksSpider(scrapy.Spider):
    name = 'links'

    no_links_fallback = [
        'http://warszawa.wyborcza.pl/warszawa/7,54420,21426713,sklep-z-papierosami-dla-dzieci-juz-otwarty-a-tam-punkt-informacyjny.html?disableRedirects=true'
    ]

    def start_requests(self):
        # Read URLs from a file and search only these URLs...
        requests = []
        for url in FileStorage().get_data(LINKS_PATH):
            requests.append(scrapy.Request(url))

        # If there are no links in links file, use a basic URL
        if len(requests) == 0:
            for url in self.no_links_fallback:
                requests.append(scrapy.Request(url))
        return requests

    def parse(self, response):
        # Extract structured data and return a dictionary of values to save/use
        return [{'xyz': 'sdff'}]