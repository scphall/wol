import pickle
import os


def arxiv_format(string):
    arxiv = string.replace('.pdf', '')
    arxiv = arxiv.split('/')[-1]
    arxiv = arxiv[:arxiv.find('v') + 1]
    return arxiv

def is_arxiv(arxiv):
    check = arxiv.split('.')
    accept = True
    if len(check) != 2:
        accept = False
    elif not check[0].isdigit() or not check[1].isdigit():
        accept = False
    elif len(check[0]) != 4 or len(check[1]) != 4:
        accept = False
    return accept

def str2arxiv(string):
    arxiv = arxiv_format(string)
    if not is_arxiv(arxiv):
        print '%s (from %s) is not a valid arxiv number' % (arxiv, string)
        raise
    return arxiv

def get_dot_wol():
    """Gets details from the .wol"""
    woldot = WolVars().woldot
    all_details = {}
    if not os.path.exists(woldot):
        f = open(woldot, 'wb')
        pickle.dump(all_details, f)
        f.close()
    else:
        f = open(woldot, 'rb')
        all_details = pickle.load(f)
        f.close()
    return all_details

