import pandas as pd 
import sentiment_module as sm 

#reading tweets from output file
tweets=pd.read_csv('outfile.csv')
tweet_list=tweets['text'].tolist()
sentiment_list=[]

#assigning sentiment to tweets
for t in tweet_list:
	s_value,confidence=sm.sentiment(t)
	if(confidence>=0.7):
		sentiment_list.append(s_value)
	else:
		sentiment_list.append('uncertain')
sent_output=pd.DataFrame(columns=['text','sentiment_value'])
sent_output['text']=tweets['text']
sent_output['sentiment_value']=sentiment_list

#creating a csv from dataframe
sent_output.to_csv('sentimentoutput.csv',sep=',')