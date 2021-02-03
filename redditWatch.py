import praw
import nltk
#nltk.download()
from nltk.corpus import stopwords

import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

reddit = praw.Reddit(client_id="RjjQbu35GDhbbQ",
client_secret="EBVe62blBmVb_2cOJuCBHlnzicrmXA",
user_agent="script:redditWatch:v1.0 (by u/EyeLoveJazz)",
username ="EyeLoveJazz",
password ="aeriallidar")

print(reddit.read_only)
allwords = []
usefulwords = []
wsb = reddit.subreddit("wallstreetbets")
count = 0
for i in wsb.new(limit=30):
    count+=1
    if (i.score>20):
        print("new post",count," (score)",i.score,": ", i.title)
        forest = i.comments
        com = 0
        for n in forest:
            #print("comment ", com, ": ", n.body)
            strv = str(n.body)
            listy = strv.split()
            allwords.extend(listy)
            com += 1

for word in allwords:
    if word in stopwords.words('english'):
        pass
    else:
        usefulwords.append(word)
#print(allwords)
#letter_counts = Counter(allwords)
#topten = sort(letter_counts)
#df = pd.DataFrame.from_dict(letter_counts, orient='index')
#df.plot(kind='bar')
#plt.show()
c = Counter()
for d in usefulwords:
    c[d] += 1
print(c.most_common(20))

df = pd.DataFrame.from_dict(c,orient='index')
df.plot(kind='bar')
plt.show()
