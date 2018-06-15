# !/usr/bin/python
# -*- coding: utf-8 -*-

from summarizer import Summarizer

from .Segment_sentence2 import Segment_sentence
from . import Segment_sentence2
from . import libiary2

class TextTeaser(object):

    def __init__(self):
        self.summarizer = Summarizer()

    def summarize(self,text,count):
        result = self.summarizer.summarize(text)
        #print(result)
        result = self.summarizer.sortSentences(result[:count])
        result = [res['sentence'] for res in result]

        return result
