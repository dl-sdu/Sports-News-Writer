from sklearn.datasets import fetch_20newsgroups  
#all categories  
#newsgroup_train = fetch_20newsgroups(subset='train')  
#part categories  
categories = ['comp.graphics',  
 'comp.os.ms-windows.misc',  
 'comp.sys.ibm.pc.hardware',  
 'comp.sys.mac.hardware',  
 'comp.windows.x'];  
newsgroup_train = fetch_20newsgroups(subset = 'train',categories = categories); 
print newsgroup_train.target.shape
print newsgroup_train.target[:10]