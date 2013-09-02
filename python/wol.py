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
import os
import wolOperations as wolOps
from wolFunctions import *
################################################################################
def help_msg():
    msg = 'Options for wol:'
    msg += '\n    add        Add something to wol'
    msg += '\n    mv         Move paper(s) to new directory'
    msg += '\n    find       Find paper(s) matching ALL arguments'
    msg += '\n    findor     Find paper(s) matching ONE argument'
    msg += '\n    show       Show paper(s) matching ALL arguments'
    msg += '\n    update     Ensure wol is up to date'
    msg += '\n    recent     Print most recent'
    msg += '\n    config     Change options'
    msg += '\n    info       Display info'
    msg += '\n    help       Display this message'
    print msg
    return
################################################################################


def opts(args):
    """Options parse and then run."""
    # Remove scriptname and get option
    args.pop(0)
    if len(args) == 0:
        print 'Please give an operation.'
        return
    if ('help' in args or
        '-h' in args):
        help_msg()
        return
    operation = args.pop(0)
    # Run function depending on option
    if operation == 'add':
        wolOps.add(args)
    elif operation == 'mv':
        wolOps.mv(args)
    elif operation == 'find':
        wolOps.find_and_print(args, 'and')
    elif operation == 'findor':
        wolOps.find_and_print(args, 'or')
    elif operation == 'show':
        wolOps.show(args)
    elif operation == 'recent':
        wolOps.recent()
    elif operation == 'update':
        wolOps.update(args)
    elif operation == 'config':
        wolOps.config(args)
    elif operation == 'info':
        wolOps.info(__author__, __version__)
    else:
        print 'For help, just ask'
    return
################################################################################

if __name__ == "__main__":
    """Run the script!"""
    opts(sys.argv)
