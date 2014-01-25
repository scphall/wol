import re
from wolArxiv import *
################################################################################

class ArXivs(object):
    """Class container for all arXiv entries"""
    _arxivs = {}
    _config = {}
    def __init__(self):
        self._config = {
            'viewer' : 'open'
        }

    @property
    def viewer(self):
        return _config['viewer']

    def __str__(self):
        out = ('-' * 80) + '\n'
        for key, item in self._arxivs.iteritems():
            out += item.__str__()
            out += ('-' * 80) + '\n'
        return out

    def exists(self, number):
        return number in self._arxivs

    def get(self, number):
        pattern = re.compile('(\d{4}\.\d{4}|\d{7})')
        match = pattern.search(number)
        if not match:
            return False
        if self._arxivs.has_key(match.groups()[0]):
            return self._arxivs.get(match.groups()[0])
        return False

    def add(self, new):
        if not self.exists(new):
            arxiv = ArXiv()
            arxiv.set(new)
            if arxiv.valid:
                self._arxivs.update({arxiv.arxiv : arxiv})
            else:
                print 'Adding {} failed'.format(arxiv.arxiv)
        return

    def move(self, arxiv, dir):
        self._arxivs.get(arxiv).move(dir)
        return

    def set_arxivs(self, arxivs):
        self._arxivs = arxivs

    def find(self, search):
        out = ('-' * 80) + '\n'
        files = []
        for key, item in self._arxivs.iteritems():
            if item.find(search):
                out += item.__str__()
                out += ('-' * 80) + '\n'
                files.append(item.file_title)
        print out
        return files

    def config(self, configurable, configured):
        if self._config.has_key(configurable):
            self._config[configurable] = configured
        else:
            print 'Configurable {} does not exist'.format(configurable)
        return

    def show_config(self):
        out = 'Wol config:\n'
        for key, item in self._config.iteritems():
            out += ' {:10s} {}\n'.format(key, item)
        print out
        return







