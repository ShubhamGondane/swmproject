from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
import pandas as pd

tweet_text = pd.read_csv('outfile.csv')
tweet_list=tweet_text['text'].tolist()

sentiment_count=[]
SID = SentimentIntensityAnalyzer()
for tweet in tweet_list:
	print(tweet)
	tweet=str(tweet)
	print(SID.polarity_scores(tweet).items())
	sentiment_dict=SID.polarity_scores(tweet)
	sentiment_count.append((sentiment_dict['pos'],sentiment_dict['neg'],sentiment_dict['neu']))

print(sentiment_count)

sentiment_value=[]

for i in sentiment_count:
	index=i.index(max(i))
	if index==0:
		sentiment_value.append('pos')
	elif index==1:
		sentiment_value.append('neg')
	elif index==2:
		if (max(i))==1:
			sentiment_value.append('neu')
		else:
			index=i.index(max(i[0],i[1]))
			if index==0:
				sentiment_value.append('pos')
			elif index==1:
				sentiment_value.append('neg')


sentiment_output=pd.DataFrame(columns=['text','sentiment_value'])

sentiment_output['text']=tweet_list
sentiment_output['sentiment_value']=sentiment_value

sentiment_output.to_csv('sentimentoutput.csv',sep=',')




