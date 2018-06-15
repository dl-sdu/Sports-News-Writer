#-*- encoding:utf-8 -*-
from __future__ import print_function
from importlib import reload
import sys

import xlrd
import re
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass
import codecs
from lexrank import Rank_Sentence1

#text = codecs.open('../TextRank4ZH-master/test/doc/01.txt', 'r', 'utf-8').read()
#text= openpyxl.load_workbook(filename='/Users/hejie/Desktop/课外学习/数据集/新浪直播数据/实录/0.xls')

'''text= openpyxl.load_workbook(filename='./generation_text/0.xls')
sheets = text.get_sheet_names()   # 获取所有表格(worksheet)的名字
sheet0 = sheets[0]  # 第一个表格的名称
ws = text.get_sheet_by_name(sheet0) # 获取特定的 worksheet
rows = ws.rows
text1=[]

for i in range(rows):
    print (6)
    text1.append("第"+ws.cell(row=i, column=1).value+'分钟'+ws.cell(row=i, column=0).value+"比分"+ws.cell(row=i, column=2).value)
'''
text= xlrd.open_workbook('./generation_text/4.xls')
table = text.sheets()[0]   # 获取所有表格(worksheet)的名字

rows = table.nrows
text1=[]
count=0
for i in range(rows):
   # print (6)3
    count+=1
    text1.append("第"+str(table.cell(i,1).value)+'分钟'+str(table.cell(i,0).value)+"比分"+str(table.cell(i,2).value)+'。'+"\n")
#print(text1)
tr= Rank_Sentence1()
tr.analyze(text=text1, lower=True, source = 'no_filter')

print()
print( '生成新闻：' )
fo=open('./generation_text/4.txt','w')

out_dict={}#最终输出数组字典

for item in tr.keysentences[:count//2]:
    #print(item.index, item.weight, item.sentence)

    print( item)
    if (re.findall(r'[0-9]+\.', item , flags=0)):
      m = re.findall(r'[0-9]+\.', item, flags=0)
      m = re.sub(r'\.', '', m[0], count=0, flags=0)
      out_dict[item] =int(m)
    else:
        out_dict[item] = 10000#设置完赛时间标号为10000

print(out_dict)
m=sorted(out_dict.items(),key=lambda item:item[1])
print(m)
for i in m:
    print(i[0])
    fo.write(i[0])
