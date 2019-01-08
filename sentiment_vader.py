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
import csv
import pandas as pd 

tweet_data=pd.read_csv("outfile.csv")
print(tweet_data)