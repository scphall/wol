################################################################################
import os
################################################################################

class WolVars:
    """Keeps all variables and pathnames and urls etc."""
    arxiv_abs = 'http://arxiv.org/abs/%s'
    arxiv_pdf = 'http://arxiv.org/pdf/%s.pdf'
    woldir = ''
    arxiv_dir = ''
    delete_dir = ''
    woldot = ''
    def __init__(self):
        self.woldir = os.getenv('WOLDIR')
        if not self.woldir:
            self.woldir = os.getcwd()
        self.arxiv_dir = '%s/arxiv' % self.woldir
        self.delete_dir = '%s/.deleted' % self.woldir
        self.woldot = '%s/.wol' % self.woldir
    #
    def get_arxiv_abs(self, number):
        return self.arxiv_abs % number
    #
    def get_arxiv_pdf(self, number):
        return self.arxiv_pdf % number
    #

################################################################################
