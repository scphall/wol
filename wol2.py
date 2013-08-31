################################################################################
import sys
import os
import urllib
from wolClasses import *
from wolFunctions import *
################################################################################
def check_directory(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)
        return

def get_arxiv_details(arxiv):
    wolvars = WolVars()
    url = wolvars.get_arxiv_abs(arxiv)
    data = urllib.urlopen(url).read()
    parser = LitHTMLParser()
    parser.feed(data)
    urlname = wolvars.get_arxiv_pdf(parser.filename)
    return (parser.filename, parser.title)

def create_ln(details):
    wolvars = WolVars()
    files = os.listdir('%s/%s' % (wolvars.woldir, details['dir']))
    files = [str2arxiv(x) for x in files]
    arxiv = str2arxiv(details['version'])
    if not files.count(arxiv):
        cmd = 'ln -s %s/%s.pdf %s/%s/"%s".pdf'
        cmd = cmd % (wolvars.arxiv_dir, details['version'],
                     wolvars.woldir, details['dir'], details['title'])
        os.system(cmd)
    return

def add_wol_file(filename, handler):
    if not os.path.exists(filename):
        print "File %s does not exist" % filename
        return
    print "Adding %s" % filename
    new_handler = get_dot_wol(filename)
    new_details = new_handler.details
    files = os.listdir(WolVars().arxiv_dir)
    for arxiv, details in new_details.iteritems():
        if not handler.append(arxiv, details):
            print "Paper %s already present in %s" % (arxiv,
                                                      handler.get(arxiv, 'dir'))
            continue
        if not arxiv_file(arxiv, files):
            get_arxiv_from_web(details)
        check_directory(handler.get(arxiv, 'dir'))
        create_ln(handler.get(arxiv))
        print 'Paper "%(title)s" in %(dir)s' % handler.get(arxiv)
    return

def add(args):
    print 80 * '-'
    wolvars = WolVars()
    wolfiles = [x for x in args if x.endswith('.wol')]
    move_dir = args.pop(-1)
    arxivs = [str2arxiv(x) for x in args]
    test_dir = arxiv_format(move_dir)
    if not is_arxiv(test_dir):
        directory = test_dir
    else:
        directory = 'papers'
        arxivs.append(test_dir)
    handler = get_dot_wol()
    check_directory(wolvars.arxiv_dir)
    for arxiv in arxivs:
        files = os.listdir(wolvars.arxiv_dir)
        if not handler.has(arxiv):
            version, title = get_arxiv_details(arxiv)
            handler.add(arxiv, version, directory, title)
        if not arxiv_file(arxiv, files):
            get_arxiv_from_web(handler.get(arxiv))
        check_directory(handler.get(arxiv, 'dir'))
        create_ln(handler.get(arxiv))
        #print 'Paper "%(title)s" in %(dir)s' % handler.get(arxiv)
        handler.printer(arxiv)
    for wolfile in wolfiles:
        add_wol_file(wolfile, handler)
    put_dot_wol(handler)
    return

def mv(args):
    print 80 * '-'
    wolvars = WolVars()
    directory = args.pop(-1)
    arxivs = [str2arxiv(x) for x in args]
    handler = get_dot_wol()
    check_directory(wolvars.arxiv_dir)
    for arxiv in arxivs:
        files = os.listdir(wolvars.arxiv_dir)
        if not handler.has(arxiv):
            version, title = get_arxiv_details(arxiv)
            handler.add(arxiv, version, directory, title)
        if not arxiv_file(arxiv, files):
            get_arxiv_from_web(handler.get(arxiv))
        if directory != handler.get(arxiv, 'dir'):
            cmd = 'rm -f %s/%s/"%s".pdf'
            cmd = cmd % (wolvars.woldir,
                         handler.get(arxiv, 'dir'),
                         handler.get(arxiv, 'title'))
            handler.put(arxiv, 'dir', directory)
            os.system(cmd)
        check_directory(handler.get(arxiv, 'dir'))
        create_ln(handler.get(arxiv))
        #print 'Paper "%(title)s" in %(dir)s' % handler.get(arxiv)
        handler.printer(arxiv)
        #print 'Paper "%(title)s" in %(dir)s' % handler.get(arxiv)
    put_dot_wol(handler)
    return


def find(args):
    print '-' * 80
    handler = get_dot_wol()
    to_print = False
    args = [x.lower() for x in args]
    for arxiv, details in handler.details.iteritems():
        if args == []:
            handler.printer(arxiv)
            continue
        to_print = False
        for arg in args:
            if (details['title'].lower().count(arg) or 
                details['dir'].lower().count(arg) or 
                details['version'].lower().count(arg)):
                handler.printer(arxiv)
    return

def update(args):
    if len(args) != 0:
        print 'No options needed to update'
        return
    print 80 * '-'
    wolvars = WolVars()
    handler = get_dot_wol()
    check_directory(wolvars.arxiv_dir)
    for arxiv, details in handler.details.iteritems():
        files = os.listdir(wolvars.arxiv_dir)
        if not arxiv_file(arxiv, files):
            get_arxiv_from_web(details)
            handler.printer(arxiv)
        check_directory(handler.get(arxiv, 'dir'))
        create_ln(details)
    return


def opts(args):
    args.pop(0)
    if len(args) == 0:
        print 'Please give an operation.'
        return
    operation = args.pop(0)
    if operation == 'add':
        add(args)
    elif operation == 'mv':
        mv(args)
    elif operation == 'find':
        find(args)
    elif operation == 'update':
        update(args)
    else:
        print 'What??'
    return


if __name__ == "__main__":
    opts(sys.argv)
