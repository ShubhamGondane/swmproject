import nltk
import random
from nltk.corpus import movie_reviews,stopwords
import pickle
from nltk.stem import PorterStemmer
from nltk.corpus import movie_reviews
import pickle
from nltk.corpus import movie_reviews
import pickle
from nltk.corpus import movie_reviews
import pickle
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.linear_model import LogisticRegression,SGDClassifier
from sklearn.svm import SVC,LinearSVC,NuSVC
from nltk.classify import ClassifierI
from statistics import mode
import string
import re
import pandas as pd 
import csv

common_words = pd.read_csv('common_words.csv')
common_words = list(common_words)
#print("common_words")
#print(common_words)
tweets=pd.read_csv('outfile.csv')
tweet_list=tweets['text'].tolist()

documents=[]
#We select the part of speech we want to consider to assign sentiment
#allowed_word_types=['J','R','V']
allowed_word_types=['N']

all_topics=[]
topics=[]
stop_words = stopwords.words('english') + list(string.punctuation)+["'re"]+["n't"]+["..."]+["dont"]
stop_words=stop_words+common_words
#print("Stop words")
stop_words = set(stop_words)
#print(stop_words)

for x in tweet_list:
	r=str(x)
	#r = re.sub(r'http\S+', " ",r)
	r = r.lower()
	words = word_tokenize(r)
	#filtered_words = [w for w in words if not w in stop_words]
	filtered_words=[]
	for w in words:
		if w  in stop_words:
			continue
		else:
			filtered_words.append(w)
	pos=nltk.pos_tag(filtered_words)
	
	l1=[]
	for w in pos:
		if w[1][0] in allowed_word_types and len(w[0])>2:
			l1.append(w[0].lower())
			all_topics.append(w[0].lower())
	topics.append(l1)

#for x in topics:
#	print(x)

all_topics=nltk.FreqDist(all_topics)
all_pos=nltk.pos_tag(all_topics)
#top_topics=(list(all_topics.keys())[:100])
top_topics=all_topics.most_common(100)
#named_ent=nltk.ne_chunk(all_pos,binary=True)

tlist=[]
for t in top_topics:
	tlist.append(t[0])
fp=open("top_topics.pickle","wb")
pickle.dump(tlist,fp)
fp.close()

sentiment_output=pd.read_csv('sentimentoutput_topic.csv')
sentiment_values=sentiment_output['sentiment_value'].tolist()

sentiment_calc=[]

for i in range(0,len(top_topics)):
	sentiment_calc.append([0,0,0])

for i in range(0,len(top_topics)):
	for j in range(0,len(topics)):
		if top_topics[i][0] in topics[j] and sentiment_values[j]=='neg':
			sentiment_calc[i][1]=sentiment_calc[i][1]+1
		elif top_topics[i][0] in topics[j] and sentiment_values[j]=='pos':
			sentiment_calc[i][0]=sentiment_calc[i][0]+1
		elif top_topics[i][0] in topics[j] and sentiment_values[j]=='neu':
			sentiment_calc[i][2]=sentiment_calc[i][2]+1

svalues_topic=[]
for i in range(0,len(top_topics)):
	svalues_topic.append([tlist[i],sentiment_calc[i][0],sentiment_calc[i][1],sentiment_calc[i][2]])
fp=open("svalues.pickle","wb")
pickle.dump(svalues_topic,fp)
fp.close()
topics_and_keywords=[]

for i in range(0,len(top_topics)):
	for j in range(0,len(topics)):
		if(top_topics[i][0] in topics[j]):
			a=topics[j]
			a = [x for x in a if x != top_topics[i][0]]
			#b=top_topics[i][0]
			#print(b)
			#set_of_topics=set_of_topics
			topics_and_keywords.append([top_topics[i][0],a])

#for i in range(0,len(topics_and_keywords)):
	#print(topics_and_keywords[i])

fp=open("topics_and_keywords.pickle","wb")
pickle.dump(topics_and_keywords,fp)
fp.close()