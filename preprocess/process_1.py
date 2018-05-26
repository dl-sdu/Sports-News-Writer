# -*- coding: utf-8 -*-
import os
import chardet # detect encoding of file
import re
import pandas as pd
import sys

#!!!TODO
"""1.Remove editor name in the end of report
"""

"""
Generate train_text_data.
According to reports in reportDir, find live_text file. Generate multiple samples
splitd by minutes_list in one game.
"""
#------------------------------------------------------------------------------
reportDir = u"/home/dell-u/Spyder/textsum/新浪直播数据/战报"
liveDir = u"/home/dell-u/Spyder/textsum/新浪直播数据/实录"
trainDir = u"/home/dell-u/Spyder/textsum/新浪直播数据/训练集"


def write_segment(live_list, report_list):
    """Write all segment(live_list, report_list) in one game to a file."""
    #assert len(live_list) == len(report_list)
    with open(os.path.join(trainDir, 'train_text_data'), 'a') as train_text_data: # a means append mode
        for r, l in zip(report_list, live_list):
            sample = "abstract=<d> <p> <s> " + r.strip("\r\n") + "</s> </p> </d>"	\
                    + "\t" + "article=<d> <p> <s> " + l.strip("\r\n") + \
                    " . </s> </p> </d>\tpublisher=AFP"
            train_text_data.write(sample + "\n")
        

reportDirList = sorted(os.listdir(reportDir))
for fi, name in enumerate(reportDirList[:]): 
    if fi % 500 == 0:   print fi
    report_path = os.path.join(reportDir, name) 
    
    #!!! for test  " 10.txt"
    if name not in []:
        with open(report_path, 'rb') as report:
            lines = report.readlines()
            #print(chardet.detect(lines[0]))
            encoding = chardet.detect(lines[0])['encoding']
            if encoding == 'GB2312':
                report_text = ''.join(lines).decode('GBK')
        # regex '第^(\d{1,2})分钟' u'[\u7b2c]\d{1,2}[\u5206][\u949f]'
        report_list = re.compile(u'[\u7b2c]\d{1,2}[\u5206][\u949f]').split(report_text)
        minute_list = re.compile(u'[\u7b2c]\d{1,2}[\u5206][\u949f]').findall(report_text)
        if report_list[0] == '':
            report_list.pop(0)        
        if len(report_list) != len(minute_list):
            for i in range(len(minute_list)):
                report_list[i+1] = minute_list[i] + report_list[i+1]
        else:
            for i in range(len(minute_list)):
                report_list[i] = minute_list[i] + report_list[i]
        report_list = [r.encode('utf8') for r in report_list]
        #split the whole game into multiple segments    
        minute_list = [int(s[1:-2]) for s in minute_list] 
        
        
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
        live_list = []
        minute_list.append(live.iat[-2, 1]) #for last segment in live
            
        for index, m in enumerate(minute_list):
            if index == 0:
                seg_df = live[live.time < m]
            elif index == len(minute_list):
                seg_df = live[(live.time <= m) & (live.time >= minute_list[index-1])]
            else:
                seg_df = live[(live.time < m) & (live.time >= minute_list[index-1])]
            live_seg = ''.join(list(seg_df['livetext']))
            try:
                live_set = str(seg_df.iat[0, 1]) + live_seg.encode("utf8") + str(seg_df.iat[-1, -1])
            except:
                continue
            live_list.append(live_set)
        
        write_segment(live_list, report_list)
        
            
#--------------------------------------------------------------------------------   
"""
Remove '\n' in the end of a line that is not end with AFP.
"""

train_text_data = u"/home/dell-u/Spyder/textsum/新浪直播数据/训练集/train_text_data"
train_data = u"/home/dell-u/Spyder/textsum/新浪直播数据/训练集/output"

with open(train_text_data, 'r') as train_text_data, open(train_data, 'w') as train_data:    
    for line in train_text_data:
        #line = re.sub(u'<img .*>', "", line)
        if line[-4:-1] != 'AFP':
            line = line.strip("\n")
        train_data.write(line)
        
          
           
        
