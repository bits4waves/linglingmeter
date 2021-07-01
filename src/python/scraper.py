import scrapy
import re


def cleanup(s):
    """Remove unwanted characters from string."""
    return re.sub('\s+', ' ', re.sub('\n', '', s)).strip()


class ArticlesSpider(scrapy.Spider):

    name = 'articles'
    start_urls = ['../html/catgut-papers.html']


    def parse(self, response):
        for i, x in \
            enumerate(response.css('div.c02 p b::text').extract()):
            if x.find('Abbot'):
                print(i)
                break
        #     yield {
        #         'author': quote.xpath('span/small/text()').get(),
        #         'text': quote.css('span.text::text').get(),
        #     }

        # next_page = response.css('li.next a::attr("href")').get()
        # if next_page is not None:
        #     yield response.follow(next_page, self.parse)
