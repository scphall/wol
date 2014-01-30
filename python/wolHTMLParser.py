################################################################################
from HTMLParser import HTMLParser
################################################################################

class WolHTMLParser(HTMLParser):
    """Parses HTML and keeps title and filename."""
    title = ''
    filename = ''
    get_title = False
    get_filename = False
    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            self.get_title = True
        if tag == 'a':
            self.get_filename = True
        return
    #
    def handle_endtag(self, tag):
        if tag == 'title':
            self.get_title = False
        if tag == 'a':
            self.get_filename = False
        return
    #
    def handle_data(self, data):
        if self.get_title:
            self.title += data
        elif self.get_filename:
            if data.startswith('arXiv:'):
                self.filename = data.replace('arXiv:', '')
        return
    #

################################################################################
