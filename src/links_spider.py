# -*- coding: utf-8 -*-
import scrapy

from  glomerulus.config import LINKS_PATH
from  glomerulus.io import FileStorage


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
        #print("TUTAJ: " + response.css('title::text').extract_first())
        #return [{'xyz': 'sdff'}]
        self.get_paragraphs2(response)


    def get_paragraphs2(self, response):
        article = response.css('article')[0]
        content = "ARTYKUŁ: "

        all_pars = article.xpath('.//p/text()').extract()
        comment_pars = article.css('section[id*="comments"] p::text').extract()

        content += "\n TREŚĆ --- \n"
        for p in all_pars:
            content += p
        content += "\n KOMENTARZE --- \n"
        for p in comment_pars:
            content += p

        content_pars = []
        content += "\n KONTENT --- \n"
        for par in all_pars:
            for comment_par in comment_pars:
                is_comment = False
                if par == comment_par:
                    is_comment = True
                    break
            if is_comment == False:
                content_pars.append(par)
                content += par

        FileStorage().save_data('article', content)

    def get_paragraphs(self, response):
        article = response.css('article')[0]
        content = "ARTYKUŁ: "
        for p in article.xpath('.//p/text()').extract():
            content += p
        all_pars = []
        comment_pars = []

        content += "\n TREŚĆ --- \n"
        for p in article.xpath('.//p/text()').extract():
            all_pars.append(p)
            content += p
        content += "\n KOMENTARZE --- \n"
        for p in article.css('section[id*="comments"] p::text').extract():
            comment_pars.append(p)
            content += p
        content_pars = []
        content += "\n KONTENT --- \n"
        for par in all_pars:
            for comment_par in comment_pars:
                is_comment = False
                if par == comment_par:
                    is_comment = True
                    break
            if is_comment == False:
                content_pars.append(par)
                content += par

        FileStorage().save_data('article', content)