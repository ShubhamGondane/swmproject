# If you are getting an error about Python "not being a framework" then obey stackoverflow
# https://stackoverflow.com/a/35107136

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from mpl_toolkits.mplot3d import Axes3D

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

tweet_text = pd.read_csv('outfile.csv')
tweet_list=tweet_text['text'].tolist()

positive = []
negative = []
neutral = []

SID = SentimentIntensityAnalyzer()
for tweet in tweet_list:
	print(tweet)
	sent = SID.polarity_scores(tweet)
	positive.append(sent['pos'])
	negative.append(sent['neg'])
	neutral.append(sent['neu'])


# Let's make out graph.
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.title("All of Twitter in region.") # The name of the topic in question.

#			  X 		Y 		  Z
ax.scatter(positive, negative, neutral, c='r', marker='o')

ax.set_xlabel('Positive')
ax.set_ylabel('Negative')
ax.set_zlabel('Neutral')

plt.show()