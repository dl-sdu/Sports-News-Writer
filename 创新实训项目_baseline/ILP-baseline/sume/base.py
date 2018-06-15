# -*- coding: utf-8 -*-

""" Base structures and functions for the sume module.

    Base contains the Sentence, LoadFile and State classes.


    author: florian boudin (florian.boudin@univ-nantes.fr)
    version: 0.1
    date: Nov. 2014
"""
'''
句子中的每个词都对应一个二值变量表示该词是否保留，并且每个词都有一个打分（比如tf-idf），目标函数就是最大化句子中的词的打分；
既然是规划那当然要给出限制，最简单的限制比如说至少保留一个词，再比如说当形容词被保留时其修饰的词也要保留（根据parse tree）。
'''
import re
import os
import codecs
from collections import Counter
import jieba
import jieba.posseg as pseg
import xlrd
class State:
    """ State class

    Internal class used as a structure to keep track of the search state in
    the tabu_search method.  #内部的类用来跟踪搜索状态在搜索方法中

    Args:
        subset (set): a subset of sentences   句子的子集
        concepts (Counter): a set of concepts for the subset 子集的概念集合
        length (int): the length in words  单词的长度
        score (int): the score for the subset   子集的分数
    """
    def __init__(self):
        self.subset = set()
        self.concepts = Counter()
        self.length = 0
        self.score = 0

class Sentence:
    """The sentence data structure.  #句子数据结构

    Args: 
        tokens (list of str): the list of word tokens.   #单词表示列表
        doc_id (str): the identifier of the document from which the sentence
          comes from.      #文档id 用来识别句子从何处来
        position (int): the position of the sentence in the source document.  #句子在源文档中的位置
    """
    def __init__(self, tokens, doc_id, position):

        self.tokens = tokens
        """ tokens as a list. """

        self.doc_id = doc_id
        """ document identifier of the sentence. """

        self.position = position
        """ position of the sentence within the document. """

        self.concepts = []
        """ concepts of the sentence. """

        self.untokenized_form = ''
        """ untokenized form of the sentence. """

        self.length = 0
        """ length of the untokenized sentence. """

class LoadFile(object):
    """Objects which inherit from this class have read file functions.  有读取文件的方法

    """

    def __init__(self, input_directory):
        """
        Args:
            input_file (str): the path of the input file.  #输入文件的路径
            use_stems (bool): whether stems should be used instead of words,
              defaults to False.#是否stems应该被使用，而不是单词

        """
        self.input_directory = input_directory
        self.sentences = []

    def read_documents(self):
            """Read the input files in the given directory.
               #在给定路径下，阅读文件
        Load the input files and populate the sentence list. Input files are
        expected to be in one tokenized sentence per line format.

        Args:
            file_extension (str): the file extension for input documents,
              defaults to txt.
            """
            infile=re.findall(r'[0-9]*',self.input_directory)[0]

            text = xlrd.open_workbook(self.input_directory)
            table = text.sheets()[0]  # 获取所有表格(worksheet)的名字

            rows = table.nrows
            lines= []

            for i in range(rows):
                # print (6)
                lines.append("第" + str(table.cell(i, 1).value) + '分钟' + str(table.cell(i, 0).value) + "比分" + str(
                    table.cell(i, 2).value) + '。' + "\n")

                # load the sentences
            print(lines)

                # loop over sentences
            for i in range(len(lines)):
                    print(lines[i].strip())
                    # split the sentence into tokens
                    tokens = segment(self,lines[i].strip(), lower=True)
                   # print(tokens)
                    # add the sentence
                    if len(tokens) > 0:      #token象征
                        sentence = Sentence(tokens, infile, i)
                        untokenized_form = untokenize(tokens)
                        sentence.untokenized_form = untokenized_form
                        sentence.length = len(untokenized_form.split(' '))
                        #print(sentence.length)
                        self.sentences.append(sentence)

def untokenize(tokens):
    """Untokenizing a list of tokens. 

    Args:
        tokens (list of str): the list of tokens to untokenize.

    Returns:
        a string

    """
    text = u' '.join(tokens)
    text = re.sub(u"\s+", u" ", text.strip())
    text = re.sub(u" ('[a-z]) ", u"\g<1> ", text)
    text = re.sub(u" ([\.;,-]) ", u"\g<1> ", text)
    text = re.sub(u" ([\.;,-?!])$", u"\g<1>", text)
    text = re.sub(u" _ (.+) _ ", u" _\g<1>_ ", text)
    text = re.sub(u" \$ ([\d\.]+) ", u" $\g<1> ", text)
    text = text.replace(u" ' ", u"' ")
    text = re.sub(u"([\W\s])\( ", u"\g<1>(", text)
    text = re.sub(u" \)([\W\s])", u")\g<1>", text)
    text = text.replace(u"`` ", u"``")
    text = text.replace(u" ''", u"''")
    text = text.replace(u" n't", u"n't")
    text = re.sub(u'(^| )" ([^"]+) "( |$)', u'\g<1>"\g<2>"\g<3>', text)

    # times
    text = re.sub('(\d+) : (\d+ [ap]\.m\.)', '\g<1>:\g<2>', text)

    text = re.sub('^" ', '"', text)
    text = re.sub(' "$', '"', text)
    text = re.sub(u"\s+", u" ", text.strip())

    return text


def segment(self, text, lower=True):
    """对一段文本进行分词，返回list类型的分词结果，输入的是一个句子

    Keyword arguments:
    lower                  -- 是否将单词小写（针对英文）
    use_stop_words         -- 若为True，则利用停止词集合来过滤（去掉停止词）
    use_speech_tags_filter -- 是否基于词性进行过滤。若为True，则使用self.default_speech_tag_filter过滤。否则，不过滤。
    """

    jieba_result = pseg.cut(text)  # 标注句子分词后每个词的词性


    jieba_result = [w for w in jieba_result]

    # 去除特殊符号
    word_list = [w.word.strip() for w in jieba_result if w.flag != 'x']
    word_list = [word for word in word_list if len(word) > 0]

    if lower:
        word_list = [word.lower() for word in word_list]

    return word_list