import os
from HTMLParser import HTMLParser

class WolVars:
    """Keeps all variables and pathnames and urls etc."""
    arxiv_abs = 'http://arxiv.org/abs/%s'
    arxiv_pdf = 'http://arxiv.org/pdf/%s.pdf'
    lhcb_ana = 'https://cds.cern.ch/record/1384141/files/%s'
    woldir = ''
    arxiv_dir = ''
    woldot = ''
    def __init__(self):
        self.woldir = os.getenv('WOLDIR')
        if not self.woldir:
            self.woldir = os.getcwd()
        self.arxiv_dir = '%s/arxiv' % self.woldir
        self.woldot = '%s/.wol' % self.woldir
    #
    def get_arxiv_abs(self, number):
        return self.arxiv_abs % number
    #
    def get_arxiv_pdf(self, number):
        return self.arxiv_pdf % number
    #
    def get_lhcb_ana(self, name):
        return self.lhcb_ana % name


class WolDictHandler:
    details = {}
    recents = []
    template = ''
    def __init__(self):
        self.template = ' arXiv:      %(version)s\n'
        self.template += ' Directory:  %(dir)s\n'
        self.template += ' %(title_print)s\n'
        self.template += (80 * '-')
        return
    #
    def setup(self, details, recents=[]):
        self.details = details
        self.recents = recents
    #
    def get(self, arxiv, key=None):
        if key is None:
            try:
                return self.details[arxiv]
            except KeyError:
                print 'No arXiv number %s in wol' % arxiv
                raise
        else:
            try:
                return self.details[arxiv][key]
            except KeyError:
                print 'No arXiv number %s with key %s in wol' % arxiv, key
                raise
        return
    #
    def add(self, arxiv, vers, directory, title):
        title = title.replace('\n', '')
        title = title.replace('$', '')
        title = title.replace('  ', ' ')
        title = title.replace('/', '')
        title = title.replace('--gt;', '\\to')
        title = title.replace('-gt;', '\\to')
        split = title.split(' ')[1:]
        title_print = split.pop(0)
        n = 1
        for word in split:
            if (len(title_print) + len(word)) > 75 * n:
                title_print += '\n  '
                n += 1
            title_print += ' %s' % word
        self.details[arxiv] = {'version' : vers,
                               'dir' : directory,
                               'title' : title,
                               'title_print' : title_print}
        return
    #
    def has(self, key):
        return self.details.has_key(key)
    #
    def put(self, key, var, value):
        self.get(key)[var] = value
        return
    #
    def remove(self, arxiv):
        try:
            self.details.pop(arxiv)
        except KeyError:
            print 'No arXiv number %s in wol' % arxiv
            sys.exit(0)
        return
    #
    def move(self, arxiv, directory):
        if self.get(arxiv)['dir'] == directory:
            return False
        self.details[arxiv]['dir'] = directory
        return True
    #
    def append(self, arxiv, new_details):
        if self.has(arxiv):
            return False
        else:
            self.add(arxiv, new_details['version'],
                     new_details['dir'],
                     new_details['title'])
        return True
    #
    def printer(self, arxiv):
        info = self.template % self.get(arxiv)
        return


class LitHTMLParser(HTMLParser):
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
        #print 'Start', tag
    def handle_endtag(self, tag):
        if tag == 'title':
            self.get_title = False
        if tag == 'a':
            self.get_filename = False
        #print 'End', tag
    def handle_data(self, data):
        if self.get_title:
            self.title += data
        elif self.get_filename:
            if data.startswith('arXiv:'):
                self.filename = data.replace('arXiv:', '')
        #print 'Data', data
