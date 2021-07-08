import scrapy
import re


def cleanup(s):
    """Remove unwanted characters from string."""
    return re.sub('\s+', ' ', re.sub('\n', '', s)).strip()


class InfoSpider(scrapy.Spider):

    name = 'info'
    start_urls = ['file:///home/rafa/dev/linglingmeter/src/html/catgut-papers.html']


    @staticmethod
    def get_vol_maybe(info):
        """Return volume number from text."""
        m = re.search('(Vol\. ?)(\d*)', info)
        if m:
            vol = m.group(2)
        else:
            vol = None
        return vol


    def parse(self, response):
        parts = response.css('div.c02 p b::text').extract()
        for i, part in enumerate(parts):
            if i % 2 == 0:
                info = part
            else:
                info = cleanup(info + ' ' + part)

                vol = self.get_vol_maybe(info)

                if i < 162:
                    # Journal entries.
                    type = 'journal'
                else:
                    # Article entries.
                    type = 'article'

                yield {'i': i,
                       'info': info,
                       'type': type,
                       'vol': vol}
