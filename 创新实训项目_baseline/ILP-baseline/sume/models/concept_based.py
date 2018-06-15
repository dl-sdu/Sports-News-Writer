# -*- coding: utf-8 -*-

""" Concept-based ILP summarization methods.

    authors: Florian Boudin (florian.boudin@univ-nantes.fr)
             Hugo Mougard (hugo.mougard@univ-nantes.fr)
    version: 0.2
    date: May 2015
"""

from sume.base import Sentence, State, untokenize, LoadFile

from collections import defaultdict, deque

import os
import re
import codecs
import random
import sys

import nltk
import pulp


class ConceptBasedILPSummarizer(LoadFile):
    """Implementation oasedILPSummarizer(dir_path)
f the concept-based ILP model for summarization.

    The original algorithm was published and described in:

      * Dan Gillick and Benoit Favre, A Scalable Global Model for Summarization,
        *Proceedings of the NAACL HLT Workshop on Integer Linear Programming for
        Natural Language Processing*, pages 10–18, 2009.
        
    """
    def __init__(self, input_directory):
        """
        Args:
            input_directory (str): the directory from which text documents to
              be summarized are loaded.

        """
        self.input_directory = input_directory
        self.sentences = []#句子数组
        self.weights = {}#权重列表
        self.c2s = defaultdict(set)#defaultdict是其中一个方法，就是给字典value元素添加默认类型  集合类型，不存在哈希值
        self.concept_sets = defaultdict(frozenset)#frozenset是冻结的集合，它是不可变的，存在哈希值
        self.stoplist = nltk.corpus.stopwords.words('english')#停止词列表
        self.word_frequencies = defaultdict(int)#添加int类型
        self.w2s = defaultdict(set)#添加集合类型

    def extract_ngrams(self, n=2):
        """Extract the ngrams of words from the input sentences.

        Args:
            n (int): the number of words for ngrams, defaults to 2
        """

        for i, sentence in enumerate(self.sentences):
           # print(len(sentence.tokens))
            # for each ngram of words
            for j in range(len(sentence.tokens)-(n-1)):

                # initialize ngram container
                ngram = []


                # for each token of the ngram
                for k in range(j, j+n):
                    ngram.append(sentence.tokens[k].lower())#加入ngram词表 每个句子有蛮多个ngram词表


                # do not consider ngrams composed of only stopwords 只包含停止词的ngram我们不要
                stops = [t for t in ngram if t in self.stoplist]
                if len(stops) == len(ngram):
                    continue

                #print(ngram)
                # add the ngram to the concepts
                self.sentences[i].concepts.append(' '.join(ngram))
            #print(self.sentences[i].concepts)
    def compute_document_frequency(self):
        """Compute the document frequency of each concept.
           计算每个概念在文档中的频率
        """
        for i in range(len(self.sentences)):
            #print(231321213)
            # for each concept
            for concept in self.sentences[i].concepts:

                # add   `the document id to the concept weight container
                if concept not in self.weights:
                    self.weights[concept] = set([])
                self.weights[concept].add(self.sentences[i].doc_id)#如果该概念已经在权重列表中，则权重列表对于该概念添加文档id

        # loop over the concepts and compute the document frequency
        for concept in self.weights:
            self.weights[concept] = len(self.weights[concept])#权重集是指 某一个概念出现在多少个文章中
          #  print(self.weights[concept])
    def compute_word_frequency(self):
        """Compute the frequency of each word in the set of documents. """
        #计算一个单词在文档中出现的频率
        for i, sentence in enumerate(self.sentences):
            for token in sentence.tokens:
                t = token.lower() 
                #print(456457)

                self.w2s[t].add(i)
                self.word_frequencies[t] += 1
                #print( self.w2s[t])
    def prune_sentences(self,mininum_sentence_length=5):
        """Prune the sentences.修剪

        Remove the sentences that are shorter than a given length, redundant冗余的
        sentences and citations from entering the summary.

        Args:
            mininum_sentence_length (int): the minimum number of words for a
              sentence to enter the summary, defaults to 5
            remove_citations (bool): indicates that citations are pruned,  引用
              defaults to True
            remove_redundancy (bool): indicates that redundant sentences are
              pruned, defaults to True

        """
        pruned_sentences = []

        # loop over the sentences
        for sentence in self.sentences:

            # prune short sentences
            if sentence.length < mininum_sentence_length:
                continue

            # prune citations
            first_token, last_token = sentence.tokens[0], sentence.tokens[-1]

            # otherwise add the sentence to the pruned sentence container
            pruned_sentences.append(sentence)

        self.sentences = pruned_sentences
        print(self.sentences)
    def prune_concepts(self, method="threshold", value=1):
        """Prune the concepts for efficient summarization.修剪概念为了高效率的摘要

        Args:
            method (str): the method for pruning concepts that can be whether
              by using a minimal value for concept scores (threshold) or using
              the top-N highest scoring concepts (top-n), defaults to
              threshold.
            value (int): the value used for pruning concepts, defaults to 3.

        """
        # 'threshold' pruning method
        if method == "threshold":
            print(231) #还没用到这个方法
            # iterates over the concept weights
            concepts = self.weights.keys()
            for concept in concepts:
                if self.weights[concept] < value:
                    del self.weights[concept]

        # 'top-n' pruning method
        elif method == "top-n":  #topn方法

            # sort concepts by scores
            sorted_concepts = sorted(self.weights,
                                     key=lambda x: self.weights[x],
                                     reverse=True)

            # iterates over the concept weights
            concepts = self.weights.keys()
            for concept in concepts:
                if concept not in sorted_concepts[:value]:
                    del self.weights[concept]#del语句可以用来删除列表中某一个元素或者是某一个片段

        # iterates over the sentences
        for i in range(len(self.sentences)):#保留那些经过权重筛选后的concept

            # current sentence concepts
            concepts = self.sentences[i].concepts

            # prune concepts
            self.sentences[i].concepts = [c for c in concepts
                                          if c in self.weights]

    def compute_c2s(self):
        """Compute the inverted 倒 concept to sentences dictionary. """

        for i, sentence in enumerate(self.sentences):
            for concept in sentence.concepts:
                self.c2s[concept].add(i)#标注concept单词是哪句话中的

    def compute_concept_sets(self):
        """Compute the concept sets for each sentence."""

        for i, sentence in enumerate(self.sentences):
            for concept in sentence.concepts:
                self.concept_sets[i] |= {concept}#每句话的concept组成一个集合
        print(self.concept_sets[i])
    def greedy_approximation(self, summary_size=1500):
        """Greedy approximation of the ILP model.

        Args:
            summary_size (int): the maximum size in words of the summary,
              defaults to 100.

        Returns:
            (value, set) tuple (int, list): the value of the approximated
              objective function and the set of selected sentences as a tuple.

        """
        # initialize the inverted c2s dictionary if not already created
        if not self.c2s:
            self.compute_c2s()

        # initialize weights
        weights = {}

        # initialize the score of the best singleton单个的
        best_singleton_score = 0

        # compute indices of our sentences  指数
        sentences = range(len(self.sentences))

        # compute initial weights and fill the reverse index
        # while keeping track of the best singleton solution
        for i, sentence in enumerate(self.sentences):
            weights[i] = sum(self.weights[c] for c in set(sentence.concepts))#m某个句子的权重等于句子中所有concept权重之和
            if sentence.length <= summary_size\
               and weights[i] > best_singleton_score:
                best_singleton_score = weights[i]
                best_singleton = i

        # initialize the selected solution properties
        sel_subset, sel_concepts, sel_length, sel_score = set(), set(), 0, 0

        # greedily select a sentence
        while True:

            ###################################################################
            # RETRIEVE THE BEST SENTENCE
            ###################################################################

            # sort the sentences by gain and reverse length
            sort_sent = sorted(((weights[i] / float(self.sentences[i].length),#句子单词平均权重
                                 -self.sentences[i].length,
                                 i)
                                for i in sentences),
                               reverse=True)

            # select the first sentence that fits in the length limit
            for sentence_gain, rev_length, sentence_index in sort_sent:
                if sel_length - rev_length <= summary_size:
                    break
            # if we don't find a sentence, break out of the main while loop
            else:
                break

            # if the gain is null, break out of the main while loop
            if not weights[sentence_index]:
                break

            # update the selected subset properties
            sel_subset.add(sentence_index)
            sel_score += weights[sentence_index]
            sel_length -= rev_length

            # update sentence weights with the reverse index
            for concept in set(self.sentences[sentence_index].concepts):
                if concept not in sel_concepts:
                    for sentence in self.c2s[concept]:
                        weights[sentence] -= self.weights[concept]
            #经过一系列操作之后，句子的权重只计算那些被纳入sel_concepts的concept的权重
            # update the last selected subset property
            sel_concepts.update(self.sentences[sentence_index].concepts)

        # check if a singleton has a better score than our greedy solution
        if best_singleton_score > sel_score:
            return best_singleton_score, set([best_singleton])

        # returns the (objective function value, solution) tuple
        return sel_score, sel_subset

    def tabu_search(self, summary_size=1500, memory_size=10, iterations=100, mutation_size=2):
        """Greedy approximation of the ILP model with a tabu search
          meta-heuristic.启发式

        Args:
            summary_size (int): the maximum size in words of the summary,
              defaults to 100.   摘要最多单词数
            memory_size (int): the maximum size of the pool of sentences
              to ban at a given time, defaults at 5.
            iterations (int): the number of iterations to run, defaults at
              30.   循环30次
            mutation_size (int): number of sentences to unselect and add to
              the tabu list at each iteration.   未被选中的句子，然后被添加到tabu列表在每次循环中

        Returns:
            (value, set) tuple (int, list): the value of the approximated
              objective function and the set of selected sentences as a tuple.返回近似对象函数的值以及选中句子的列表

        """
        # compute concept to sentences and concept sets for each sentence 计算句子概念以及句子概念集
        if not self.c2s:
            self.compute_c2s()
        if not self.concept_sets:
            self.compute_concept_sets()

        # initialize weights
        weights = {}

        # initialize the score of the best singleton
        best_singleton_score = 0

        # compute initial weights and fill the reverse index
        # while keeping track of 跟踪 the best singleton solution
        for i, sentence in enumerate(self.sentences):
            weights[i] = sum(self.weights[c] for c in set(sentence.concepts))
            if sentence.length <= summary_size\
               and weights[i] > best_singleton_score:
                best_singleton_score = weights[i]
                best_singleton = i

        best_subset, best_score = None, 0
        state = State()
        for i in range(iterations):
            queue = deque([], memory_size)#这个对象类似于list列表，不过你可以操作它的“两端”
            # greedily select sentences
            state = self.select_sentences(summary_size,
                                          weights,
                                          state,
                                          queue)
            if state.score > best_score:
                best_subset = state.subset.copy()
                best_score = state.score
            to_tabu = set(random.sample(state.subset, mutation_size))# 从指定序列中随机获取指定长度的片断，相近的句子不再取
            state = self.unselect_sentences(weights, state, to_tabu)
            queue.extend(to_tabu)

        # check if a singleton has a better score than our greedy solution
        if best_singleton_score > best_score:
            return best_singleton_score, set([best_singleton])

        # returns the (objective function value, solution) tuple
        return best_score, best_subset

    def select_sentences(self,summary_size,weights,  state, tabu_set):
        """Greedy sentence selector. 贪婪句子选择器

        Args:
            summary_size (int): the maximum size in words of the summary,
              defaults to 100.
            weights (dictionary): the sentence weights dictionary. This
              dictionnary is updated during this method call (in-place).
            state (State): the state of the tabu search from which to start
              selecting sentences.  tabu搜索方法where开始选择句子
            tabu_set (iterable): set of sentences that are tabu: this
              selector will not consider them. 一些被禁止的句子


        Returns:
            state (State): the new state of the search. Also note that
              weights is modified in-place.

        """
        # greedily select a sentence while respecting the tabu
        while True:

            ###################################################################
            # RETRIEVE THE BEST SENTENCE
            ###################################################################

            # sort the sentences by gain and reverse length
            sort_sent = sorted(((weights[i] / float(self.sentences[i].length),
                                 -self.sentences[i].length,
                                 i)
                                for i in range(len(self.sentences))
                                if self.sentences[i].length + state.length <=
                                summary_size),
                               reverse=True)

            # select the first sentence that fits in the length limit
            for sentence_gain, rev_length, sentence_index in sort_sent:
               if sentence_index not in tabu_set:
                        break
            # if we don't find a sentence, break out of the main while loop
            else:
                break

            # if the gain is null, break out of the main while loop
            if not weights[sentence_index]:
                break

            # update state
            state.subset |= {sentence_index}
            state.concepts.update(self.concept_sets[sentence_index])#用于统计对象元素的更新，原有的Counter计数器对象与新增元素的统计计数值相加
            state.length -= rev_length
            state.score += weights[sentence_index]

            # update sentence weights with the reverse index
            for concept in set(self.concept_sets[sentence_index]):
                if state.concepts[concept] == 1:
                    for sentence in self.c2s[concept]:
                        weights[sentence] -= self.weights[concept]#对于已经出现过在state中的concept，其包含的句子权重要减去它
        return state

    def unselect_sentences(self, weights, state, to_remove):
        """Sentence ``un-selector'' (reverse operation of the
          select_sentences method).

        Args:
            weights (dictionary): the sentence weights dictionary. This
              dictionnary is updated during this method call (in-place).
            state (State): the state of the tabu search from which to start
              un-selecting sentences.
            to_remove (iterable): set of sentences to unselect.

        Returns:
            state (State): the new state of the search. Also note that
              weights is modified in-place.

        """
        # remove the sentence indices from the solution subset
        state.subset -= to_remove
        for sentence_index in to_remove:
            # update state
            state.concepts.subtract(self.concept_sets[sentence_index])
            state.length -= self.sentences[sentence_index].length
            # update sentence weights with the reverse index
            for concept in set(self.concept_sets[sentence_index]):
                if not state.concepts[concept]:
                    for sentence in self.c2s[concept]:
                        weights[sentence] += self.weights[concept]
            state.score -= weights[sentence_index]
        return state

    def solve_ilp_problem(self, summary_size=1500,solver='glpk',  excluded_solutions=[]):
        """Solve the ILP formulation of the concept-based model.

        Args:
            summary_size (int): the maximum size in words of the summary,   摘要最大的单词数
              defaults to 100.
            solver (str): the solver used, defaults to glpk.  缺省解决办法glpk
            excluded_solutions (list of list): a list of subsets of sentences
              that are to be excluded, defaults to []


        Returns:
            (value, set) tuple (int, list): the value of the objective function
              and the set of selected sentences as a tuple.

        """
        # initialize container shortcuts
        concepts = self.weights.keys()#权重关键字
        w = self.weights#权重
        L = summary_size#摘要大小
        C = len(concepts)#权重概念数目
        S = len(self.sentences)#句子长度

        if not self.word_frequencies:
            self.compute_word_frequency()#如果不存在单词频率，则计算单词频率

        tokens = self.word_frequencies.keys()#单词频率的标记
        f = self.word_frequencies #单词频率
        T = len(tokens)#单词数目

        # HACK Sort keys
        concepts = sorted(self.weights, key=self.weights.get, reverse=True)#根据weight的key来进行排序

        # formulation of the ILP problem
        prob = pulp.LpProblem(self.input_directory, pulp.LpMaximize)

        # initialize the concepts binary variables
        c = pulp.LpVariable.dicts(name='c',
                                  indexs=range(C), #权重概念数目
                                  lowBound=0,
                                  upBound=1,
                                  cat='Integer')
        #用来构造变量字典，可以让我们不用一个个地创建Lp变量实例。name指定所有变量的前缀,index是列表，其中的元素会被用来构成变量名
        #lowBound和upBound是下界和上界，默认分别是负无穷到正无穷,cat用来指定变量是离散(Integer,Binary)还是连续(Continuous)。

        # initialize the sentences binary variables
        s = pulp.LpVariable.dicts(name='s',
                                  indexs=range(S), #句子长度
                                  lowBound=0,
                                  upBound=1,
                                  cat='Integer')

        # initialize the word binary variables
        t = pulp.LpVariable.dicts(name='t',
                                  indexs=range(T), #单词数目
                                  lowBound=0,
                                  upBound=1,
                                  cat='Integer')

        # OBJECTIVE FUNCTION
        prob += sum(w[concepts[i]] * c[i] for i in range(C))#使得概念权重*概念变量之和最大


        # CONSTRAINT FOR SUMMARY SIZE 摘要大小的限制
        prob += sum(s[j] * self.sentences[j].length for j in range(S)) <= L #判断是否取句子进入摘要，总长度小于L，s[j]取值应该是1/0

        # INTEGRITY CONSTRAINTS 限制
        for i in range(C):
            for j in range(S):
                if concepts[i] in self.sentences[j].concepts:
                    prob += s[j] <= c[i]#如果s[j]小于等于c[i]，那么prob加进去，不可能出现s[j]进去，c[j]没有的情况

        for i in range(C):
            prob += sum(s[j] for j in range(S)
                        if concepts[i] in self.sentences[j].concepts) >= c[i]  #c[i]肯定是要小于s[j]的

        # WORD INTEGRITY CONSTRAINTS


        # CONSTRAINTS FOR FINDING OPTIMAL SOLUTIONS
        for sentence_set in excluded_solutions:
            prob += sum([s[j] for j in sentence_set]) <= len(sentence_set)-1

        # prob.writeLP('test.lp')

        # solving the ilp problem
        if solver == 'gurobi':
            prob.solve(pulp.GUROBI(msg=0))
        elif solver == 'glpk':
            prob.solve(pulp.GLPK(msg=0))
        elif solver == 'cplex':
            prob.solve(pulp.CPLEX(msg=0))
        else:
            sys.exit('no solver specified')

        # retreive the optimal subset of sentences
        solution = set([j for j in range(S) if s[j].varValue == 1])

        # returns the (objective function value, solution) tuple
        return (pulp.value(prob.objective), solution)
