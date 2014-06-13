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
            'browser' : 'open',
            'show_max' : '10',
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
    @property
    def show_max(self):
        return int(self._config['show_max'])
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
                    #continue
                elif not self.exists(key):
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
    #def move(self, arxiv, dir):
        #print('here2')
        #self._arxivs.get(arxiv).move(dir)
        #print('here2')
        #return
    #
    def set_arxivs(self, arxivs):
        self._arxivs = arxivs
        return
    #
    def set_config(self, conf):
        self._config.update(conf)
        return
    #
    def find(self, *searches, **kwargs):
        printer = True
        if kwargs.has_key('printer'):
            printer = kwargs['printer']
        out = ('-' * 80) + '\n'
        files = []
        for key, item in self._arxivs.iteritems():
            found = True
            for search in searches:
                if not item.find(search):
                    found = False
            if found:
                out += item.__str__() + '\n'
                out += ('-' * 80) + '\n'
                files.append(item.file_title)

            #if item.find(search):
                #out += item.__str__() + '\n'
                #out += ('-' * 80) + '\n'
                #files.append(item.file_title)
        if printer:
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
    def move(self, search, newdir, printer=False):
        arxiv_number = ArXiv().get_arxiv_number(search)
        for key, item in self._arxivs.iteritems():
            found = False
            if item.find(search):
                item.move(newdir)
                found = True
            elif arxiv_number and item.find(arxiv_number):
                item.move(newdir)
                found = True
            if found and printer:
                print '{0}\n{1}'.format('-' * 80, item.__str__())
        return
    #
    def check(self):
        for key, item in self._arxivs.iteritems():
            item.check()
        return
    #
    def delete(self, todel):
        if self.exists(todel):
            number = todel
            if not self._arxivs.has_key(todel):
                number = ArXiv().get_arxiv_number(todel)
            arxiv2del = self._arxivs.pop(number)
            arxiv2del.delete()
            print ' Deleted '.center(80, '-')
            print arxiv2del
            print '-' * 80
            return True
        return False
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



