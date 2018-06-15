from __future__ import print_function
import util
import Segmentation

from importlib import reload
import sys
import codecs
def segment(self, text):
    res = [util.as_text(text)]  # 返回句子

    util.debug(res)
    util.debug(self.delimiters)

    for sep in self.delimiters:
        text, res = res, []
        for seq in text:
            res += seq.split(sep)  # split() 通过指定分隔符对字符串进行切片
    res = [s.strip() for s in res if len(s.strip()) > 0]
    return res

text = codecs.open('../test/doc/01.txt', 'r', 'utf-8').read()
delimiters = set([util.as_text(item) for item in util.sentence_delimiters])
res = [util.as_text(text)]


for sep in delimiters:
    text, res = res, []
    for seq in text:#他传入的文章就有换行符，所以已经会分割了
        res += seq.split(sep)  # split() 通过指定分隔符对字符串进行切片
        #print(res)
res = [s.strip() for s in res if len(s.strip()) > 0]#去除掉换行符句子得到一个完整的句子列表




