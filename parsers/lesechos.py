from baseparser import BaseParser
from BeautifulSoup import BeautifulSoup
from datetime import datetime
import logging
import re

DATE_FORMAT = '%B %d, %Y at %l:%M%P EDT'

class LesEchosParser(BaseParser):
    domains = ['www.lesechos.fr']

    feeder_pages = ['http://www.lesechos.fr/']
    feeder_pat  = '^http://www.lesechos.fr/([a-z-]+/)+[0-9]{12,}-'

    def _parse(self, html):
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES, fromEncoding='utf-8')

        self.meta = soup.findAll('meta')
        self.title = soup.find('meta', attrs={'property':'og:title'}).get('content')
        
        author = soup.find('span', attrs={'class':'auteur'}).find('a')
        if author:
            self.byline = author.getText()
        else:
            self.byline = ''

        self.date = ''
        
        # description = soup.find('div', attrs={'class':re.compile(r'\beditorial\b')}).childGenerator()
        description_text = ''#'\n'.join([p.string for p in description if p])
        
        article = soup.find('div', attrs={'id':'article'})
        
        article_tags = article.findAll(['h2', 'div'], attrs={'class':re.compile(r"^(intertitre|typetitle|texte)$")})
        
        main_body = '\n\n'.join([p.getText() for p in article_tags if p.parent.name == 'btn_impr'])
        
        self.body = '\n'.join([description_text, main_body])

