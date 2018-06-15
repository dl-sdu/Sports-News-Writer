# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 17:10:57 2017

@author: Mee
"""

import os
import re
import jieba
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import operator
import xlrd
f = open(r'./stopword.txt')  # 停止词
stopwords = f.readlines()
stopwords = [i.replace("\n", "") for i in stopwords]

def cleanData(name):
    setlast = jieba.cut(name, cut_all=False)
    seg_list = [i.lower() for i in setlast if i not in stopwords]
    return " ".join(seg_list)

def calculateSimilarity(sentence, doc):  # 根据句子和句子，句子和文档的余弦相似度
    if doc == []:
        return 0
    vocab = {}
    for word in sentence.split():
        vocab[word] = 0  # 生成所在句子的单词字典，值为0

    docInOneSentence = '';
    for t in doc:
        docInOneSentence += (t + ' ')  # 所有剩余句子合并
        for word in t.split():
            vocab[word] = 0  # 所有剩余句子的单词字典，值为0
    #print(vocab.keys())
    #print( docInOneSentence)
    cv = CountVectorizer(vocabulary=vocab.keys()) #CountVectorizer 类会将文本中的词语转换为词频矩阵，例如矩阵中包含一个元素a[i][j]，它表示j词在i类文本下的词频
   # print(cv)
    docVector = cv.fit_transform([docInOneSentence])
    sentenceVector = cv.fit_transform([sentence])
    #print(sentence)
    #print(sentenceVector)
    return cosine_similarity(docVector, sentenceVector)[0][0]

text= xlrd.open_workbook('./generation_text/4.xls')
table = text.sheets()[0]   # 获取所有表格(worksheet)的名字

rows = table.nrows
text1=[]

for i in range(rows):
   # print (6)3
    text1.append("第"+str(table.cell(i,1).value)+'分钟'+str(table.cell(i,0).value)+"比分"+str(table.cell(i,2).value)+'。'+"\n")
#data = open(r"./news_data.txt")  # 测试文件
#texts = data.readlines()  # 读行
texts = [i[:-1] if i[-1] == '\n' else i for i in text1]
#抽取文章每一行出来
#print(texts)
sentences = []#设置一个句子数组
clean = []#设置一个clean
originalSentenceOf = {}#设置一个原始句子属于..列表

import time

start = time.time()#当前时间的时间戳

# Data cleansing
for line in texts:

    parts = line.split('。')[:-1]  # 句子拆分
    #	print (parts)
    for part in parts:
        cl = cleanData(part)  # 句子切分以及去掉停止词
        #		print (cl)
        sentences.append(part)  # 原本的句子
        clean.append(cl)  # 干净有重复的句子
        originalSentenceOf[cl] = part  # 字典格式
setClean = set(clean)  # 干净无重复的句子
#print(clean)
#print(setClean)
#print(sentences)
# calculate Similarity score each sentence with whole documents
scores = {}
for data in clean:
    temp_doc = setClean - set([data])  # 在除了当前句子的剩余所有句子
    #print(data)
    #print(temp_doc)
    score = calculateSimilarity(data, list(temp_doc))  # 计算当前句子与剩余所有句子的相似度
    scores[data] = score  # 得到相似度的列表
# print score


# calculate MMR
n = 50 * len(sentences) / 100  # 摘要的比例大小
alpha = 0.7
summarySet = []
while n > 0:
    mmr = {}
    # kurangkan dengan set summary
    for sentence in scores.keys():
        if not sentence in summarySet:
            mmr[sentence] = alpha * scores[sentence] - (1 - alpha) * calculateSimilarity(sentence, summarySet)  # 公式
    selected = max(mmr.items(), key=operator.itemgetter(1))[0]#根据每个句子的mmr值 进行排序，获取最大的那个

    summarySet.append(selected)
    #	print (summarySet)
    n -= 1

# rint str(time.time() - start)
fo=open('./generation_text/4.txt','w')


print('\nSummary:\n')



out_dict={}#最终输出数组字典

for sentence in  summarySet:
    #print(item.index, item.weight, item.sentence)

   # print( item)
    if (re.findall(r'[0-9]+\.', originalSentenceOf[sentence].lstrip(' ')+"\n" , flags=0)):
      m = re.findall(r'[0-9]+\.', originalSentenceOf[sentence].lstrip(' ')+"\n", flags=0)
      m = re.sub(r'\.', '', m[0], count=0, flags=0)
      out_dict[originalSentenceOf[sentence].lstrip(' ')+"\n"] =int(m)
    else:
        out_dict[originalSentenceOf[sentence].lstrip(' ')+"\n"] = 10000#设置完赛时间标号为10000

print(out_dict)
m=sorted(out_dict.items(),key=lambda item:item[1])
print(m)
for i in m:
    print(i[0])
    fo.write(i[0])

fo.close()
print('=============================================================')
print('\nOriginal Passages:\n')