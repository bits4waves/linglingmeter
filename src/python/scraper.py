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
        series, prefix = None, info
        m = re.findall('(.*)( \(Series II\)$)', info)
        if m:
            prefix = m[0][0]
            n = re.findall('Series (.*)\)$', m[0][1])
            if n:
                series = n[0]

        return series, prefix


    @staticmethod
    def get_pages(info):
        """Return the entry's page numbers."""
        m = re.findall('(.*)([pP]\.? ?[-0-9]+( and [0-9]*)?\.?$)', info)
        if m:
            prefix = m[0][0]
            pages = re.findall('([-0-9]+( and [0-9]*)?)', m[0][1])[0][0]
        else:
            prefix = info
            pages = None

        return pages, prefix


    @staticmethod
    def get_number(info):
        """Return issue number from text."""
        number, prefix = None, info
        for p in ['Number ', 'No\. ?']:
            m = re.findall('(.*)(' + p + ')(\d*)([.,]? ?)$', info)
            if m:
                prefix = m[0][0]
                number = m[0][2]
                break

        return number, prefix


    def parse(self, response):
        entries = response.css('div.c02')
        for entry in entries:
            parts = entry.css('p b::text').extract()

            info = self.get_info(parts)
            vol = self.get_vol_maybe(info)
            if vol is None:
                vol = '0'
            series, prefix = self.get_series(info)
            pages, prefix = self.get_pages(prefix)
            number, prefix = self.get_number(prefix)

            online = entry.css('div.online')
            if online:
                # Journal entries.
                issue_type = 'journal'
                url = online.css('a::attr(href)').extract_first()
                file_id = url[-11:]
                pdf_url = f'https://stacks.stanford.edu/file/druid:{file_id}/CAS_{file_id}.pdf'
                wget_command = f'wget {pdf_url} -O vol-{vol}-number-{number}.pdf'
            else:
                # Article entries.
                issue_type = 'article'
                pdf_url = None
                wget_command = None

            yield {'wget_command': wget_command,
                   'info': info,
                   'type': issue_type,
                   'pdf_url': pdf_url,
                   'vol': vol,
                   'number': number,
                   'series': series,
                   'pages': pages}
