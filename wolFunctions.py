import pickle
import sys
import os
from wolClasses import *



def arxiv_format(string):
    arxiv = string.replace('.pdf', '')
    arxiv = arxiv.split('/')[-1]
    if arxiv.count('v'):
        arxiv = arxiv[:arxiv.find('v')]
    if arxiv.count(']'):
        arxiv = arxiv.replace('[', '')
        arxiv = arxiv[:arxiv.find(']')]
    return arxiv

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

def str2arxiv(string):
    arxiv = arxiv_format(string)
    if not is_arxiv(arxiv):
        print '%s (from %s) is not a valid arxiv number' % (arxiv, string)
        sys.exit(0)
    return arxiv

def put_dot_wol(handler):
    """Puts handler from the .wol"""
    woldot = WolVars().woldot
    f = open(woldot, 'wb')
    handler = pickle.dump(handler, f)
    f.close()
    return

def get_dot_wol(filename=None):
    """Gets details from the .wol"""
    woldot = WolVars().woldot
    dict_handler = WolDictHandler()
    if filename is None:
        filename = woldot
    if not os.path.exists(filename):
        dict_handler.setup({}, [])
        f = open(filename, 'wb')
        pickle.dump(dict_handler, f)
        f.close()
    else:
        f = open(filename, 'rb')
        details = pickle.load(f)
        dict_handler.setup(details.details, details.recents)
        f.close()
    return dict_handler

def arxiv_file(arxiv, files):
    if type(files) is str:
        files = [files]
    files = [str2arxiv(x) for x in files]
    arxiv = str2arxiv(arxiv)
    if files.count(arxiv):
        return True
    return False

def get_arxiv_from_web(details):
    cmd = 'wget -q --user-agent=Lynx %s -O %s/%s.pdf'
    wolvars = WolVars()
    cmd = cmd % (wolvars.get_arxiv_pdf(details['version']), wolvars.arxiv_dir,
            details['version'])
    os.system(cmd)

    
