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
#We select the part of speech we want to consider to assign sentiment
#allowed_word_types=['J','R','V']
allowed_word_types=['J','N','R','V']

all_words=[]
stop_words = stopwords.words('english') + list(string.punctuation)
ps = PorterStemmer()

with open('train_data.csv',encoding="utf8") as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for line in readCSV:
        documents.append((line[2],line[1]))
        r=line[2]
        r = re.sub(r'http\S+', " ",r)
        words = word_tokenize(r)
        filtered_words = [w for w in words if not w in stop_words]
        pos=nltk.pos_tag(filtered_words)
        for w in pos:
            if w[1][0] in allowed_word_types:
                all_words.append(w[0].lower())



#pickling the documents
save_documents = open("pickled_algos/documents.pickle","wb")
pickle.dump(documents, save_documents)
save_documents.close()

#Converting list of word to a frequency distribution
all_words=nltk.FreqDist(all_words)

#Finding n most common words
#print(all_words.most_common(20))
 
#Finding frequency of a particular word               
#print(all_words['great'])


#selecting the 5000 most frequent words as features
word_features=list(all_words.keys())[:5000]

#pickling the word features
save_word_features = open("pickled_algos/word_features5k.pickle","wb")
pickle.dump(word_features, save_word_features)
save_word_features.close()

#checking how many features exist in the given text
def find_features(document):
    words=word_tokenize(document)
    features={}
    for w in word_features:
        features[w]=(w in words)
    return features

#buiding featuresets for the entire data
featuresets=[(find_features(rev),category) for (rev,category) in documents]

random.shuffle(featuresets)

training_set=featuresets[:10000]
testing_set=featuresets[10000:]

#print(featuresets)

'''
testing_documents=[]

for line in open("test.csv"):
    row=line.split()
    testing_documents.append(line[1])
    r=line[1]
    r = re.sub(r'http\S+', " ",r)
    words = word_tokenize(r)
    filtered_words = [w for w in words if not w in stop_words]
    pos=nltk.pos_tag(filtered_words)
    words=word_tokenize(r)
    pos=nltk.pos_tag(words)
    for w in pos:
        if w[1][0] in allowed_word_types:
            all_words.append(w[0].lower())

test_featuresets=[(find_features(rev)) for rev in testing_documents]
testing_set=test_featuresets
'''
classifier=nltk.NaiveBayesClassifier.train(training_set)
#Loading a saved classifier using pickle
#classifier_f=open("naivebayes.pickle","rb")
#classifier=pickle.load(classifier_f)
#classifier_f.close()
#Testing accuracy:
print(" Orginal Naive Bayes Accuracy=",(nltk.classify.accuracy(classifier,testing_set)*100))
classifier.show_most_informative_features(15)

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
'''
#NuSVC
NuSVC_classifier=SklearnClassifier(NuSVC())
NuSVC_classifier.train(training_set)
print("Nu SVC Accuracy=",(nltk.classify.accuracy(NuSVC_classifier,testing_set)*100))
'''


'''
>>>>>>> cbf05e001d16ff7e950b99d7b173f428d376e9a0
=======
'''

'''
>>>>>>> cbf05e001d16ff7e950b99d7b173f428d376e9a0
#Ensemble classifier
VoteClassifier_classifier=VoteClassifier(classifier,MNB_classifier,Bern_classifier,LogisticRegression_classifier,SGDClassifier_classifier,NuSVC_classifier,LinearSVC_classifier)
print("Vote Classifier Accuracy=",(nltk.classify.accuracy(VoteClassifier_classifier,testing_set)*100))
print("Classification:",VoteClassifier_classifier.classify(testing_set[0][0]),"Confidence %:",VoteClassifier_classifier.confidence(testing_set[0][0]))
print("Classification:",VoteClassifier_classifier.classify(testing_set[1][0]),"Confidence %:",VoteClassifier_classifier.confidence(testing_set[1][0]))
print("Classification:",VoteClassifier_classifier.classify(testing_set[2][0]),"Confidence %:",VoteClassifier_classifier.confidence(testing_set[2][0]))
print("Classification:",VoteClassifier_classifier.classify(testing_set[3][0]),"Confidence %:",VoteClassifier_classifier.confidence(testing_set[3][0]))
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD


=======
'''

'''
>>>>>>> cbf05e001d16ff7e950b99d7b173f428d376e9a0
=======
'''

