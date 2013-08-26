

class WolDictHandler:
    details = {}
    recents = []
    def __init__(self, details, recents=[]):
        self.details = details
        self.recents = recents
        return
    #
    def get(self, arxiv):
        try:
            return self.details[arxiv]
        except KeyError:
            print 'No arXiv number %s in wol' % arxiv
            raise
        return
    #
    def add(self, arxiv, vers, directory, title):
        try:
            self.details[arxiv] = {'version' : vers,
                                   'dir' : directory,
                                   'title' : title}
        except KeyError:
            raise
        return
    #
    def remove(self, arxiv):
        try:
            self.details.pop(arxiv)
        except KeyError:
            print 'No arXiv number %s in wol' % arxiv
            raise
        return
    #
    def move(self, arxiv, directory):
        if self.get(arxiv)['dir'] == directory:
            return False
        self.details[arxiv]['dir'] = directory
        return True
 
