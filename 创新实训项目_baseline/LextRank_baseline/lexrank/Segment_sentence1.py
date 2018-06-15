#-*- encoding:utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import jieba.posseg as pseg
import codecs
import os

import libiary1

def get_default_stop_words_file():
    d = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(d, 'stopwords.txt')

class WordSegmentation(object):
    """ 分词 """
    
    def __init__(self, stop_words_file = None, allow_speech_tags = libiary1.allow_speech_tags): #词性列表，用于过滤
        """
        Keyword arguments:
        stop_words_file    -- 保存停止词的文件路径，utf8编码，每行一个停止词。若不是str类型，则使用默认的停止词
        allow_speech_tags  -- 词性列表，用于过滤
        """     
        
        allow_speech_tags = [item for item in allow_speech_tags]

        self.default_speech_tag_filter = allow_speech_tags
        self.stop_words = set()
        self.stop_words_file = get_default_stop_words_file()
        if type(stop_words_file) is str:
            self.stop_words_file = stop_words_file
        for word in codecs.open(self.stop_words_file, 'r', 'utf-8', 'ignore'):
            self.stop_words.add(word.strip())
        #添加入停止词列表中的词语
    def segment(self, text, lower = True, use_stop_words = False, use_speech_tags_filter = False):
        """对一段文本进行分词，返回list类型的分词结果，输入的是一个句子

        Keyword arguments:
        lower                  -- 是否将单词小写（针对英文）
        use_stop_words         -- 若为True，则利用停止词集合来过滤（去掉停止词）
        use_speech_tags_filter -- 是否基于词性进行过滤。若为True，则使用self.default_speech_tag_filter过滤。否则，不过滤。    
        """

        jieba_result = pseg.cut(text)   #标注句子分词后每个词的词性

        if use_speech_tags_filter == True:
            jieba_result = [w for w in jieba_result if w.flag in self.default_speech_tag_filter]
        else:
            jieba_result = [w for w in jieba_result]

        # 去除特殊符号
        word_list = [w.word.strip() for w in jieba_result if w.flag!='x']
        word_list = [word for word in word_list if len(word)>0]
        
        if lower:
            word_list = [word.lower() for word in word_list]

        if use_stop_words:
            word_list = [word.strip() for word in word_list if word.strip() not in self.stop_words]

        return word_list
        
    def segment_sentences(self, sentences, lower=True, use_stop_words=False, use_speech_tags_filter=False):
        """将列表sequences中的每个元素/句子转换为由单词构成的列表。
        sequences -- 列表，每个元素是一个句子（字符串类型）
        """
        
        res = []
        for sentence in sentences:
            print(sentence)
            res.append(self.segment(text=sentence, 
                                    lower=lower, 
                                    use_stop_words=use_stop_words, 
                                    use_speech_tags_filter=use_speech_tags_filter))
        return res
        #返回一个二维的列表


class Segment_sentence(object):
    
    def __init__(self, stop_words_file = None, 
                    allow_speech_tags = libiary1.allow_speech_tags,
                    delimiters = libiary1.sentence_delimiters):
        """
        Keyword arguments:
        stop_words_file -- 停止词文件
        delimiters      -- 用来拆分句子的符号集合
        """
        self.ws = WordSegmentation(stop_words_file=stop_words_file, allow_speech_tags=allow_speech_tags)

        
    def segment(self, text, lower = False):

        sentences = text#分句得到正常的句子列表
        #print(sentences)
        words_no_filter = self.ws.segment_sentences(sentences=sentences, 
                                                    lower = lower, 
                                                    use_stop_words = False,
                                                    use_speech_tags_filter = False)
        words_no_stop_words = self.ws.segment_sentences(sentences=sentences, 
                                                    lower = lower, 
                                                    use_stop_words = True,
                                                    use_speech_tags_filter = False)

        words_all_filters = self.ws.segment_sentences(sentences=sentences, 
                                                    lower = lower, 
                                                    use_stop_words = True,
                                                    use_speech_tags_filter = True)
        #返回一个字典
        return libiary1.AttrDict(
                    sentences           = sentences, 
                    words_no_filter     = words_no_filter, 
                    words_no_stop_words = words_no_stop_words, 
                    words_all_filters   = words_all_filters
                )

if __name__ == '__main__':
    pass