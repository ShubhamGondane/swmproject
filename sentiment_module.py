import nltk
import random
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer


#Ensemble classifier for deciding using votes
class VoteClassifier(ClassifierI):
    
    def __init__(self,*classifiers):
        self._classifiers=classifiers
        
    #classifies based on votes    
    def classify(self,features):
        votes=[]
        for c in self._classifiers:
            v=c.classify(features)
            votes.append(v)
        return mode(votes)
    #confidence of assigned sentiment
    def confidence(self,features):
        votes=[]
        for c in self._classifiers:
            v=c.classify(features)
            votes.append(v)
        choice_votes=votes.count(mode(votes))
        conf=choice_votes/len(votes)
        return conf
 #Loading all pickle files           
documents_f = open("pickled_algos/documents.pickle", "rb")
documents = pickle.load(documents_f)
documents_f.close()




word_features5k_f = open("pickled_algos/word_features5k.pickle", "rb")
word_features = pickle.load(word_features5k_f)
word_features5k_f.close()

def find_features(document):
    SID = SentimentIntensityAnalyzer()
    sentiment_dict=SID.polarity_scores(document)
    features={}
    features['pos']=sentiment_dict['pos']
    features['neg']=sentiment_dict['neg']
    features['neu']=sentiment_dict['neu']
    return features
'''
featuresets_f = open("pickled_algos/featuresets.pickle", "rb")
featuresets = pickle.load(featuresets_f)
featuresets_f.close()
'''
featuresets=[(find_features(rev),category) for (rev,category) in documents]

random.shuffle(featuresets)
#print(len(featuresets))

testing_set = featuresets[10000:]
training_set = featuresets[:10000]

open_file = open("pickled_algos/originalnaivebayes5k.pickle", "rb")
classifier = pickle.load(open_file)
open_file.close()


open_file = open("pickled_algos/MNB_classifier5k.pickle", "rb")
MNB_classifier = pickle.load(open_file)
open_file.close()



open_file = open("pickled_algos/BernoulliNB_classifier5k.pickle", "rb")
BernoulliNB_classifier = pickle.load(open_file)
open_file.close()


open_file = open("pickled_algos/LogisticRegression_classifier5k.pickle", "rb")
LogisticRegression_classifier = pickle.load(open_file)
open_file.close()


open_file = open("pickled_algos/LinearSVC_classifier5k.pickle", "rb")
LinearSVC_classifier = pickle.load(open_file)
open_file.close()


open_file = open("pickled_algos/SGDC_classifier5k.pickle", "rb")
SGDC_classifier = pickle.load(open_file)
open_file.close()




voted_classifier = VoteClassifier(classifier,MNB_classifier,BernoulliNB_classifier,LogisticRegression_classifier,SGDC_classifier)



#function for deciding sentiment
def sentiment(text):
    feats = find_features(text)
    return voted_classifier.classify(feats),voted_classifier.confidence(feats)