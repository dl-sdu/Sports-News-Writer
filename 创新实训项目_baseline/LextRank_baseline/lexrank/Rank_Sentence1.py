#-*- encoding:utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import networkx as nx
import numpy as np
from . import libiary1
from .Segment_sentence1 import Segment_sentence
from .Segment_sentence1 import WordSegmentation
import networkx as nx
import similarity1
from nltk.tokenize import word_tokenize
import numpy as np
#import miscellaneous as ms
import itertools
import argparse
import math

def build_graph(self,nodes, threshold, idf):  # nodes是句子的列表；idf是单词的idf字典
    gr = nx.Graph()  # initialize an undirected graph
    gr.add_nodes_from(nodes)  # 一个句子就是一个节点
    nodePairs = list(itertools.combinations(nodes, 2))
    self.ws=WordSegmentation(stop_words_file = None,
                    allow_speech_tags = libiary1.allow_speech_tags)
    # add edges to the graph (weighted by cosine similarity)
    for pair in nodePairs:
        node1 = pair[0]
        node2 = pair[1]
        node1_1=self.ws.segment(text=node1, lower=True, use_stop_words=False, use_speech_tags_filter=False)
        node1_2=self.ws.segment(text=node2, lower=True, use_stop_words=False, use_speech_tags_filter=False)
        #print(2131231)
        #print(node1_1,node1_2,idf)
        simval = similarity1.idf_modified_cosine1(node1_1, node1_2, idf)

        #print(simval)

        if simval > threshold:  # 只有句子之间的相似度大于一定阈值才有边
            gr.add_edge(node1, node2, weight=simval)

    return gr



# key sentences are obtained
def get_keysentences(graph):
    # weight is the similarity value obtained from the idf_modified_cosine
    calculated_page_rank = nx.pagerank(graph, weight='weight')  # python的networkx中包含了PageRank
    # most important words in ascending order of importance
    keysentences = sorted(calculated_page_rank, key=calculated_page_rank.get, reverse=True)
    return keysentences


class Rank_Sentence1(object):
    
    def __init__(self, stop_words_file = None,
                 allow_speech_tags = libiary1.allow_speech_tags,  #词性列表，用于过滤
                 delimiters = libiary1.sentence_delimiters):#分割符
        """
        Keyword arguments:
        stop_words_file  --  str，停止词文件路径，若不是str则是使用默认停止词文件
        delimiters       --  默认值是`?!;？！。；…\n`，用来将文本拆分为句子。
        
        Object Var:
        self.sentences               --  由句子组成的列表。
        self.words_no_filter         --  对sentences中每个句子分词而得到的两级列表。
        self.words_no_stop_words     --  去掉words_no_filter中的停止词而得到的两级列表。"停用词"（stop words），表示对找到结果毫无帮助、必须过滤掉的词
        self.words_all_filters       --  保留words_no_stop_words中指定词性的单词而得到的两级列表。
        """
        self.seg = Segment_sentence(stop_words_file=stop_words_file,
                                allow_speech_tags=allow_speech_tags,
                                delimiters=delimiters)

        self.sentences = None
        self.words_no_filter = None     # 2维列表
        self.words_no_stop_words = None
        self.words_all_filters = None
        
        self.key_sentences = None

    def analyze(self, text, lower = False,
                source = 'no_filter'):
        """
        Keyword arguments:
        text                 --  文本内容，字符串。
        lower                --  是否将文本转换为小写。默认为False。
        source               --  选择使用words_no_filter, words_no_stop_words, words_all_filters中的哪一个来生成句子之间的相似度。
                                 默认值为`'all_filters'`，可选值为`'no_filter', 'no_stop_words', 'all_filters'`。
        sim_func             --  指定计算句子相似度的函数。
        """
        
        self.key_sentences = []

        result = self.seg.segment(text=text, lower=lower)
        self.sentences = result.sentences
        self.words_no_filter = result.words_no_filter
        self.words_no_stop_words = result.words_no_stop_words
        self.words_all_filters   = result.words_all_filters

        #print(self.sentences)

       # print(self.words_all_filters)

        options = ['no_filter', 'no_stop_words', 'all_filters']
        if source in options:
            _source = result['words_'+source]
        else:#传入参数是no_stop_words所以else的结果也是这个
            _source = result['words_no_stop_words']
        #改动之处

        threshold = 0.05  # 观察相似度矩阵可以发现大部分值都很小，如果threshold设得太大，就几乎没有边了，随机初始化的影响大，导致排序结果不稳定
        top = 5

        sent_tokens=self.sentences
        word_tokens=_source
        word_sum=[]
        for i in word_tokens:
            word_sum=word_sum+i

        print(word_sum)

        words = list(set(word_sum))#得到单词列表

        N = len(sent_tokens)#返回句子数目

        print(word_tokens)
        print(words)

        idf = similarity1.idf(word_tokens, words, N)  #传送单词矩阵 以及单词列表，返回一个单词的idf值

        matrix = similarity1.get_similarity_matrix(word_tokens, idf)   #传送单词矩阵 以及idf 得到相似矩阵

        print("Printing similarity matrix:\n", matrix)

        print(idf)

        gr = build_graph(self,sent_tokens, threshold, idf) #建立图

        self.keysentences = get_keysentences(gr)

        print("Printing Top " + str(top) + " Key sentences:\n", self.keysentences[:top])  # 这里返回的句子是按重要性排序的


        #改动完毕
        '''self.key_sentences = libiary1.sort_sentences(sentences = self.sentences,
                                                    words     = _source,
                                                    sim_func  = sim_func,
                                                     pagerank_config = pagerank_config)'''

            


if __name__ == '__main__':
    pass