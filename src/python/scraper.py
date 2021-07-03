import scrapy
import re


def cleanup(s):
    """Remove unwanted characters from string."""
    return re.sub('\s+', ' ', re.sub('\n', '', s)).strip()


class ArticlesSpider(scrapy.Spider):

    name = 'articles'
    start_urls = ['file:///home/rafa/dev/linglingmeter/src/html/catgut-papers.html']


    def parse(self, response):
        everything = response.css('div.c02 p b::text').extract()
        for i, x in enumerate(everything):
            if i < 162: continue
            if i % 2 == 0:
                y = x
            else:
                y = y + ' ' + x
                yield {'i': i, 'y': cleanup(y)}
