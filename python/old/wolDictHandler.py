################################################################################
from wolVars import *
################################################################################

class WolDictHandler:
    """Class that is held in pickled file.
    Holds all information, including configurations.
    """
    details = {}
    recents = []
    config = {}
    template_info = ''
    template_add = ''
    def __init__(self):
        self.template_add = ' arXiv:      %(version)s\n'
        self.template_add += ' Directory:  %(dir)s\n'
        self.template_add += ' %(title_print)s\n'
        self.template_add += (80 * '-')
        #self.template_info = ' %s' % WolVars().woldir
        #self.template_info += '/%(dir)s/%(version)s.pdf\n'
        self.template_info = ' %(title_print)s\n'
        self.template_info += ' %s' % WolVars().arxiv_dir
        self.template_info += '/%(version)s.pdf\n'
        self.template_info += (80 * '-')
        self.config = {'viewer' : 'evince'}
        return
    #
    def setup(self, details, recents, config):
        self.details = details
        self.recents = recents
        self.config.update(config)
    #
    def get(self, arxiv, key=None):
        if key is None:
            try:
                return self.details[arxiv]
            except KeyError:
                print 'No arXiv number %s in wol' % arxiv
                raise
        else:
            try:
                return self.details[arxiv][key]
            except KeyError:
                print 'No arXiv number %s with key %s in wol' % arxiv, key
                raise
        return
    #
    def add_recent(self, arxiv):
        if self.recents.count(arxiv):
            self.recents.pop(self.recents.index(arxiv))
        if len(self.recents) > 9:
            self.recents = self.recents[:9]
        self.recents.append(arxiv)
        return
    #
    def add(self, arxiv, vers, directory, title):
        title = title.replace('\n', '')
        title = title.replace('$', '')
        title = title.replace('  ', ' ')
        title = title.replace('/', '')
        title = title.replace('--gt;', '\\to')
        title = title.replace('-gt;', '\\to')
        split = title.split(' ')[1:]
        title_print = split.pop(0)
        #vers.replace('/', '')
        n = 1
        for word in split:
            if (len(title_print) + len(word)) > 75 * n:
                title_print += '\n  '
                n += 1
            title_print += ' %s' % word
        directory = directory.rstrip('/.')
        self.details[arxiv] = {'version' : vers.replace('/', ''),
                               'version_get' : vers,
                               'dir' : directory,
                               'title' : title,
                               'title_print' : title_print}
        self.add_recent(arxiv)
        return
    #
    def has(self, key):
        return self.details.has_key(key)
    #
    def put(self, key, var, value):
        if var == 'dir':
            value = value.rstrip('/.')
        #elif var == 'version':
        #    value = value.replace('/', '')
        self.get(key)[var] = value
        return
    #
    def remove(self, arxiv):
        try:
            self.details.pop(arxiv)
        except KeyError:
            print 'No arXiv number %s in wol' % arxiv
            sys.exit(0)
        return
    #
    def move(self, arxiv, directory):
        if self.get(arxiv)['dir'] == directory:
            return False
        self.details[arxiv]['dir'] = directory
        return True
    #
    def append(self, arxiv, new_details):
        if self.has(arxiv):
            return False
        else:
            self.add(arxiv, new_details['version'],
                     new_details['dir'],
                     new_details['title'])
        return True
    #
    def printer(self, arxiv, new=False):
        if new:
            info = self.template_add % self.get(arxiv)
        else:
            info = self.template_info % self.get(arxiv)
        print info
        return
    #
    def printer_recents(self):
        print 80 * '-'
        for n, arxiv in enumerate(self.recents):
            print '%d )' % (len(self.recents) - n),
            self.printer(arxiv)
    #

################################################################################
