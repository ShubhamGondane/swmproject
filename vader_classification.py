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
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
import pandas as pd


#Class for the ensemble classifier
class VoteClassifier(ClassifierI):
    
    def __init__(self,*classifiers):
        self._classifiers=classifiers
        
    #finds the sentiment by voting   
    def classify(self,features):
        votes=[]
        for c in self._classifiers:
            v=c.classify(features)
            votes.append(v)
        return mode(votes)
    #Finds the confidence of the assigned sentiment value
    def confidence(self,features):
        votes=[]
        for c in self._classifiers:
            v=c.classify(features)
            votes.append(v)
        choice_votes=votes.count(mode(votes))
        conf=choice_votes/len(votes)
        return conf

documents=[]            
with open('train_data.csv',encoding="utf8") as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for line in readCSV:
        documents.append((line[2],line[1]))

save_documents = open("pickled_algos/documents.pickle","wb")
pickle.dump(documents, save_documents)
save_documents.close()

featuresets=[]

SID = SentimentIntensityAnalyzer()

def find_features(document):
    sentiment_dict=SID.polarity_scores(document)
    features={}
    features['pos']=sentiment_dict['pos']
    features['neg']=sentiment_dict['neg']
    features['neu']=sentiment_dict['neu']
    return features

featuresets=[(find_features(rev),category) for (rev,category) in documents]

random.shuffle(featuresets)

training_set=featuresets[:15000]
testing_set=featuresets[15000:]


classifier=nltk.NaiveBayesClassifier.train(training_set)
#Loading a saved classifier using pickle
#classifier_f=open("naivebayes.pickle","rb")
#classifier=pickle.load(classifier_f)
#classifier_f.close()
#Testing accuracy:
print(" Orginal Naive Bayes Accuracy=",(nltk.classify.accuracy(classifier,testing_set)*100))
#classifier.show_most_informative_features(15)

#saving a classifier using pickle
#==============================================================================
# save_classifier=open("naivebayes.pickle","wb")
# pickle.dump(classifier,save_classifier)
# save_classifier.close() 
#==============================================================================

save_classifier = open("pickled_algos/originalnaivebayes5k.pickle","wb")
pickle.dump(classifier, save_classifier)
save_classifier.close()

#Multinomial Naive Bayes 
MNB_classifier=SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print(" Multinomial Naive Bayes Accuracy=",(nltk.classify.accuracy(MNB_classifier,testing_set)*100))

#==============================================================================
# #Gaussian Naive Bayes doesn't work
# Gauss_classifier=SklearnClassifier(GaussianNB())
# Gauss_classifier.train(training_set)
# print(" Gaussian Naive Bayes Accuracy=",(nltk.classify.accuracy(Gauss_classifier,testing_set)*100))
# 
#==============================================================================
save_classifier = open("pickled_algos/MNB_classifier5k.pickle","wb")
pickle.dump(MNB_classifier, save_classifier)
save_classifier.close()

#Bernoulli Naive Bayes
Bern_classifier=SklearnClassifier(BernoulliNB())
Bern_classifier.train(training_set)
print(" Bernoulli Naive Bayes Accuracy=",(nltk.classify.accuracy(Bern_classifier,testing_set)*100))

save_classifier = open("pickled_algos/BernoulliNB_classifier5k.pickle","wb")
pickle.dump(Bern_classifier, save_classifier)
save_classifier.close()

#LogisticRegression
LogisticRegression_classifier=SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)
print(" LogisticRegression Accuracy=",(nltk.classify.accuracy(LogisticRegression_classifier,testing_set)*100))

save_classifier = open("pickled_algos/LogisticRegression_classifier5k.pickle","wb")
pickle.dump(LogisticRegression_classifier, save_classifier)
save_classifier.close()


#SGDClassifier
SGDClassifier_classifier=SklearnClassifier(SGDClassifier())
SGDClassifier_classifier.train(training_set)
print(" SGDClassifier Accuracy=",(nltk.classify.accuracy(SGDClassifier_classifier,testing_set)*100))

save_classifier = open("pickled_algos/SGDC_classifier5k.pickle","wb")
pickle.dump(SGDClassifier_classifier, save_classifier)
save_classifier.close()
#SVC
'''
SVC_classifier=SklearnClassifier(SVC())
SVC_classifier.train(training_set)
print(" SVC Accuracy=",(nltk.classify.accuracy(SVC_classifier,testing_set)*100))
'''


#Linear SVC
LinearSVC_classifier=SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)
print("Linear SVC Accuracy=",(nltk.classify.accuracy(LinearSVC_classifier,testing_set)*100))

save_classifier = open("pickled_algos/LinearSVC_classifier5k.pickle","wb")
pickle.dump(LinearSVC_classifier, save_classifier)
save_classifier.close()
