from __future__ import division

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
import pandas as pd
import sys

print(sys.argv)
if len(sys.argv) is 1:
	fname = "outfile.csv"
	title = "All Tweets"
else:
	fname = sys.argv[1]
	title = sys.argv[2]

tweet_text = pd.read_csv(fname)
tweet_list=tweet_text['text'].tolist()

SID = SentimentIntensityAnalyzer()
positive = []
negative = []
neutral = []

mneg = 0
mtweet = ""
for index, tweet in enumerate(tweet_list):
	#if not tweet.strip():
	#	continue
	sentiment = SID.polarity_scores(str(tweet))
	positive.append(sentiment['pos'])
	negative.append(sentiment['neg'])
	neutral.append(sentiment['neu'])

	if sentiment['neu'] > mneg:
		mneg = sentiment['neu']
		mtweet = tweet

print(mtweet)

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