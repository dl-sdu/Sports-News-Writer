#coding:utf-8
import sys
import keras


VECTOR_DIR = 'vectors.bin'

MAX_SEQUENCE_LENGTH = 100
EMBEDDING_DIM = 128
VALIDATION_SPLIT = 0.16
TEST_SPLIT = 0.2


print( '(1) load texts...')
train_texts = open('train_contents.txt','r',encoding = 'utf-8').read().split('\n')
train_labels = open('train_labels.txt','r',encoding = 'utf-8').read().split('\n')
test_texts = open('test_contents.txt','r',encoding = 'utf-8').read().split('\n')
test_labels = open('test_labels.txt','r',encoding = 'utf-8').read().split('\n')
all_texts = train_texts + test_texts
all_labels = train_labels + test_labels


print ('(2) doc to var...')
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
import numpy as np

tokenizer = Tokenizer()
tokenizer.fit_on_texts(all_texts)
sequences = tokenizer.texts_to_sequences(all_texts)
print(sequences)#单个使用text_to_word_sequent
word_index = tokenizer.word_index
print(word_index)
print('Found %s unique tokens.' % len(word_index))
data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)
labels = to_categorical(np.asarray(all_labels))
print('Shape of data tensor:', data.shape)
print('Shape of label tensor:', labels.shape)


print ('(3) split data set...')
# split the data into training set, validation set, and test set
p1 = int(len(data)*(1-VALIDATION_SPLIT-TEST_SPLIT))
p2 = int(len(data)*(1-TEST_SPLIT))
x_train = data[:p1]                          #训练数据
y_train = labels[:p1]
x_val = data[p1:p2]                          #验证数据
y_val = labels[p1:p2]
x_test = data[p2:]                          #测试数据
print(data[p2:])
y_test = labels[p2:]
print ('train docs: '+str(len(x_train)))
print ('val docs: '+str(len(x_val)))
print ('test docs: '+str(len(x_test)))

print('----------------------------------------')
for i in range(20):
    print (labels[i])


print ('(4) load word2vec as embedding...')
import gensim
from keras.utils import plot_model
w2v_model = gensim.models.KeyedVectors.load_word2vec_format(VECTOR_DIR, binary=True)
embedding_matrix = np.zeros((len(word_index) + 1, EMBEDDING_DIM))
not_in_model = 0
in_model = 0
print (np.shape(embedding_matrix))
for word, i in word_index.items(): 
    if word in w2v_model:#.encode('utf-8').decode('utf-8')
        in_model += 1
        embedding_matrix[i] = np.asarray(w2v_model[word], dtype='float32')
        #print(np.shape(w2v_model[word]))#.encode('utf-8').decode('utf-8')
    else:
        not_in_model += 1

print (str(not_in_model)+' words not in w2v model')
print (str(in_model)+' words in w2v model')
print (word.encode('utf-8').decode('utf-8'))
#print ('w2v_model is ')+w2v_model

from keras.layers import Embedding
embedding_layer = Embedding(len(word_index) + 1,
                            EMBEDDING_DIM,
                            weights=[embedding_matrix],
                            input_length=MAX_SEQUENCE_LENGTH,
                            trainable=False)


print ('(5) training model...')
from keras.layers import Dense, Input, Flatten, Dropout
from keras.layers import Conv1D, MaxPooling1D, Embedding, GlobalMaxPooling1D
from keras.models import Sequential

model = Sequential()
model.add(embedding_layer)           #转化成词向量
model.add(Dropout(0.2))              #丢掉了20%的神经元
model.add(Conv1D(250, 3, padding='valid', activation='relu', strides=1))
model.add(MaxPooling1D(3))
model.add(Flatten())
model.add(Dense(EMBEDDING_DIM, activation='relu'))
model.add(Dense(labels.shape[1], activation='softmax'))
model.summary()
#plot_model(model, to_file='model.png',show_shapes=True)

model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['acc','categorical_accuracy'])
print (model.metrics_names)
model.fit(x_train, y_train, validation_data=(x_val, y_val), epochs=2, batch_size=128)
model.save('word_vector_cnn.h5')

print ('(6) testing model...')
print (model.evaluate(x_test, y_test))
print (model.metrics_names)

        




