import scrapy
import re

def cleanup(s):
    """Remove unwanted characters from string."""
    return re.sub('\s+', ' ', re.sub('\n', '', s)).strip()


class InfoSpider(scrapy.Spider):

    name = 'info'
    start_urls = ['file:///home/rafa/dev/linglingmeter/src/html/catgut-papers.html']


    @staticmethod
    def get_info(parts):
        """Return the entry's main data."""
        try:
            return cleanup(parts[0])
        except Exception as e:
            raise RuntimeError('Could not extract article info.')


    @staticmethod
    def get_vol_maybe(info):
        """Return volume number from text."""
        m = re.search('(Vol\. ?)(\d*)', info)
        if m:
            vol = m.group(2)
        else:
            vol = None
        return vol


    @staticmethod
    def get_series(info):
        """Return series number from text."""
        prefix, series = info, None
        m = re.findall('(.*)( \(Series II\)$)', info)
        if m:
            prefix = m[0][0]
            n = re.findall('Series (.*)\)$', m[0][1])
            if n:
                series = n[0]

        return prefix, series


    @staticmethod
    def get_number(info):
        """Return issue number from text."""
        number = None
        for p in ['Number ', 'No\. ?']:
            m = re.findall('(' + p + ')(\d*)', info)
            if m:
                number = m[0][-1]
                if len(m) > 1:
                    number += ' (+)'

        return number


    @staticmethod
    def get_pages(info):
        """Return the entry's page numbers."""
        m = re.findall('(.*)(p\.? ?[-0-9]+\.?$)', info)
        if m:
            prefix = m[0][0]
            pages = re.findall('[-0-9]+', m[0][1])[0]
        else:
            prefix = info
            pages = None

        return prefix, pages


    def parse(self, response):
        entries = response.css('div.c02')
        for entry in entries:
            online = entry.css('div.online')
            if online:
                # Journal entries.
                issue_type = 'journal'
                url = online.css('a::attr(href)').extract_first()
            else:
                # Article entries.
                issue_type = 'article'
                url = None

            parts = entry.css('p b::text').extract()

            info = self.get_info(parts)
            vol = self.get_vol_maybe(info)
            prefix, series = self.get_series(info)
            prefix, pages = self.get_pages(prefix)
            number = self.get_number(prefix)

            yield {'info': info,
                   'type': issue_type,
                   'url': url,
                   'vol': vol,
                   'number': number,
                   'series': series,
                   'pages': pages}
