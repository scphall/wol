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
    #
    @property
    def file_arxiv(self):
        return os.path.join(self._vars.arxiv_dir, '{}.pdf'.format(self._version.replace('/', '_')))
    #
    @property
    def arxiv(self):
        return self._arxiv
    #
    @property
    def file_title(self):
        return os.path.join(self._vars.woldir, self._directory, '{}.pdf'.format(self._title))
    #
    @property
    def web_address(self):
        return self._vars.get_arxiv_abs(self.arxiv)
    #
    @staticmethod
    def get_arxiv_number(number):
        pattern = re.compile('(\d{4}\.\d{4}|[\w-]+/\d{7})')
        match = pattern.search(number)
        if not match:
            return False
        return match.groups()[0]
    #
    def __str__(self):
        out = '{}{}'.format(self._version.ljust(40), self._directory.rjust(40))
        title = self._title.replace('[{}] '.format(self.arxiv).replace('/', ''), '')
        line1 = False
        for line in re.findall('.{1,78}(?:\s|$)', title):
            out += '\n'
            if line1: out += '  '
            out += line
            line1 = True
        return out
    #
    def find(self, search):
        title = self._title.replace('[{}] '.format(self.arxiv), '')
        pattern = re.compile(search)
        search1 = pattern.search(self._arxiv)
        search2 = pattern.search(title)
        search3 = pattern.search(self._directory)
        if (search1 or search2 or search3):
            return True
        return False
    #
    def set_arxiv_number(self, number):
        number = self.get_arxiv_number(number)
        if number:
            self._arxiv = number
            return True
        return False
    #
    def set_title(self, title):
        pattern = re.compile('\$|\s{2,}|/')
        title = pattern.sub('', title)
        pattern = re.compile('\t|\n')
        title = pattern.sub(' ', title)
        pattern = re.compile('-+gt;')
        title = pattern.sub('to', title)
        self._title = title
        return
    #
    def get_arxiv_details(self):
        url = self._vars.get_arxiv_abs(self.arxiv)
        data = urllib.urlopen(url).read()
        parser = WolHTMLParser()
        parser.feed(data)
        urlname = self._vars.get_arxiv_pdf(self.arxiv)
        self._version = parser.filename
        self.set_title(parser.title)
        return
    #
    def set_by_copy(self, name):
        filename = os.path.split(name)[-1]
        check_dir(self._vars.arxiv_dir)
        if not os.path.exists(os.path.join(self._vars.arxiv_dir,
                                           filename.replace('/', '_'))):
            shutil.copy(name, os.path.join(self._vars.arxiv_dir,
                                           filename.replace('/', '_')))
        return
    #
    def set_by_download(self, name):
        cmd = 'wget -q -U firefox {} -O {}'
        cmd = cmd.format(self._vars.get_arxiv_pdf(name), self.file_arxiv)
        check_dir(self._vars.arxiv_dir)
        os.system(cmd)
        return
    #
    def create_link(self):
        cmd = 'ln -s "{}" "{}"'
        cmd = cmd.format(self.file_arxiv, self.file_title)
        check_dir(os.path.split(self.file_title)[0])
        if not os.path.exists(self.file_title):
            os.system(cmd)
        return
    #
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
    #
    def move(self, newdir):
        old = self.file_title
        self._directory = newdir
        new = self.file_title
        check_dir(os.path.split(new)[0])
        shutil.move(old, new)
        return
    #
    def check(self):
        if not os.path.exists(self.file_arxiv):
            self.set_by_download(self._arxiv)
        if not os.path.exists(self.file_title):
            self.create_link()
    #
    def delete(self):
        if os.path.exists(self.file_title):
            os.remove(self.file_title)
        if os.path.exists(self.file_arxiv):
            check_dir(self._vars.del_dir)
            shutil.move(
                self.file_arxiv,
                os.path.join(self._vars.del_dir, '{}.pdf'.format(self._version.replace('/', '_')))
            )
        return
################################################################################

