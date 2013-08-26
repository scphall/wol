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
    def __init__(self, details, recents=[]):
        self.details = details
        self.recents = recents
        return
    #
    def get(self, arxiv):
        try:
            return self.details[arxiv]
        except KeyError:
            print 'No arXiv number %s in wol' % arxiv
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
        self.details[arxiv] = {'version' : vers,
                               'dir' : directory,
                               'title' : title}
        return
    #
    def remove(self, arxiv):
        try:
            self.details.pop(arxiv)
        except KeyError:
            print 'No arXiv number %s in wol' % arxiv
            raise
        return
    #
    def move(self, arxiv, directory):
        if self.get(arxiv)['dir'] == directory:
            return False
        self.details[arxiv]['dir'] = directory
        return True
 

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
