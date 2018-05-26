# -*- coding: utf-8 -*-

"""Calculate vocabulary frequency."""

import os
from collections import Counter

import jieba
import jieba.analyse  


reportDir = u"/home/dell-u/Spyder/textsum/新浪直播数据/战报"
liveDir = u"/home/dell-u/Spyder/textsum/新浪直播数据/实录"
trainDir = u"/home/dell-u/Spyder/textsum/新浪直播数据/训练集"
train_data = 'train_text_data'


tokens = []
"""
reportDirList = sorted(os.listdir(reportDir))

for fi, name in enumerate(reportDirList[:]): 
    report_path = os.path.join(reportDir, name)
    with open(report_path, "r") as f:
        content = f.readlines()
        content = ''.join(content)
        tags = jieba.analyse.extract_tags(content)
        tokens.extend(tags)
"""     
with open(os.path.join(trainDir, train_data), "r") as f:
    line = f.readline()
    while line:
        tags = jieba.analyse.extract_tags(line)
        tokens.extend(tags)
        line = f.readline()

       
counter = Counter(tokens)

with open("/home/dell-u/Spyder/textsum/textsum/data/train_vocab", 'w') as train_vocab:
    for a in counter.most_common(3000):
        train_vocab.write(a[0].encode('utf8') + " " +str(a[1]) + "\n")
