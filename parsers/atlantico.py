from baseparser import BaseParser
from BeautifulSoup import BeautifulSoup, Comment
from datetime import datetime
import logging
import re

DATE_FORMAT = '%B %d, %Y at %l:%M%P EDT'
MONTH = {'janvier':1,u'f\xe9vrier':2,'mars':3,'avril':4,'mai':4,'juin':6,'juillet':7,u'ao\xfbt':8,'septembre':9,'octobre':10,'novembre':11,u'd\xe9cembre':12}

class AtlanticoParser(BaseParser):
    domains = ['www.atlantico.fr']

    feeder_pages = ['http://www.atlantico.fr/']
    feeder_pat  = '^http://www.atlantico.fr/(?!breves|dossier)([a-z]+)/[a-z0-9-]+-[0-9]{6,}.html$'

    def _parse(self, html):
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES, fromEncoding='utf-8')

        comments = soup.findAll(text=lambda text:isinstance(text, Comment))
        [comment.extract() for comment in comments]
        [script.extract() for script in soup.findAll('script')]

        self.meta = soup.findAll('meta')
        self.title = soup.find('meta', attrs={'property':'og:title'}).get('content')
        
        try:
            byline = soup.find('div', attrs={'id':'bio-auteur'}).find('a', attrs={'class':'profile-link'}).getText()
            self.byline = byline
        except AttributeError:
            self.byline = ''

        try:
            p_tags = soup.find('div', attrs={'id':'content-body'}).findAll('p')
        except AttributeError:
            self.real_article = False
            return

        datestr = soup.find('div', attrs={'id':'content'}).find('div', attrs={'class':'metas'}).getText()
        datestr = datestr.replace(u'Publi\xe9 le ', '')
        dateComponents = datestr.split(' ')
        date = str(dateComponents[0]) + '-' + str(MONTH[dateComponents[1]]) + '-' + str(dateComponents[2])
        datet = datetime.strptime(date, '%d-%m-%Y')
        self.date = datet.strftime(DATE_FORMAT)
        
        chapo = soup.find('p', attrs={'class':re.compile(r"\bchapo\b")}).getText()
        
        main_body = '\n\n'.join([p.getText() for p in p_tags])
        
        self.body = '\n\n'.join([chapo, main_body])

