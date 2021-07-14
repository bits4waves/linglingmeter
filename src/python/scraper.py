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
    def get_number(info):
        """Return issue number from text."""
        number = None
        for p in ['Number ', 'No\. ?']:
            m = re.search(p + '(\d*)', info)
            if m:
                number = m.group(1)

        return number


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
            number = self.get_number(info)

            yield {'info': info,
                   'type': issue_type,
                   'url': url,
                   'vol': vol,
                   'number': number}
