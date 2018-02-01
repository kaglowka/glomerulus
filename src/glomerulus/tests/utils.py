import os

from scrapy.http import HtmlResponse, Request


def fake_response_with_body(str):
    url = 'http://www.example.com'
    request = Request(url=url)
    response = HtmlResponse(
        url=url,
        encoding='utf-8',
        request=request,
        body=str)
    return response
