#!/usr/bin/python
################################################################################

"""
wol is named for the most intelligent inhabitant of the Hundred Acre Wood.
He will gladly manage arXiv papers for you.

Setup your WOLDIR to be where you wish, and then begin.
If not set it will use the current directory.

See /wol/README.md for more details.

"""

__title__  = "wol.py"
__author__ = "Sam Hall"
__email__  = "samcphall@gmail.com"
__version__ = "v2r0"

################################################################################
import sys
import urllib
import os
import re
import pickle
from wolHTMLParser import *
from wolVars import *
from wolArxivs import *
#import wolOperations as wolOps
#from wolFunctions import *
################################################################################


def get_arxiv(number):
    pattern = re.compile('(\d{4}\.\d{4}|\d{7})')
    match = pattern.search(number)
    if not match:
        return False
    return match.groups()[0]


def set_dotwol(arxivs):
    with open(WolVars().dotwol, 'wb') as f:
        pickle.dump(arxivs._arxivs, f)
        pickle.dump(arxivs._config, f)
    return


def read_dotwol(filename=None):
    arxivs = ArXivs()
    if filename is None:
        filename = WolVars().dotwol
    if not os.path.exists(WolVars().dotwol):
        print 'Making new .wol file'
        with open(filename, 'wb') as f:
            pickle.dump({}, f)
            pickle.dump({}, f)
    else:
        with open(filename, 'rb') as f:
            arxivs.set_arxivs(pickle.load(f))
            arxivs.set_config(pickle.load(f))
    return arxivs


def add(arxivs, *args):
    """Add arXiv papers to wol, or move into given directory"""
    dir = None
    if len(args) == 0:
        return arxivs
    if not get_arxiv(args[-1]) and len(args) > 1:
        dir = args[-1]
        args = args[:-1]
    for arg in args:
        arxivs.add(arg)
        if dir is not None:
            arxivs.move(arg, dir)
        print '{0}\n{1}'.format('-' * 80, arxivs.get(arg))
    print 80 * '-'
    return arxivs


def addwol(arxivs, *args):
    """Add existing .wol file to current .wol"""
    for arg in args:
        new_arxivs = read_dotwol(arg)
        arxivs.add(new_arxivs)
    return arxivs


def find(arxivs, *args):
    """Find an arXiv paper in wol"""
    if len(args) > 0:
        arxivs.find(args[0])
    else:
        arxivs.find('.')
    return arxivs


def move(arxivs, *args):
    """Move arXiv papers in wol"""
    if len(args) > 1:
        arxivs.move(args[0], args[1])
    return arxivs


def show(arxivs, *args):
    """Show arXiv papers"""
    files = arxivs.find(args[0])
    cmd = '{} '.format(arxivs.viewer)
    if len(files) > 6:
        files = files[:6]
    for file in files:
        cmd += '"{}" '.format(file)
    if len(files) > 0:
        os.system(cmd)
    return arxivs


def config(arxivs, *args):
    """Show or set config"""
    if len(args) == 2:
        arxivs.config(args[0], args[1])
    arxivs.show_config()
    return arxivs


def update(arxivs, *args):
    """Make sure everythin in .wol is in WOLDIR"""
    arxivs.check()
    return arxivs

def delete(arxivs, *args):
    """Remove entry by arxiv reference"""
    for arg in args:
        arxivs.delete(arg)
    return arxivs


def help(operations):
    print 'Wol help, possible operations are:'
    for key, item in sorted(operations.iteritems()):
        print ' {:10s} {}'.format(key, item.__doc__)
    return

def info(arxivs, *args):
    """Print info"""
    print 'Wol info:'
    print ' {:30s} {}'.format('Number of entries', len(arxivs))
    return arxivs


def opts(operation, *args):
    """Options parse and then run."""
    operations = {
        'add' : add,
        'addwol' : addwol,
        'move' : move,
        'find' : find,
        'show' : show,
        'config' : config,
        'update' : update,
        'del' : delete,
        'info' : info,
    }
    if operation in ['help', '-h']:
        help(operations)
        return
    if operation not in operations.keys():
        print 'Operation {} is unknown'.format(operation)
    else:
        arxivs = read_dotwol()
        arxivs = operations[operation](arxivs, *args)
        set_dotwol(arxivs)
    return

################################################################################

if __name__ == "__main__":
    """Run the script!"""
    args = sys.argv[1:]
    if not args:
        print 'Please give an operation'
    else:
        operation = args.pop(0)
        opts(operation, *args)


