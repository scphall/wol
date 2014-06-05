import re
import os
from wolArxiv import *
################################################################################

class ArXivs(object):
    """Class container for all arXiv entries"""
    _arxivs = {}
    _config = {}
    def __init__(self):
        self._config = {
            'viewer' : 'open',
            'browser' : 'open'
        }
        return
    #
    @property
    def viewer(self):
        return self._config['viewer']
    #
    @property
    def browser(self):
        return self._config['browser']
    #
    def __str__(self):
        out = ('-' * 80) + '\n'
        for key, item in self._arxivs.iteritems():
            out += item.__str__()
            out += ('-' * 80) + '\n'
        return out
    #
    def __len__(self):
        return len(self._arxivs)
    #
    def exists(self, number):
        if self._arxivs.has_key(number):
            return True
        number = ArXiv().get_arxiv_number(number)
        if not number:
            return False
        return self._arxivs.has_key(number)
    #
    def get(self, number):
        if self.exists(number):
            number = ArXiv().get_arxiv_number(number)
            return self._arxivs.get(number)
        return False
    #
    def add(self, new):
        if type(new) == ArXivs:
            print 80 * '-'
            for key, item in new._arxivs.iteritems():
                if not item.get_arxiv_number(key):
                    print 'Paper is not from arXiv'
                    print item, '\n', 80 * '-'
                    continue
                if not self.exists(key):
                    item.check()
                    self._arxivs.update({key : item})
                    print item, '\n', 80 * '-'
        else:
            if not self.exists(new):
                arxiv = ArXiv()
                arxiv.set(new)
                if arxiv.valid:
                    self._arxivs.update({arxiv.arxiv : arxiv})
                else:
                    print 'Adding {} failed'.format(arxiv.arxiv)
        return
    #
    def move(self, arxiv, dir):
        self._arxivs.get(arxiv).move(dir)
        return
    #
    def set_arxivs(self, arxivs):
        self._arxivs = arxivs
        return
    #
    def set_config(self, conf):
        self._config = conf
        return
    #
    def find(self, search):
        out = ('-' * 80) + '\n'
        files = []
        for key, item in self._arxivs.iteritems():
            if item.find(search):
                out += item.__str__() + '\n'
                out += ('-' * 80) + '\n'
                files.append(item.file_title)
        print out
        return files
    #
    def find_arxivs(self, search):
        out = ('-' * 80) + '\n'
        files = []
        for key, item in self._arxivs.iteritems():
            if item.find(search):
                out += item.__str__() + '\n'
                out += ('-' * 80) + '\n'
                files.append(item)
        print out
        return files
    #
    def config(self, configurable, configured):
        if self._config.has_key(configurable):
            self._config[configurable] = configured
        else:
            print 'Configurable {} does not exist'.format(configurable)
        return
    #
    def show_config(self):
        out = 'Wol config:'
        for key, item in sorted(self._config.iteritems()):
            out += '\n {:10s} {}'.format(key, item)
        print out
        return
    #
    def move(self, search, newdir):
        out = ('-' * 80) + '\n'
        for key, item in self._arxivs.iteritems():
            if item.find(search):
                item.move(newdir)
                out += item.__str__() + '\n'
                out += ('-' * 80) + '\n'
        print out
    #
    def check(self):
        for key, item in self._arxivs.iteritems():
            item.check()
        return
    #
    def delete(self, todel):
        #print "HERE"
        print todel
        print self.exists(todel)
        if self.exists(todel):
            number = todel
            if not self._arxivs.has_key(todel):
                number = ArXiv().get_arxiv_number(todel)
            arxiv2del = self._arxivs.pop(number)
            arxiv2del.delete()
            print 'Deleted {}'.format(number)
        return
    #
    def put(self, path, title, dir):
        arxiv = ArXiv()
        arxiv.put(path, title, dir)
        self._arxivs.update({arxiv.arxiv : arxiv})
        print 80 * '-'
        print arxiv
        print 80 * '-'
        return

################################################################################



