# -*- coding: utf-8 -*-
import os
import chardet # detect encoding of file
import re
import pandas as pd
import numpy as np

import jieba
import jieba.analyse  


"""
Generate train_text_data.
According to reports in reportDir, find live_text file. Each sample is a whole game.
"""
#------------------------------------------------------------------------------
reportDir = u"/home/dell-u/Spyder/textsum/新浪直播数据/战报"
liveDir = u"/home/dell-u/Spyder/textsum/新浪直播数据/实录"
trainDir = u"/home/dell-u/Spyder/textsum/新浪直播数据/训练集"

train_data = 'train_text_data'


def write_segment(live_list, report_list):
    """Write live and report in one game to a file."""
    #assert len(live_list) == len(report_list)
    with open(os.path.join(trainDir, train_data), 'a') as train_text_data: # a means append mode
            sample = u"abstract=<d> <p> "
            for r in report_list:
                sample += " <s> " + r.strip("\r\n") + " </s>"              
            sample += " </p> </d> " + "article=<d> <p> "
            for l in live_list:
                sample += " <s> " + l.strip("\r\n") + " </s>"
            sample += " </p> </d>\tpublisher=AFP"
            
            sample = sample.encode("utf-8")
            train_text_data.write(sample + "\n")


# Count how many words in each sentence
num_sent_num_words_matrix = []

reportDirList = sorted(os.listdir(reportDir))
for fi, name in enumerate(reportDirList[:]): 
    if fi % 500 == 0:   print fi
    report_path = os.path.join(reportDir, name) 
    
    #!!! for test  " 10.txt"
    if name  in [" 10.txt"]:
        print name
        with open(report_path, 'rb') as report:
            report_list = report.readlines()
            #print(chardet.detect(report_list[0]))
            encoding = chardet.detect(report_list[0])['encoding']
            if encoding == 'ascii': # it's impossible to be ascii
                continue
            for i in range(len(report_list)):
                if encoding == 'GB2312':
                    report_list[i] = report_list[i].decode('GBK')    
                else:
                    report_list[i] = report_list[i].decode(encoding)    
     
        # find live text according to the report's index
        live_path = os.path.join(liveDir, name[:-4] + '.xls') 
        try:
            live = pd.read_excel(live_path, header=None)
        except IOError:
            continue
        if len(live) == 0:
            print "live is empty", name
            continue
        live.columns = ['livetext', 'time', 'score']
        live_list = live['livetext'].tolist()
                
        #write_segment(live_list, report_list)
        
        
        num_word = []
        for l in live_list:
            tokens = jieba.analyse.extract_tags(l)
            num_word.append(len(tokens))
        num_sent_num_words_matrix.append(num_word)
            
mat = np.array(num_sent_num_words_matrix)                      
np.save("/home/dell-u/Spyder/textsum/num_sent_num_words_matrix.npy", mat)
        