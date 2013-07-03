from baseparser import BaseParser
from BeautifulSoup import BeautifulSoup, Comment
from datetime import datetime
import logging
import re
import nltk

DATE_FORMAT = '%B %d, %Y at %l:%M%P EDT'
def print_hierchy(tag):
    for child in tag.findAll():
        print(child.name)
        print_hierchy(child.findAll())

class LeParisienParser(BaseParser):
    domains = ['www.leparisien.fr']

    feeder_pages = ['http://www.leparisien.fr/']
    feeder_pat  = '^http://www.leparisien.fr(/(?!espace-premium|diaporama|videos)([a-z0-9-]+))+-\d{2}-\d{2}-\d{4}-\d{7,}\.php$'

    def visible_text(self, element):
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
            return ''
        result = re.sub('<!--.*-->|\r|\n', '', str(element), flags=re.DOTALL)
        result = re.sub('\s{2,}|&nbsp;', ' ', result)
        return result

    def _parse(self, html):
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES, fromEncoding='utf-8')

        [no_impr.extract() for no_impr in soup.findAll('btn_noimpr')]
        
        try:
            content = soup.find('div', attrs={'id':'content'})
            body = nltk.clean_html(content.renderContents())
        except AttributeError:
            self.real_article = False
            return
        
        self.meta = soup.findAll('meta')
        self.title = soup.find('meta', attrs={'property':'og:title'}).get('content')
        
        author_block = soup.find('p', attrs={'class':'auteurPubli'})
        
        if author_block:
            author = author_block.getText().strip().split('|', 1)[0].strip()
            if u'Publi' not in author:
                self.byline = author
            else:
                self.byline = ''
        else:
            self.byline = ''

        self.date = ''
        
        self.body = body.decode('utf8')
        #nltk.clean_html(content.renderContents().encode('utf8'))

