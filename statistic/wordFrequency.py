# loading in all the essentials for data manipulation
import pandas as pd
import numpy as np
#load inthe NTLK stopwords to remove articles, preposition and other words that are not actionable
from nltk.corpus import stopwords
# This allows to create individual objects from a bog of words
from nltk.tokenize import word_tokenize
# Lemmatizer helps to reduce words to the base form
from nltk.stem import WordNetLemmatizer
# Ngrams allows to group words in common pairs or trigrams..etc
from nltk import ngrams
# We can use counter to count the objects
from collections import Counter
# This is our visual library
import seaborn as sns
import matplotlib.pyplot as plt
import csv,os,sys, time
import nltk
ROOT=os.path.dirname( os.path.dirname( os.path.abspath(__file__)))
LOCAL=os.path.dirname(os.path.abspath(__file__))
NLTK_DATA=os.path.join(ROOT,"nltk_data")
nltk.data.path.append(NLTK_DATA)
# nltk.download("wordnet",download_dir=NLTK_DATA)
# nltk.download("stopwords",download_dir=NLTK_DATA)
# nltk.download("punkt",download_dir=NLTK_DATA)
def word_frequency(sentence):
    ''' Record word for one paragraph '''
    # joins all the sentenses
    # sentence =" ".join(sentence)
    # creates tokens, creates lower class, removes numbers and lemmatizes the words
    new_tokens = word_tokenize(sentence)
    new_tokens = [t.lower() for t in new_tokens]
    stop=stopwords.words('english')
    diy_stopwords=['men', 'would', 'upon', 'war', 'great', 'thing', 'shall', 'year', 'yet', 'many', 'tho', 'part', 'u', 
                 'camp', 'every', 'shall', 'say', 'man', 'two', 'sort', 'may', 'must', 'self', 'well', 'one', 'many', 
                 'know', 'men', 'put', 'either', 'make', 'said', 'much', 'reason', 'able', 'lay', 'never', 'sir', 'see', 
                 'self', 'seem', 'think', 'whole', 'made', 'part', 'bin', 'could', 'new', 'total', 'get', 'thousand', 
                 'le', 'else', 'eight', 'tell', 'shou', 'sure', 'one', 'unto', 'first', 'like', 'without', 'according', 
                 'li', 'per', 'several', 'age', 'majesty', 'hundred', 'twenty', 'let']
    stop.extend(diy_stopwords)
    new_tokens =[t for t in new_tokens if t not in stop]
    new_tokens = [t for t in new_tokens if t.isalpha()]
    lemmatizer = WordNetLemmatizer()
    new_tokens =[lemmatizer.lemmatize(t) for t in new_tokens]
    new_tokens =[t for t in new_tokens if t not in diy_stopwords]
    #counts the words, pairs and trigrams
    counted = Counter(new_tokens)
    counted_2= Counter(ngrams(new_tokens,2))
    counted_3= Counter(ngrams(new_tokens,3))
    #creates 3 data frames and returns thems
    word_freq = pd.DataFrame(counted.items(),  columns=['key','frequency']).sort_values(by='frequency',ascending=False)
    word_pair = pd.DataFrame(counted_2.items(),columns=['key','frequency']).sort_values(by='frequency',ascending=False)
    trigrams  = pd.DataFrame(counted_3.items(),columns=['key','frequency']).sort_values(by='frequency',ascending=False)
    return word_freq,word_pair,trigrams

suffix=time.strftime("%H%M%S",time.localtime())
lister=[]
with open(os.path.join(ROOT,"papers.csv") ,"r", encoding="utf-8") as f:
    read=csv.reader(f)
    lister=[i for i in read]
for index,i in enumerate(lister):
    if not index :continue
    title,path=i[2],i[3]
    content=[]
    name=path.split("/")[-1].split(".")[0]
    txtPath=os.path.join(ROOT,"txt",name+".txt")
    if not len(name) or not os.path.isfile(txtPath): continue
    with open(txtPath ,"r",encoding="utf-8") as f:
        content=f.readlines()  
    print("*"*20)
    print(name)
    print("LENGTH is {}.".format(len(content)))
    word= pd.DataFrame(data=[],columns=['key','frequency'])  
    par = pd.DataFrame(data=[],columns=['key','frequency'])
    tri = pd.DataFrame(data=[],columns=['key','frequency'])
    for para in content:
        stat=word_frequency(para)
        word=pd.concat([word,stat[0]],ignore_index=True)
        par =pd.concat([par, stat[1]],ignore_index=True)
        tri =pd.concat([tri, stat[2]],ignore_index=True)
            
    Stat=[word,par,tri]
    print("Word shape is:",Stat[0].shape)
    print("Pair shape is:",Stat[1].shape)
    # print("Trim shape is:",Stat[2].shape)
    if not Stat[0].shape[0]: exit()
    # exit()
    lister={}
    for (data,n) in zip(Stat,["word","pair","triple"]):
        temp={}
        for i,row in data.iterrows():
            # print(i,row[0],row[1])
            num=temp.setdefault(row[0],0)
            temp[row[0]]=num+row[1]
        lister[n]=pd.DataFrame(temp.items(),  columns=['key','frequency']).sort_values(by='frequency',ascending=False)
    # create subplot of the different data frames
    # print("LENGTH is: ",len(lister["word"]))
    fig, axes = plt.subplots(2,1,figsize=(12,35))
    sns.barplot(ax=axes[0],x='frequency',y='key',  data=lister["word"].head(30))
    sns.barplot(ax=axes[1],x='frequency',y='key',  data=lister["pair"].head(30))
    # sns.barplot(ax=axes[2],x='frequency',y='key',  data=lister["triple"].head(30))\
    path='figures'
    if not os.path.exists(os.path.join(LOCAL,path,suffix)):
        os.mkdir(os.path.join(LOCAL,path,suffix)) 
    plt.savefig(os.path.join(LOCAL,path,suffix,'{}.png'.format(name)),dpi=600)
    print("*"*20)
    # plt.show()
