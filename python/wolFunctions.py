################################################################################
"""
Contains all basic functions that are used repeatedly.

"""
################################################################################
import pickle
import urllib
import sys
import os
from wolVars import *
from wolHTMLParser import *
from wolDictHandler import *
################################################################################

def arxiv_format(string):
    string = string.replace('.pdf', '')
    string = string.split('/')
    arxiv = string[-1]
    if arxiv.count('v'):
        arxiv = arxiv[:arxiv.find('v')]
    if arxiv.count(']'):
        arxiv = arxiv.replace('[', '')
        arxiv = arxiv[:arxiv.find(']')]
    if len(arxiv) == 7 and len(string) > 1:
        arxiv = '/'.join([string[-2], arxiv])
    return arxiv
################################################################################

def is_arxiv(arxiv):
    check = arxiv.split('.')
    accept = True
    if len(check) != 2:
        accept = False
    elif not check[0].isdigit() or not check[1].isdigit():
        accept = False
    elif len(check[0]) != 4 or len(check[1]) != 4:
        accept = False
    return accept
################################################################################

def is_arxiv_old(arxiv):
    check = arxiv.split('/')
    accept = True
    if len(check) == 2:
        if check[0].isdigit() or not check[1].isdigit():
            accept = False
        elif len(check[1]) != 7:
            accept = False
    elif len(check) == 1:
        if not len(check[0]) > 7:
            accept = False
        elif not check[0][-7:].isdigit():
            accept = False
    return accept
################################################################################

def str2arxiv(string):
    arxiv = arxiv_format(string)
    if not is_arxiv(arxiv) and not is_arxiv_old(arxiv):
        print '%s (from %s) is not a valid arxiv number' % (arxiv, string)
        sys.exit(0)
    return arxiv
################################################################################

def put_dot_wol(handler):
    """Puts handler from the .wol"""
    woldot = WolVars().woldot
    f = open(woldot, 'wb')
    handler = pickle.dump(handler, f)
    f.close()
    return
################################################################################

def get_dot_wol(filename=None):
    """Gets details from the .wol"""
    woldot = WolVars().woldot
    dict_handler = WolDictHandler()
    if filename is None:
        filename = woldot
    if not os.path.exists(filename):
        dict_handler.setup({}, [], {})
        f = open(filename, 'wb')
        pickle.dump(dict_handler, f)
        f.close()
    else:
        f = open(filename, 'rb')
        details = pickle.load(f)
        dict_handler.setup(details.details, details.recents, details.config)
        f.close()
    return dict_handler
################################################################################

def arxiv_file(arxiv, files):
    if type(files) is str:
        files = [files]
    files = [str2arxiv(x) for x in files]
    arxiv = str2arxiv(arxiv)
    if files.count(arxiv):
        return True
    return False
################################################################################

def get_arxiv_from_web(details):
    cmd = 'wget -q --user-agent=Lynx %s -O %s/%s.pdf'
    wolvars = WolVars()
    cmd = cmd % (wolvars.get_arxiv_pdf(details['version_get']),
                 wolvars.arxiv_dir,
                 details['version'])
    os.system(cmd)
    return
################################################################################

def check_directory(directory):
    directory = directory.rstrip('/.')
    if not os.path.exists(directory):
        os.mkdir(directory)
    return
################################################################################

def get_arxiv_details(arxiv):
    wolvars = WolVars()
    url = wolvars.get_arxiv_abs(arxiv)
    data = urllib.urlopen(url).read()
    parser = WolHTMLParser()
    parser.feed(data)
    urlname = wolvars.get_arxiv_pdf(parser.filename)
    return (parser.filename, parser.title)
################################################################################

def create_ln(details):
    wolvars = WolVars()
    files = os.listdir('%s/%s' % (wolvars.woldir, details['dir']))
    files = [str2arxiv(x) for x in files]
    #arxiv = str2arxiv(details['version'])
    if not files.count(str2arxiv(details['version'])):
        cmd = 'ln -s %s/%s.pdf %s/%s/"%s".pdf'
        cmd = cmd % (wolvars.arxiv_dir, details['version'],
                     wolvars.woldir, details['dir'], details['title'])
        os.system(cmd)
    return
################################################################################

def find(args, handler, and_or='and'):
    args = [x.lower() for x in args]
    if and_or != 'and' and and_or != 'or':
        and_or = 'and'
    pass_list = []
    for arxiv, details in handler.details.iteritems():
        if args == []:
            pass_list.append(arxiv)
            continue
        if and_or == 'and':
            passes = True
        else:
            passes = False
        for arg in args:
            if not (details['title'].lower().count(arg) or
                    details['dir'].lower().count(arg) or
                    details['version'].lower().count(arg)):
                if and_or == 'and':
                    passes &= False
                else:
                    passes |= True
        if passes:
            pass_list.append(arxiv)
    return pass_list
################################################################################
