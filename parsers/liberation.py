from baseparser import BaseParser
from BeautifulSoup import BeautifulSoup
from datetime import datetime

DATE_FORMAT = '%B %d, %Y at %l:%M%P EDT'

class LiberationParser(BaseParser):
    domains = ['www.liberation.fr']

    feeder_pages = ['http://www.liberation.fr/']
    feeder_pat  = '^http://www.liberation.fr/[a-z]+/\d{4}/\d{2}/\d{2}/[^commentaires]'

    def _parse(self, html):
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES, fromEncoding='utf-8')

        try:
            p_tags = soup.find('div', attrs={'itemprop':'articleBody'}).findAll('p')
        except AttributeError:
            self.real_article = False
            return
        self.meta = soup.findAll('meta')

        self.title = soup.find('meta', attrs={'property':'og:title'}).get('content')
        
        authors = soup.find('div', attrs={'itemprop':'author'}).findAll('strong')
        
        if authors:
            self.byline = ', '.join([author.getText() for author in authors])
        else:
            self.byline = ''

        datestr = soup.find('time', attrs={'itemprop':'datePublished'}).get('datetime')
        new_dt = datestr[:19]
        datet = datetime.strptime(new_dt, '%Y-%m-%dT%H:%M:%S')
        self.date = datet.strftime(DATE_FORMAT)
        
        description = soup.find('h2', attrs={'itemprop':'description'})
        if description:
            description_text = description.getText()
        else:
            description_text = ''
        
        main_body = '\n\n'.join([p.getText() for p in p_tags])
        
        self.body = '\n'.join([description_text, main_body,])

