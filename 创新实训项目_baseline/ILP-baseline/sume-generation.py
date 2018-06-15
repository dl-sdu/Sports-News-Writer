import sume
import re
# directory from which text documents to be summarized are loaded. Input
# files are expected to be in one tokenized sentence per line format.#文件地址
dir_path = "./file/4.xls"

# create a summarizer, here a concept-based ILP model
s =sume.ConceptBasedILPSummarizer(dir_path)

# load documents with extension 'txt'
s.read_documents()

# compute the parameters needed by the model
# extract bigrams as concepts
s.extract_ngrams()  #抽取ngram词表当做概念词

# compute document frequency as concept weights
s.compute_document_frequency() #计算文档频率当做概念权重

# prune sentences that are shorter than 10 words, identical sentences and  #修剪那些少于10个单词的句子，标识句子以及那些有开始和结束标志的句子
# those that begin and end with a quotation mark
s.prune_sentences(mininum_sentence_length=10)

# solve the ilp model
value, subset = s.solve_ilp_problem()

# outputs the summary
print ('\n'.join([s.sentences[j].untokenized_form for j in subset]))

fo=open('./file/4.txt','w')


out_dict={}#最终输出数组字典

for item in subset:
    #print(item.index, item.weight, item.sentence)

    print( item)
    if (re.findall(r'[0-9]+\.', (s.sentences[item].untokenized_form).replace(' ','')+'\n' , flags=0)):
      m = re.findall(r'[0-9]+\.', (s.sentences[item].untokenized_form).replace(' ','')+'\n', flags=0)
      m = re.sub(r'\.', '', m[0], count=0, flags=0)
      out_dict[(s.sentences[item].untokenized_form).replace(' ','')+'\n'] =int(m)
    else:
        out_dict[(s.sentences[item].untokenized_form).replace(' ','')+'\n'] = 10000#设置完赛时间标号为10000

print(out_dict)
m=sorted(out_dict.items(),key=lambda item:item[1])
print(m)
for i in m:
    print(i[0])
    fo.write(i[0])
fo.close()