from apyori import apriori
import pickle

fp = open("topics_and_keywords.pickle", "rb")
topic_list= pickle.load(fp)
fp.close()

transactions = {}
for topic, transaction in (row for row in topic_list):
    if topic in transactions:
        transactions[topic].append(transaction)
    else:
        transactions[topic] = [transaction]

for topic, transaction in transactions.items():
	for l in list(apriori(transaction)):
		for x in l[2]:
			confidence = x[2]
			if confidence > 0.5:
				'''
				print(topic,end=" ")
				print("Support = ",support,end=" ")
				print("Confidence = ",confidence)
				'''
				pickle_topics = open("pickled_topics.pickle","wb")
				pickle.dump(topic, pickle_topics)
				pickle_topics.close()
			break
		break
