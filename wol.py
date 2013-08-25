#!/usr/bin/python

###############################################################################

"""
wol is named for the most intelligent inhabitant of the Hundred Acre Wood.
He will gladly manage arXiv papers for you.

Setup your WOLDIR to be where you wish, and then begin.
If not set it will use the current directory.
Add an arXiv paper with:
    wol -a 1234.5678
    wol -a /path/to/arxiv/file/1234.*
These will all need a web connection to get the title.
Can specify directory in which to store with
    wol -a 1234.5678 -d Theory
Details of the directory is stored in the $WOLDIR/.wol file, this can be sent
and then immediately added with:
    wol -w new.wol
or update a new .wol with
    wol -u

"""

__title__  = "wol.py"
__author__ = "Sam Hall"
__email__  = "shall@cern.ch"
__version__ = "v1r0"

###############################################################################

import os
import sys
import urllib
import pickle
import glob
from HTMLParser import HTMLParser
from optparse import OptionParser

################################################################################

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
    def get_arxiv_abs(self, number):
        return self.arxiv_abs % number
    def get_arxiv_pdf(self, number):
        return self.arxiv_pdf % number
    def get_lhcb_ana(self, name):
        return self.lhcb_ana % name


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


class RunDotWol():
    """Takes a .wol and gets stuff."""
    details = {}
    def __init__(self, filename):
        f = open(filename, 'rb')
        self.details = pickle.load(f)
    def get_files(self):
        wolvars = WolVars()
        if not os.path.exists(wolvars.arxiv_dir):
            os.mkdir(wolvars.arxiv_dir)
        for key in self.details.keys():
            entry = self.details[key]
            cmd = 'wget -q --user-agent=Lynx %s -O %s/%s.pdf'
            cmd = cmd % (wolvars.get_arxiv_pdf(key),
                         wolvars.arxiv_dir, key)
            os.system(cmd)
            if not os.path.exists('%s/%s' % (wolvars.woldir, entry['dir'])):
                os.mkdir('%s/%s' % (wolvars.woldir, entry['dir']))
            files = os.listdir('%s/%s' % (wolvars.woldir, entry['dir']))
            files = [x for x in files if x.count(key[:key.find('v')])]
            if len(files) == 0:
                cmd = 'ln -s %s/%s.pdf %s/%s/"%s".pdf'
                cmd = cmd % (wolvars.arxiv_dir, key,
                             wolvars.woldir, entry['dir'], entry['title'])
                os.system(cmd)
        return 


def opts():
    """Get options from parser."""
    parser = OptionParser("usage: %prog [options] [args]", epilog=
                          '  mv a b       move a to directory b')
    parser.add_option("-a", "--arxiv", dest="arxiv",
                      help="Input arXiv number")
    parser.add_option("-d", "--dir", dest="directory",
                      help="Directory name")
    parser.add_option("-w", "--wol", dest="read_wol",
                      help="Load a .wol file")
    parser.add_option("-u", "--update", dest="update",
                      action='store_true', default=False,
                      help="Update")
    options, args = parser.parse_args()
    options.mv = []
    if args.count('mv'):
        options.mv.append(args[args.index('mv') + 1])
        options.mv.append(args[args.index('mv') + 2])
        args.pop(args.index('mv') + 2)
        args.pop(args.index('mv') + 1)
        args.pop(args.index('mv'))
    if options.arxiv:
        more_arxiv = []
        for arg in args:
            if arg.split('/')[-1].split('.')[0].isdigit():
                more_arxiv.append(arg)
        more_arxiv.insert(0, options.arxiv)
        options.arxiv = more_arxiv
    return options, args


def get_arxiv(name):
    """Get arXiv from web and title."""
    details = {}
    wolvars = WolVars()
    files = os.listdir(wolvars.arxiv_dir)
    files = [x.replace('.pdf', '') for x in files]
    files = [x[:x.find('v') + 1] for x in files]
    url = wolvars.get_arxiv_abs(name)
    data = urllib.urlopen(url).read()
    parser = LitHTMLParser()
    parser.feed(data)
    urlname = wolvars.get_arxiv_pdf(parser.filename)
    if not os.path.exists('%s/%s' % (wolvars.arxiv_dir, parser.filename)):
        cmd = 'wget -q --user-agent=Lynx %s -O %s/%s.pdf'
        cmd = cmd % (urlname, wolvars.arxiv_dir, parser.filename)
        os.system(cmd)
    parser.title = parser.title.replace('\n', '')
    parser.title = parser.title.replace('$', '')
    parser.title = parser.title.replace('  ', ' ')
    parser.title = parser.title.replace('/', '')
    parser.title = parser.title.replace('--gt;', '\\to')
    details.update({name : {'title' : parser.title,
                            'arxiv' : parser.filename}})
    return details

