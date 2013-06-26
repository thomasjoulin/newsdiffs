from baseparser import BaseParser
from BeautifulSoup import BeautifulSoup
from datetime import datetime

DATE_FORMAT = '%B %d, %Y at %l:%M%P EDT'

class LeFigaroParser(BaseParser):
    domains = ['www.lefigaro.fr']

    feeder_pages = ['http://www.lefigaro.fr/']
    feeder_pat  = '^http://www.lefigaro.fr/[^/photos][a-zA-Z-]+/\d{4}/\d{2}/\d{2}/[a-zA-Z0-9-]+.php$'

    def _parse(self, html):
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES, fromEncoding='utf-8')

        try:
            p_tags = soup.find('div', attrs={'itemprop':'articleBody'}).findAll('p')
        except AttributeError:
            self.real_article = False
            return

        main_body = '\n'.join([p.getText() for p in p_tags])

        self.body = main_body

        self.meta = soup.findAll('meta')

        self.title = soup.find('meta', attrs={'property':'og:title'}).get('content')
        
        author = soup.find('p', attrs={'itemprop':'name'})
        
        if author:
            self.byline = author.getText()
        else:
            self.byline = ''

        datestr = soup.find('time', attrs={'itemprop':'datePublished'}).get('datetime')
        new_dt = datestr[:19]
        datet = datetime.strptime(new_dt, '%Y-%m-%dT%H:%M:%S')
        self.date = datet.strftime(DATE_FORMAT)
        


