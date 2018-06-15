# !/usr/bin/python
# -*- coding: utf-8 -*-
import nltk.data
import os
import libiary2
import jieba.posseg as pseg
import codecs
import Segment_sentence2
from Segment_sentence2 import Segment_sentence
class Parser:
    def __init__(self):
        self.ideal = 20.0
        self.seg = Segment_sentence(stop_words_file=None,
                                    allow_speech_tags=libiary2.allow_speech_tags,
                                    delimiters=libiary2.sentence_delimiters)

    def getKeywords(self, text):
        text = self.removePunctations(text)#去除标点后的文档
        result2 = self.seg.segment(text=text, lower=False)
        self.words_no_filter = result2.words_no_filter
        words = []
        for i in  self.words_no_filter:
            words=words+i


        uniqueWords = list(set(words))#得到一篇文章词典

        keywords = [{'word': word, 'count': words.count(word)} for word in uniqueWords]#得到每个词语出现的次数
        keywords = sorted(keywords, key=lambda x: -x['count'])#按词语出现次数进行排序,遵循从大到小的顺序

        return (keywords, len(words))#返回keywords以及单词总数

    def getSentenceLengthScore(self, sentence):#求句子长度得分
        return (self.ideal - abs(self.ideal - len(sentence))) / self.ideal

    # Jagadeesh, J., Pingali, P., & Varma, V. (2005). Sentence Extraction Based Single Document Summarization. International Institute of Information Technology, Hyderabad, India, 5.
    def getSentencePositionScore(self, i, sentenceCount):#传入第I个句子，以及句子总数 对句子在文中出现的位置取一个权重
        normalized = i / (sentenceCount * 1.0)

        if normalized > 0 and normalized <= 0.1:
            return 0.17
        elif normalized > 0.1 and normalized <= 0.2:
            return 0.23
        elif normalized > 0.2 and normalized <= 0.3:
            return 0.14
        elif normalized > 0.3 and normalized <= 0.4:
            return 0.08
        elif normalized > 0.4 and normalized <= 0.5:
            return 0.05
        elif normalized > 0.5 and normalized <= 0.6:
            return 0.04
        elif normalized > 0.6 and normalized <= 0.7:
            return 0.06
        elif normalized > 0.7 and normalized <= 0.8:
            return 0.04
        elif normalized > 0.8 and normalized <= 0.9:
            return 0.04
        elif normalized > 0.9 and normalized <= 1.0:
            return 0.15
        else:
            return 0


     #分割文档句子  ,分割句子单词，分割文章总单词



    def removePunctations(self, text):#移除标点
        return ''.join(t for t in text if t.isalnum() or t == ' ')# isalnum() 方法检测字符串是否由字母和数字组成







