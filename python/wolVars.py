################################################################################
import os
################################################################################

def Singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


@Singleton
class WolVars(object):
    """Keeps all variables and pathnames and urls etc."""
    _web_arxiv_abs = 'http://arxiv.org/abs/{}'
    _web_arxiv_pdf = 'http://arxiv.org/pdf/{}.pdf'
    _woldir = None
    def __init__(self):
        self._woldir = os.getenv('WOLDIR')
        if not self._woldir:
            self._woldir = os.getcwd()

    @property
    def arxiv_dir(self):
        return os.path.join(self._woldir, 'arxiv')
    @property
    def default_dir(self):
        #return os.path.join(self._woldir, 'papers')
        return 'papers'
    @property
    def dotwol(self):
        return os.path.join(self._woldir, '.wol')
    @property
    def woldir(self):
        return self._woldir
    @property
    def del_dir(self):
        return os.path.join(self._woldir, 'deleted')

    def get_arxiv_abs(self, number):
        return self._web_arxiv_abs.format(number)
    #
    def get_arxiv_pdf(self, number):
        return self._web_arxiv_pdf.format(number)
    #

################################################################################
