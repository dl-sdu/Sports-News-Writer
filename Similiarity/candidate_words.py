# coding=utf-8
import jieba.posseg as pseg      #words tagging
import os


class CandidateWords:

        def __init__(self):
            self.stopws = []  # 停用词表
            self.candidate_word = []    # 候选词列表
            self.flag = []  # 候选词的词性
            self.candidate_dict = {}  # candidate_word + flag 词为key，flag为value
            self.nword = {}  # candidate_word (元组)

        def get_stopwd(self):
            """
            function: 获取停用词表(哈工大+百度停用词表)
            :return: 停用词表
            """
            base_dir = os.path.dirname(__file__)  # 获取当前文件夹的绝对路径
            file_path = os.path.join(base_dir, 'stopwords.txt')  # 获取当前文件夹内的文件
            files = open(file_path, "r")  # 读取文件
            stop_words = files.readlines()
            for line in stop_words:
                sw = line.strip('\n')
                sw = sw.decode('utf-8')  # type is str
                self.stopws.append(sw)
            files.close()
            return self.stopws

        def get_candidate_list(self, string_sentence):
            """
            function:使用停用词过滤,
            :param: string_data: 带分析的短句
            :return: candidate_dict: 停用词过滤后的候选词及其词性, nword:候选词词典及其初始化的权重
            """
            stop_words = self.get_stopwd()
            words_tag = pseg.cut(string_sentence)
            for w in words_tag:
                if w.flag != u'x' and (w.word not in stop_words):
                    self.candidate_word.append(w.word.encode("utf-8"))  # 去除停用词后的候选词candidate_word
                    self.flag.append(w.flag.encode("utf-8"))  # 保留候选词的词性
            for i in range(len(self.flag)):
                self.candidate_dict[self.candidate_word[i]] = self.flag[i]   # disorder dict (word:flag)
            for i in range(len(self.candidate_word)):
                self.nword[i] = self.candidate_word[i]
            return self.candidate_dict, self.nword

