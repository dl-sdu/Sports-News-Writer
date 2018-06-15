#-*- encoding:utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from importlib import reload
import os
import math
import networkx as nx
import numpy as np
import sys

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass
    
sentence_delimiters = ['?', '!', ';', '？', '！', '。', '；', '……', '…', '\n']
allow_speech_tags= ['an', 'i', 'j', 'l', 'n', 'nr', 'nrfg', 'ns', 'nt', 'nz', 't', 'v', 'vd', 'vn', 'eng']

PY2 = sys.version_info[0] == 2

__DEBUG = None

def debug(*args):
    global __DEBUG
    if __DEBUG is None:
        try:
            if os.environ['DEBUG'] == '1':
                __DEBUG = True
            else:
                __DEBUG = False
        except:
            __DEBUG = False
    if __DEBUG:
        print( ' '.join([str(arg) for arg in args]) )

class AttrDict(dict):
    """Dict that can get attribute by dot"""
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self




if __name__ == '__main__':
    pass