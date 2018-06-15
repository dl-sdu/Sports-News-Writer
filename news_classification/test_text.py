# -*- coding:utf-8 -*-

import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

import jieba

MAX_SEQUENCE_LENGTH = 100

model = load_model('word_vector_cnn.h5')
'''text = open('test.txt', 'r', encoding = 'utf-8').read()
result = jieba.cut(text)
rtext=""
for i in result:
    rtext += i
    rtext += ' '
print (rtext)'''
stopwords=[]
for word in open('stopword.txt','r',encoding='utf-8', errors='ignore').read():
    stopwords.append(word.strip())
   # print(word)
article=open('test.txt','r',encoding='utf-8', errors='ignore').read()
print(stopwords)
words=jieba.cut(article,cut_all=False)
rtext=""
for word in words:
    print(word)
    if word not in stopwords:
        rtext+=word+" "
print (rtext)
tokenizer = Tokenizer()
tokenizer.fit_on_texts(rtext)
print(tokenizer.fit_on_texts(rtext))
sequences = tokenizer.texts_to_sequences(rtext)
print(len(sequences))
print(sequences)
sequence=[]
for i in range(len(sequences)):
    #print(sequences[i])
    if sequences[i]:
        sequence.append(sequences[i][0])

print(sequence)
seq = []
seq.append(sequence)

word_index = tokenizer.word_index
print(word_index)
data = pad_sequences(seq, maxlen=MAX_SEQUENCE_LENGTH)
print(data)
output = model.predict(data)
print (output)















