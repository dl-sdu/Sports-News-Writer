# coding=utf-8
import networkx as nx
from semantic_similarity_network import *
from candidate_words import *


class BetweenCentrality:

    def __init__(self):
        self.G = nx.Graph()
        self.bcdict = {}
        self.nword = {}

    def codes_betweeness_centarlity(self, string_sentence):
        """
        function: 计算词语的居间度
        :param: string_sentence :  待分析的短句
        :return: self.bcdict : 词语居间度
        """
        candidate_words_dict, nwword = CandidateWords().get_candidate_list(string_sentence)
        nwword_words = nwword.values()
        length = len(nwword_words)
        for i in range(length):
            self.G.add_node(i)
        E = SemanticSimilarity().similarity_network_edges(string_sentence)
        self.G.add_edges_from(E)
        vd = nx.betweenness_centrality(self.G, k=None, normalized=True, weight=None, endpoints=False, seed=None)
        for i in range(length):
            self.bcdict[nwword_words[i]] = vd[i]
        for i in range(length):
            self.nword[i] = nwword_words[i]
        return self.bcdict

