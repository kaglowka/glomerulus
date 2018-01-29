# -*- coding: utf-8 -*-
import scrapy
from collections import OrderedDict

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

        article_content, article_comments = self.get_content(response)
        publish_date = self.extract_publish_date(response)

        data = OrderedDict([
            ('url',response.url),
            ('is_fake',"TODO"),
            ('publish_date', publish_date),
            ('content', article_content),
            ('comments', article_comments)]
        )
        self.save_readable_article_data(data)
        return data

    def save_readable_article_data(self, data):
        # Should be somewhere else? TODO better?
        str = ""
        for key, val in data.items():
            str += (key + ": " + val)
            str += "\n"
        str += "\n"
        FileStorage().save_data('readable-article-data', str, flag='a')


    def get_content(self, response):

        # Indentify main container
        article = self.extract_main_container(response)

        # Get all p inside main container
        all_pars = self.extract_main_content(article)

        # Extract all p likely to be comments inside main container
        comment_pars = self.extract_comments_inside_main(article)

        # Remove comments from main content
        content_pars = self.remove_elements(all_pars, comment_pars)


        #Create one string from paragraphs
        content_text = ""
        comments_text = ""

        for par in content_pars:
            content_text+=par

        for par in comment_pars:
            comments_text += par


        return [content_text, comments_text]




    def extract_main_container(self, response):

        # 1st rule -- get 1st article element
        # 2nd rule -- get 1st div whose class attribute value contains "article"
        # 3rd rule -- get 1st div whose id attribute value contains "post" (for blogs)
        # backup -- get body element

        candidate = response.css('article')
        if len(candidate) > 0:
            return candidate[0]

        candidate = response.css('section[class~="article"]')
        if len(candidate) > 0:
            return candidate[0]

        candidate = response.css('div[class~="article"]')
        if len(candidate) > 0:
            return candidate[0]

        candidate = response.css('section[id~="article"]')
        if len(candidate) > 0:
            return candidate[0]

        candidate = response.css('div[id~="article"]')
        if len(candidate) > 0:
            return candidate[0]

        candidate = response.css('div[class*="article"]')
        if len(candidate) > 0:
            return candidate[0]

        candidate = response.css('div[class~="post"]')
        if len(candidate) > 0:
            return candidate[0]

        candidate = response.css('div[id~="post"]')
        if len(candidate) > 0:
            return candidate[0]

        candidate = response.css('div[class*="post"]')
        if len(candidate) > 0:
            return candidate[0]

        candidate = response.css('div[id*="post"]')
        if len(candidate) > 0:
            return candidate[0]

        candidate = response.css('body')[0]

        return candidate



    def extract_main_content(self, main_container):
        content = []

        # Get text form every p (and its every child) inside main container
        all_p_texts = main_container.css('p *::text').extract()
        for p_text in all_p_texts:
            if len(p_text) > 1:
                content.append(p_text)
                print("p: " + p_text)

        print("all_p_texts", all_p_texts)

        # all_p_texts_xpath = main_container.xpath('//p//text()').extract()
        # for p_text in all_p_texts_xpath:
        #     if len(p_text) > 1:
        #         content.append(p_text)
        #         print("p: " + p_text)
        #
        # print("all_p_texts_xpath", all_p_texts_xpath)

        # Get texts longer than 25 chars form all divs inside main container
        all_divs_texts = main_container.css('div::text').extract()
        for div_text in all_divs_texts:
            if len(div_text) > 25:
                div_text = div_text.strip() #remove whitespaces
                content.append(div_text)
                print("div: " + div_text)

        # all_divs_texts_xpath = main_container.xpath('//div//text()').extract()
        # for div_text in all_divs_texts_xpath:
        #     if len(div_text) > 25:
        #         div_text = div_text.strip() #remove whitespaces
        #         content.append(div_text)
        #         print("div: " + div_text)

        print("CONTENT", content)
        return content



    def extract_comments_inside_main(self, main_container):
        comments = []
        # Get all p inside any element whose id attribute contains 'comment'
        all_p_id_comments = main_container.css('*[id*="comment"] p::text').extract()
        for comment in all_p_id_comments:
            comment = comment.strip()
            comments.append(comment)
        all_p_class_comments = main_container.css('*[class*="comment"] p::text').extract()
        for comment in all_p_class_comments:
            comment = comment.strip()
            comments.append(comment)

        all_div_id_comments = main_container.css('*[id*="comment"] div::text').extract()
        for comment in all_div_id_comments:
            comment = comment.strip()
            comments.append(comment)
        all_div_class_comments = main_container.css('*[class*="comment"] div::text').extract()
        for comment in all_div_class_comments:
            comment = comment.strip()
            comments.append(comment)
        return comments


    def remove_elements(self, all_elements, trash_elements):
        return_elements = []
        for el in all_elements:
            is_trash = False
            if el in trash_elements:
                is_trash = True
            if not is_trash:
                return_elements.append(el)
        return return_elements


    # DATE EXTRACTION

    def extract_publish_date(self, response):
        # date = response.css('time::text').extract_first()
        # all_dates = response.css('time::text').extract()
        # if date is not None:
        #     return date

        # TODO: first candidate datetime value

        candidate = response.css('time::text').extract()
        if len(candidate) > 0:
            return candidate[0]

        candidate = response.css('*[class="data"]::text').extract()
        if len(candidate) > 0:
            return candidate[0]


        return "BRAK DATY"