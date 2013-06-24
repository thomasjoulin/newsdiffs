from baseparser import BaseParser
from BeautifulSoup import BeautifulSoup
from datetime import datetime

DATE_FORMAT = '%B %d, %Y at %l:%M%P EDT'

class LeMondeParser(BaseParser):
    domains = ['www.lemonde.fr']

    feeder_pages = ['http://www.lemonde.fr/']
    feeder_pat  = '^http://www.lemonde.fr/[a-zA-Z]+/article/\d{4}/\d{2}/\d{2}'

    def _parse(self, html):
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES, fromEncoding='utf-8')

        self.meta = soup.findAll('meta')

        self.title = soup.find('meta', attrs={'property':'og:title'}).get('content')
        
        author = soup.find('span', attrs={'itemprop':'author'})
        
        if author:
            self.byline = author.getText()
        else:
            self.byline = ''

        datestr = soup.find('time', attrs={'itemprop':'datePublished'}).get('datetime')
        new_dt = datestr[:19]
        datet = datetime.strptime(new_dt, '%Y-%m-%dT%H:%M:%S')
        self.date = datet.strftime(DATE_FORMAT)
        
        p_tags = soup.find('div', attrs={'id':'articleBody'}).findAll('p')
        main_body = '\n'.join([p.getText() for p in p_tags])
        
        self.body = main_body

