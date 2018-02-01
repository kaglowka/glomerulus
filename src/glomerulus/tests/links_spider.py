from unittest import TestCase

from glomerulus.tests.utils import fake_response_with_body
from links_spider import LinksSpider


class LinkSpiderTests(TestCase):

    article_content = 'Lorem ipsum ' * 100

    def testMultipleNestedDivs(self):
        spider = LinksSpider()
        site = '''
            <div><div><div> {} </div></div></div>
        '''.format(self.article_content)

        extracted_content, extracted_comment = spider.get_content(fake_response_with_body(site))
        self.assertEquals(self.article_content.strip(), extracted_content.strip())

    # # failing;
    # def testTwoCandidateDivs(self):
    #     spider = LinksSpider()
    #     site = '''
    #         <div>
    #         <article><div> xyz </div></article>
    #         <div><div> {} </div></div>
    #         </div>
    #     '''.format(self.article_content)
    #
    #     extracted_content, extracted_comment = spider.get_content(fake_response_with_body(site))
    #     self.assertEquals(self.article_content.strip(), extracted_content.strip())

