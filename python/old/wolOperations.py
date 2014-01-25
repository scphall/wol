################################################################################
"""
Contains all operations that are arguments of wol

"""
################################################################################
import sys
import os
from wolVars import *
from wolDictHandler import *
from wolFunctions import *
################################################################################

def add_wol_file(filename, handler):
    """Add xxx.wol file(s) to .wol"""
    if not os.path.exists(filename):
        print "File %s does not exist" % filename
        return
    print "Adding %s" % filename
    new_handler = get_dot_wol(filename)
    new_details = new_handler.details
    files = os.listdir(WolVars().arxiv_dir)
    for arxiv, details in new_details.iteritems():
        if not handler.append(arxiv, details):
            print "Paper %s already present in %s" % (
                arxiv,
                handler.get(arxiv, 'dir'))
            continue
        if not arxiv_file(arxiv, files):
            get_arxiv_from_web(details)
        check_directory(handler.get(arxiv, 'dir'))
        create_ln(handler.get(arxiv))
        print 'Paper "%(title)s" in %(dir)s' % handler.get(arxiv)
    return
################################################################################

def add(args):
    """Add a file (by arxiv number, worked out if possible) to .wol"""
    print 80 * '-'
    wolvars = WolVars()
    wolfiles = [x for x in args if x.endswith('.wol')]
    move_dir = args.pop(-1)
    arxivs = [str2arxiv(x) for x in args]
    test_dir = arxiv_format(move_dir)
    if not is_arxiv(test_dir) and not is_arxiv_old(test_dir):
        directory = test_dir
    else:
        directory = 'papers'
        arxivs.append(str2arxiv(test_dir))
    handler = get_dot_wol()
    check_directory(wolvars.arxiv_dir)
    for arxiv in arxivs:
        files = os.listdir(wolvars.arxiv_dir)
        if not handler.has(arxiv):
            version, title = get_arxiv_details(arxiv)
            handler.add(arxiv, version, directory, title)
        if not arxiv_file(arxiv, files):
            get_arxiv_from_web(handler.get(arxiv))
        check_directory(os.path.join(wolvars.woldir, handler.get(arxiv, 'dir')))
        create_ln(handler.get(arxiv))
        #print 'Paper "%(title)s" in %(dir)s' % handler.get(arxiv)
        handler.printer(arxiv, True)
    for wolfile in wolfiles:
        add_wol_file(wolfile, handler)
    put_dot_wol(handler)
    return
################################################################################

def mv_old(args):
    """Move files to another directory."""
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
        handler.printer(arxiv, True)
    put_dot_wol(handler)
    return

################################################################################
def mv(args):
    """Move files to another directory."""
    print 80 * '-'
    wolvars = WolVars()
    directory = args.pop(-1)
    args = [x.lower() for x in args]
    handler = get_dot_wol()
    check_directory(wolvars.arxiv_dir)
    for arxiv, details in handler.details.iteritems():
        for arg in args:
            if (details['title'].lower().count(arg) or
                details['dir'].lower().count(arg) or
                details['version'].lower().count(arg)):
                #if not handler.has(arxiv):
                #    version, title = get_arxiv_details(arxiv)
                #    handler.add(arxiv, version, directory, title)
                #if not arxiv_file(arxiv, files):
                #    get_arxiv_from_web(handler.get(arxiv))
                if directory != details['dir']:
                    cmd = 'rm -f %s/%s/"%s".pdf'
                    cmd = cmd % (wolvars.woldir,
                                 handler.get(arxiv, 'dir'),
                                 handler.get(arxiv, 'title'))
                    handler.put(arxiv, 'dir', directory)
                    os.system(cmd)
                check_directory('%s/%s' % (wolvars.woldir,
                                           handler.get(arxiv, 'dir')))
                create_ln(handler.get(arxiv))
                handler.printer(arxiv, True)
    put_dot_wol(handler)
    return
################################################################################

def find_and_print(args, and_or='and'):
    """Give details on any matched arguments."""
    print '-' * 80
    handler = get_dot_wol()
    pass_list = find(args, handler, and_or)
    for arxiv in pass_list:
        handler.printer(arxiv)
    return
################################################################################

def update(args):
    """ensure that directories are up to date."""
    if len(args) != 0:
        print 'No options needed to update'
        return
    wolvars = WolVars()
    handler = get_dot_wol()
    check_directory(wolvars.arxiv_dir)
    for arxiv, details in handler.details.iteritems():
        files = os.listdir(wolvars.arxiv_dir)
        if not arxiv_file(arxiv, files):
            get_arxiv_from_web(details)
            handler.printer(arxiv, True)
        check_directory('%s/%s' % (wolvars.woldir, handler.get(arxiv, 'dir')))
        create_ln(details)
    return

################################################################################

def recent():
    handler = get_dot_wol()
    handler.printer_recents()
################################################################################

def show(args):
    """Open any matched arguments."""
    arxiv_dir = WolVars().arxiv_dir
    handler = get_dot_wol()
    cmd = [handler.config['viewer']]
    #args = [x.lower() for x in args]
    pass_list = find(args, handler, 'and')
    if len(pass_list) > 5:
        print 'Too many files, not opening'
        return
    for arxiv in pass_list:
        cmd.append('%s/%s.pdf' % (arxiv_dir, handler.get(arxiv, 'version')))
    cmd += ' &'
    cmd = ' '.join(cmd)
    os.system(cmd)
    return
################################################################################

def config(args):
    if len(args) > 2:
        print 'Config input not allowed'
        return
    handler = get_dot_wol()
    handler.config[args[0]] = args[1]
    put_dot_wol(handler)
    return
################################################################################

def info(author, version):
    handler = get_dot_wol()
    msg = 'Wol info:'
    msg += '\n    Entries : %d' % len(os.listdir(WolVars().arxiv_dir))
    msg += '\n  Configurables:'
    msg += '\n    viewer  : %(viewer)s' % handler.config
    print msg
    return
################################################################################

def rm(args):
    """Move files to another directory."""
    wolvars = WolVars()
    handler = get_dot_wol()
    check_directory(wolvars.delete_dir)
    args = [x.lower() for x in args]
    cmd_rm = []
    cmd_mv = []
    temp_rm = '%s/"%s".pdf'
    temp_mv = '%s/%s.pdf %s/%s.pdf' % (wolvars.arxiv_dir, '%s',
                                       wolvars.delete_dir, '%s')
    for arxiv, details in handler.details.iteritems():
        if arxiv not in args:
            cmd_rm.append(temp_rm % (details['dir'], details['title']))
    for arxiv in args:
        handler.details.pop(arxiv)
    cmds = ['mv %s' % x for x in cmd_mv]
    cmd_rm = ' '.join(cmd_rm)
    cmds.append('rm -f %s' % cmd_rm)
    put_dot_wol(handler)
    for cmd in cmds:
        os.system(cmd)
    return
################################################################################

def clean():
    wolvars = WolVars()
    dirs = os.listdir(wolvars.woldir)
    for dirpath, dirnames, filenames in os.walk(wolvars.woldir):
        if len(dirnames) == 0 and len(filenames) == 0:
            os.system('rmdir %s' % dirpath)
    if os.path.exists(wolvars.delete_dir):
        os.system('rm -rd %s' % wolvars.delete_dir)
    return

################################################################################
