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
        self.get_content(response)


    def get_content(self, response):

        '''

        possible upgrades: get content  from e.i. <p> <strong> blabla </strong><p>
        '''

        # Indentify main container
        article = self.extract_main_container(response)

        # We get all p inside main_container
        all_pars = article.xpath('.//p/text()').extract()

        # Extract all p likely to be comments inside main_container
        comment_pars = self.extract_comments_inside_main(article)

        # Remove comments from main_container
        content_pars = self.remove_elements(all_pars, comment_pars)

        #Generate data to write
        content = ""
        content += "\n CAŁY ARTYKUŁ --- \n"
        for p in all_pars:
            content += p
        content += "\n KOMENTARZE --- \n"
        for p in comment_pars:
            content += p
        content += "\n KONTENT --- \n"
        for par in content_pars:
            content+=par

        FileStorage().save_data('article', content)


    def extract_main_container(self, response):

        '''
        possible upgrades: class*="post"  "post-content", "main-content"
        '''

        main_container = ['no main container']
        if len(response.css('article')) > 0:
            main_container = response.css('article')[0]
        elif len(response.css('div[id*="post"]')) > 0:
            main_container = response.css('div[id*="post"]')[0]
        # elif len(response.css('div[class*="post"]')) > 0:
        #     main_container = response.css('div[id*="post"]')[0]
        return main_container


    def extract_comments_inside_main(self, main_container):
        return main_container.css('*[id*="comments"] p::text').extract()


    def remove_elements(self, all_elements, trash_elements):
        return_elements = []
        for el in all_elements:
            is_trash = False
            for trash in trash_elements:
                is_trash = False
                if el == trash:
                    is_trash = True
                    break
            if is_trash == False:
                return_elements.append(el)
        return return_elements