def arxiv2dir(details, directory):
    """Takes arXiv file and symbolically links it to something useful."""
    wolvars = WolVars()
    key = details.keys()[0]
    if not directory:
        directory = 'papers'
    #directory = '%s/%s' % (wolvars.woldir, directory)
    if not os.path.exists('%s/%s' % (wolvars.woldir, directory)):
        os.mkdir('%s/%s' % (wolvars.woldir, directory))
    details[key]['dir'] = directory
    files = os.listdir(details[key]['dir'])
    files = [x for x in files if x.count(key)]
    if len(files) == 0:
        cmd = 'ln -s %s/%s.pdf %s/%s/"%s".pdf'
        cmd = cmd % (wolvars.arxiv_dir, details[key]['arxiv'],
                     wolvars.woldir, directory, details[key]['title'])
        os.system(cmd)
    return details

def dot_wol_get():
    """Gets details from the .wol at the start."""
    woldot = WolVars().woldot
    all_details = {}
    if not os.path.exists(woldot):
        f = open(woldot, 'wb')
        pickle.dump(all_details, f)
        f.close()
    else:
        f = open(woldot, 'rb')
        all_details = pickle.load(f)
        f.close()
    return all_details
 
def dot_wol_put(all_details):
    """Puts details in the .wol at the start."""
    woldot = WolVars().woldot
    f = open(woldot, 'wb')
    pickle.dump(all_details, f)
    f.close()
    return all_details
 
def setup(options):
    """Setup!"""
    wolvars = WolVars()
    if not os.path.exists(wolvars.woldir):
        os.mkdir(wolvars.woldir)
    if not os.path.exists('%s/arxiv' % wolvars.woldir):
        os.mkdir('%s/arxiv' % wolvars.woldir)
    details = dot_wol_get()
    return details

def move(details, mv):
    """Move file from a to b"""
    wolvars = WolVars()
    arxiv = mv[0].split('/')[-1].replace('[', '')[:9]
    if not details.has_key(arxiv):
        print 'No arXiv file %s in .wol' % arxiv
        return details
    old = details[arxiv]['dir']
    new = mv[1]
    title = details[arxiv]['title']
    details[arxiv]['dir'] = new
    cmd = 'rm -f %s/%s/"%s".pdf' % (wolvars.woldir, old, title)
    os.system(cmd)
    if not os.path.exists('%s/%s' % (wolvars.woldir, new)):
        os.mkdir('%s/%s' % (wolvars.woldir, new))
    cmd = 'ln -s %s/%s.pdf %s/%s/"%s".pdf' % (wolvars.arxiv_dir,
                                              details[arxiv]['arxiv'],
                                              wolvars.woldir, new, title)
    os.system(cmd)
    return details

def main():
    options, args = opts()
    details = setup(options)
    if options.arxiv:
        #options.arxiv = glob.glob(options.arxiv)
        options.arxiv = [x.replace('.pdf', '')  for x in options.arxiv]
        options.arxiv = [x.split('/')[-1] for x in options.arxiv]
        for arxiv in options.arxiv:
            if arxiv.count('v'):
                arxiv = arxiv[:arxiv.find('v')]
            new_details = get_arxiv(arxiv)
            new_details = arxiv2dir(new_details, options.directory)
            details.update(new_details)
    elif options.update:
        rdw = RunDotWol('.wol')
        new_details = rdw.get_files()
        details.update(rdw.details)
    elif options.read_wol:
        rdw = RunDotWol(options.read_wol)
        new_details = rdw.get_files()
        details.update(rdw.details)
    if options.mv:
        details = move(details, options.mv)
    dot_wol_put(details)


if __name__ == "__main__":
    main()
    #'wget https://cds.cern.ch/record/1384141/files/LHCb-ANA-2011-073.pdf'
