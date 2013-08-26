################################################################################
import sys
import os
import urllib
################################################################################
def get_arxiv_details(arxiv):
    url = wolvars.get_arxiv_abs(arxiv)
    data = urllib.urlopen(url).read()
    parser = LitHTMLParser()
    parser.feed(data)
    urlname = wolvars.get_arxiv_pdf(parser.filename)
    if not os.path.exists('%s/%s' % (wolvars.arxiv_dir, parser.filename)):
        cmd = 'wget -q --user-agent=Lynx %s -O %s/%s.pdf'
        cmd = cmd % (urlname, wolvars.arxiv_dir, parser.filename)
        os.system(cmd)
    return parser.filename, parser.title


def add(args):
    move_dir = args.pop(-1)
    arxivs = [str2arxiv(x) for x in args]
    test_dir = arxiv_format(move_dir)
    if not is_arxiv(test_dir):
        directory = test_dir
    else:
        directory = 'papers'
        arxiv.append(test_dir)
    details = get_dot_wol()
    for arxiv in arxivs:
        qq

    print 'add'

def mv(args):
    print 'mv'

def update(args):
    print 'update'

def opts(args):
    if len(args) == 1:
        print 'Please give an operation.'
        return
    operation = args.pop(0)
    if operation == 'add':
        print 'add'
        add(args)
    elif operation == 'mv':
        print 'mv'
        mv(args)
    elif operation == 'update':
        print 'update'
        update(args)
    elif operation == 'recent':
        print 'add'
    return







if __name__ == "__main__":
    main(sys.argv)
