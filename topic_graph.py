from __future__ import division

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
import pandas as pd
import sys
from nltk.tokenize import word_tokenize,sent_tokenize
import pickle

fname = "outfile.csv"
title = "Topic Analysis"

tweet_text = pd.read_csv(fname)
tweet_list=tweet_text['text'].tolist()

SID = SentimentIntensityAnalyzer()
positive = []
negative = []
neutral = []

topic='realdonaldtrump'
fp = open("topics_and_keywords.pickle", "rb")
topic_list= pickle.load(fp)
fp.close()

#print(topic_list[0][0])
for i in range(0,len(topic_list)):
	print(topic_list[i][0])
	if topic == topic_list[i][0]:		
		sentiment = SID.polarity_scores(str(tweet_list[i]))
		positive.append(sentiment['pos'])
		negative.append(sentiment['neg'])
		neutral.append(sentiment['neu'])

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as nps
import matplotlib.cm as cm
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(positive, negative, neutral, c=neutral, cmap=cm.spectral, marker='o')

plt.title(title)

ax.set_xlabel('Positive')
ax.set_ylabel('Negative')
ax.set_zlabel('Neutral')

plt.show()