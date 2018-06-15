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
if not PY2:
    # Python 3.x and up
    text_type    = str
    string_types = (str,)
    xrange       = range

    def as_text(v):  ## 返回字符串
        if v is None:
            return None
        elif isinstance(v, bytes):
            return v.decode('utf-8', errors='ignore')
        elif isinstance(v, str):
            return v
        else:
            raise ValueError('Unknown type %r' % type(v))

    def is_text(v):
        return isinstance(v, text_type)
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

def get_similarity(word_list1, word_list2):
    """默认的用于计算两个句子相似度的函数。

    Keyword arguments:
    word_list1, word_list2  --  分别代表两个句子，都是由单词组成的列表
    """
    words   = list(set(word_list1 + word_list2))   #直接将两个列表合并为一个列表
    vector1 = [float(word_list1.count(word)) for word in words]#返回word_list1中的单词在words中的位置，并且他有几个相同的单词，那么在那个位置就是几
    vector2 = [float(word_list2.count(word)) for word in words]
    
    vector3 = [vector1[x]*vector2[x]  for x in xrange(len(vector1))]#v1和v2句子相同单词数量的乘积
    vector4 = [1 for num in vector3 if num > 0.]#判断v1和v2有多少个相同的单词
    co_occur_num = sum(vector4)#算出多少个相同的单词

    if abs(co_occur_num) <= 1e-12: #abs() 函数返回数字的绝对值
        return 0.
    
    denominator = math.log(float(len(word_list1))) + math.log(float(len(word_list2))) # 分母
    
    if abs(denominator) < 1e-12:
        return 0.
    
    return co_occur_num / denominator

def sort_sentences(sentences, words, sim_func = get_similarity, pagerank_config = {'alpha': 0.85,}):
    """将句子按照关键程度从大到小排序

    Keyword arguments:
    sentences         --  列表，元素是句子
    words             --  二维列表，子列表和sentences中的句子对应，子列表由单词组成
    sim_func          --  计算两个句子的相似性，参数是两个由单词组成的列表
    pagerank_config   --  pagerank的设置
    """
    sorted_sentences = []
    _source = words
    sentences_num = len(_source)       #算出句子的总数
    graph = np.zeros((sentences_num, sentences_num))
    
    for x in xrange(sentences_num):
        for y in xrange(x, sentences_num):
            similarity = sim_func( _source[x], _source[y] )
            graph[x, y] = similarity
            graph[y, x] = similarity

    nx_graph = nx.from_numpy_matrix(graph)       #自带的方法将邻接矩阵转换成网络图
    scores = nx.pagerank(nx_graph, **pagerank_config)              # this is a dict   #要求搞懂pagerank的思想
    sorted_scores = sorted(scores.items(), key = lambda item: item[1], reverse=True)  #key=lambda y: y[1] 备注：这里y可以是任意字母，等同key=lambda x: x[1]

    for index, score in sorted_scores:
        item = AttrDict(index=index, sentence=sentences[index], weight=score)
        sorted_sentences.append(item)

    return sorted_sentences

if __name__ == '__main__':
    pass