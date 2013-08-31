################################################################################
import os
################################################################################

class WolVars:
    """Keeps all variables and pathnames and urls etc."""
    arxiv_abs = 'http://arxiv.org/abs/%s'
    arxiv_pdf = 'http://arxiv.org/pdf/%s.pdf'
    lhcb_ana = 'https://cds.cern.ch/record/1384141/files/%s'
    woldir = ''
    arxiv_dir = ''
    woldot = ''
    def __init__(self):
        self.woldir = os.getenv('WOLDIR')
        if not self.woldir:
            self.woldir = os.getcwd()
        self.arxiv_dir = '%s/arxiv' % self.woldir
        self.woldot = '%s/.wol' % self.woldir
    #
    def get_arxiv_abs(self, number):
        return self.arxiv_abs % number
    #
    def get_arxiv_pdf(self, number):
        return self.arxiv_pdf % number
    #
    def get_lhcb_ana(self, name):
        return self.lhcb_ana % name

################################################################################
