#!/usr/bin/python
# -*- coding: utf-8 -*-
from parser import Parser
from Segment_sentence2 import Segment_sentence
from Segment_sentence2 import WordSegmentation
import libiary2
class Summarizer:
    def __init__(self):
        self.parser = Parser()#解析器
        self.seg = Segment_sentence(stop_words_file=None,
                                   allow_speech_tags=libiary2.allow_speech_tags,
                                   delimiters=libiary2.sentence_delimiters)
    def summarize(self, text):
        result = self.seg.segment(text=text, lower=False)
        self.sentences = result.sentences#分割出文档句子
        #print(self.sentences)
        (keywords, wordCount) = self.parser.getKeywords(text)

        topKeywords = self.getTopKeywords(keywords[:10], wordCount)

        result1 = self.computeScore(self.sentences,  topKeywords) #计算分数，传入3个参数，句子，标题单词，频率最高的单词10个
        result1 = self.sortScore(result1)#对分数进行排序

        return result1

    def getTopKeywords(self, keywords, wordCount):#得到单词频率最高的几个，然后给他们算分
        # Add getting top keywords in the database here
        for keyword in keywords:
            articleScore = 1.0 * keyword['count'] / wordCount
            keyword['totalScore'] = articleScore * 1.5#针对keyword添加一个新属性 totalscore

        return keywords

    def sortScore(self, dictList):
        return sorted(dictList, key=lambda x: -x['totalScore'])#将分数按从大到小排序

    def sortSentences(self, dictList):

        return sorted(dictList, key=lambda x: x['order'])

    def computeScore(self, sentences,  topKeywords):
        keywordList = [keyword['word'] for keyword in topKeywords]#先把频率最高的几个单词取出来
        summaries = []#设置一个摘要列表
        self.ws = WordSegmentation(stop_words_file=None,
                                   allow_speech_tags=libiary2.allow_speech_tags)
        for i, sentence in enumerate(sentences):#枚举句子
            sent = self.parser.removePunctations(sentence)#去除句子中的标点
            words=self.ws.segment(text=sent, lower=True, use_stop_words=False, use_speech_tags_filter=False)#对句子进行分词

            sbsFeature = self.sbs(words, topKeywords, keywordList)#传入参数，句子单词，文章最高频率单词以及这些单词，返回1/单词数目*句子分数
            dbsFeature = self.dbs(words, topKeywords, keywordList)


            sentenceLength = self.parser.getSentenceLengthScore(words)#理想句子长度是20，求句子长度得分
            sentencePosition = self.parser.getSentencePositionScore(i, len(sentences))#得到句子位置权重
            keywordFrequency = (sbsFeature + dbsFeature) / 2.0 * 10.0
            totalScore = (keywordFrequency * 2.0 + sentenceLength * 0.5 + sentencePosition * 1.0) / 4.0

            summaries.append({
                # 'titleFeature': titleFeature,
                # 'sentenceLength': sentenceLength,
                # 'sentencePosition': sentencePosition,
                # 'keywordFrequency': keywordFrequency,
                'totalScore': totalScore,
                'sentence': sentence,
                'order': i
            })

        return summaries

    def sbs(self, words, topKeywords, keywordList):
        score = 0.0

        if len(words) == 0:
            return 0

        for word in words:
            word = word.lower()
            index = -1

        if word in keywordList:
            index = keywordList.index(word)#返回句子中如果单词出现高频率单词中，返回他是哪个高频率的单词，即下标

        if index > -1:#如果出现有高频率单词
            score += topKeywords[index]['totalScore']#句子分数等于单词分数相加

        return 1.0 / abs(len(words)) * score   #1/单词数目*句子分数

    def dbs(self, words, topKeywords, keywordList):
        k = len(list(set(words) & set(keywordList))) + 1 #得到句子中有几个最高频率的词再加一
        summ = 0.0
        firstWord = {}
        secondWord = {}

        for i, word in enumerate(words):#枚举句子中词语
            if word in keywordList:#如果该词语在高频词表中
                index = keywordList.index(word)#获得该词语在高频词表中的下标

                if firstWord == {}:#如果firstword为空
                    firstWord = {'i': i, 'score': topKeywords[index]['totalScore']}#设置空的firstword 为当前句子中第一个搜索到的高频词语，给定他在句子中的位置以及分数
                else:
                    secondWord = firstWord#如果不为空，有个secword
                    firstWord = {'i': i, 'score': topKeywords[index]['totalScore']}#设置非空的firstword 为当前句子中第n个搜索到的高频词语，给定他在句子中的位置以及分数
                    distance = firstWord['i'] - secondWord['i']#返回句子中两个高频词语的位置差距

                    summ += (firstWord['score'] * secondWord['score']) / (distance ** 2)#sum=句子分数相乘/距离平方

        return (1.0 / k * (k + 1.0)) * summ#返回..
