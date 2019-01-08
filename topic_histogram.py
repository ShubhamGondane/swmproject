import matplotlib.pyplot as plt
import numpy as np
import pickle

fp = open("svalues.pickle", "rb")
topic_list= pickle.load(fp)
fp.close()
for x in topic_list:
	if x[0]=='realdonaldtrump':
		list1=[x[1],x[2],x[3]]

x = np.arange(3)
plt.bar(x, height= list1)
plt.xticks(x, ['pos','neg','neu'])
plt.show()