
# coding=utf-8

from betweenness_centrality import *
from collections import Counter
from candidate_words import *
import os
import jieba.analyse


class Keyword:

    def __init__(self):
        self.poss = {}   # 词性表
        self.word_length = {}  # 词长表(记录每个词的词长)
        self.word_score = {}  # 词的评分表

    def feature(self, string_data):
        """
        function: 计算候选词的词性权重，词频，词长
        :param string_data: 待分析的语句
        :return:
        """
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, 'tag.txt')
        files = open(file_path, "r")
        poss_file = files.readlines()
        for line in poss_file:
            s = line.strip().split(' ')
            self.poss[s[0]] = s[1]
            #print s[1]
            #print s[0]
        po = self.poss
        candidate_words_dict, nword = CandidateWords().get_candidate_list(string_data)
        nwword_words = nword.values()   #order words
        pos = {}
        for word in nwword_words:
            self.word_length[word] = len(word)/3
            if candidate_words_dict[word] in po.keys():
                pos[word] = float(po[candidate_words_dict[word]])
            else:
                pos[word] = 0.1
        words_tf_dict = dict(Counter(nwword_words))                #统计词出现的次数的列表
        files.close()
        return pos, words_tf_dict, self.word_length, nwword_words

    def score(self, string_data):
        """
        function: 计算候选词的重要性权重(weight)
        :param string_data: 待分析的短句
        :return: 候选词的权重排位
        """

        tw = 0.4  # 词权重
        vdw = 0.6  # 居间度权重
        lenw = 0.1  # 词长权重
        posw = 0.8  # 词性权重
        tfw = 0.3  # tf词频权重
        pos, words_tf_dict, word_length, candidate_word = self.feature(string_data)
        vd = BetweenCentrality().codes_betweeness_centarlity(string_data)
        for word in candidate_word:
            s = (vd[word] * vdw ) + (tw * (word_length[word] * lenw + pos[word] * posw + words_tf_dict[word]*tfw))
            self.word_score[word] = s
        rank = sorted(self.word_score.iteritems(), key=lambda d: d[1], reverse=True)
        return rank

    def keyword(self, string_data):
        """
        function: 返回关键词及其评分
        :param string_data: 待分析的短句
        :return: keywords :关键词，关键词评分
        """
        key_score = self.score(string_data)
        keywords = []
        for key in key_score[0:7]:
            keywords.append(key[0])
        return keywords, key_score


def main_keyword(news_list):
    string = ''
    for i in news_list:
        string += i
    keyword_list = Keyword().keyword(string)
    keywords = keyword_list[0]
    print '------------本程序的提取效果--------------'
    for key in keywords:
        print key
    print '\n'
    print '------------结巴分词的提取效果--------------'
    jieba_list = jieba.analyse.extract_tags(string)
    for key in jieba_list:
        print key
    print '\n'
    return keywords


if __name__ == "__main__":
#     """string将所有的相关新闻拼合，然后进项关键词提取"""
#     string = '【中方谴责越南边检污损中国护照：无耻懦夫】'
#     string += '【中方要越南调查&quot;护照脏话&quot; 越方驱逐66名中国人】'
#     string += '【中方要越南调查&quot;护照脏话&quot; 越方驱逐66名中国人】'
    string = open('test.txt','r').read().split('\n')
    keywords = main_keyword(string)
    keys={}
    score=100
    for key in keywords:
        #print key
        keys['key']=score
        score = score-10
    #print (keywords)



