import re
import os
import shutil
import urllib
from wolVars import *
from wolHTMLParser import *
################################################################################

def check_dir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
    return
################################################################################

class ArXiv(object):
    """Single arxiv entry class"""
    _arxiv = None
    _version = None
    _title = None
    _directory = None
    _vars = WolVars()
    valid = False
    def __init__(self):
        self._directory = self._vars.default_dir
        return

    @property
    def file_arxiv(self):
        return os.path.join(self._vars.arxiv_dir, '{}.pdf'.format(self._version))

    @property
    def arxiv(self):
        return self._arxiv

    @property
    def file_title(self):
        return os.path.join(self._vars.woldir, self._directory, '{}.pdf'.format(self._title))

    def __str__(self):
        out = '{}\n'.format(self._directory)
        out += '{}'.format(self._title)
        return out

    def find(self, search):
        if self._arxiv.count(search) or self._title.count(search):
            return True
        return False

    def set_arxiv_number(self, number):
        pattern = re.compile('(\d{4}\.\d{4}|\d{7})')
        match = pattern.search(number)
        if not match:
            return False
        self._arxiv = match.groups()[0]
        return True

    def set_title(self, title):
        title = title.replace('\n', '')
        title = title.replace('$', '')
        title = title.replace('  ', ' ')
        title = title.replace('/', '')
        title = title.replace('--gt;', '\\to')
        title = title.replace('-gt;', '\\to')
        self._title = title
        return


    def get_arxiv_details(self):
        url = self._vars.get_arxiv_abs(self.arxiv)
        data = urllib.urlopen(url).read()
        parser = WolHTMLParser()
        parser.feed(data)
        urlname = self._vars.get_arxiv_pdf(self.arxiv)
        self._version = parser.filename
        self.set_title(parser.title)
        return

    def set_by_copy(self, name):
        filename = os.path.split(name)[-1]
        check_dir(self._vars.arxiv_dir)
        shutil.copy(name, os.path.join(self._vars.arxiv_dir, filename))
        return

    def set_by_download(self, name):
        cmd = 'wget -q -U firefox {} -O {}'
        cmd = cmd.format(self._vars.get_arxiv_pdf(name), self.file_arxiv)
        check_dir(self._vars.arxiv_dir)
        os.system(cmd)
        return

    def create_link(self):
        cmd = 'ln -s "{}" "{}"'
        cmd = cmd.format(self.file_arxiv, self.file_title)
        check_dir(os.path.split(self.file_title)[0])
        if not os.path.exists(self.file_title):
            os.system(cmd)
        return

    def set(self, name):
        if not self.set_arxiv_number(name):
            return
        self.get_arxiv_details()
        if os.path.exists(name):
            self.set_by_copy(name)
        else:
            self.set_by_download(name)
        if self._version != '':
            self.create_link()
            self.valid = True
        return

    def move(self, newdir):
        old = self.file_title
        self._directory = newdir
        new = self.file_title
        check_dir(os.path.split(new)[0])
        shutil.move(old, new)
        return


