import math
import json


# idf score calculation
def idf(word_tokens, words, N):  # words是单词的列表；word_tokens是句子的列表，每一个句子是一个列表；N是句子数；dict是单词的idf字典，保存在idfBg中
    dict = {}
    for word in words:
        for sent in word_tokens:
            if word in sent:
                if word in dict.keys():
                    dict[word] += 1
                else:
                    dict[word] = 1
    for word, count in dict.items():
        dict[word] = math.log((N / float(count)))
    with open("idfBg", "w") as f:
        json.dump(dict, f)
    return dict


# centrality score calculation
def idf_modified_cosine1(x, y, idf):  # x、y是两个句子，是列表（下面在计算的时候利用set去除重复元素）；idf是单词的idf字典
    #print(767)
    sum = 0
    combine = x + y
    for word in set(combine):
        tf1, tf2 = x.count(word), y.count(word)  # count() 方法用于统计某个元素在列表中出现的次数。
        sum += int(tf1) * int(tf2) * float((idf[word] ** 2))

    total1, total2 = 0, 0
    for word in set(x):
        tf = x.count(word)
        total1 += (int(tf) * float(idf[word])) ** 2

    for word in set(y):
        tf = y.count(word)
        total2 += (int(tf) * float(idf[word])) ** 2
    deno = (math.sqrt((total1))) * (math.sqrt((total2)))
    return float(sum) / deno


# for investigation puspose
def get_similarity_matrix(word_tokens, idf):  # word_tokens是句子的列表；idf是单词的idf字典；matrix是一个二维的列表
    matrix = []
    for sent1 in word_tokens:
        row = []
        for sent2 in word_tokens:
            sim = idf_modified_cosine1(sent1, sent2, idf)
            row.append(sim)
        matrix.append(row)
    return matrix
