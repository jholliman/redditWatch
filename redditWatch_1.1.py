import praw
import nltk
#nltk.download()  #nead to uncomment this nltk.download to download the language packs (I downloaded all of them)
from nltk.corpus import stopwords
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt


#initialize reddit instance
reddit = praw.Reddit(client_id="RjjQbu35GDhbbQ",
client_secret="EBVe62blBmVb_2cOJuCBHlnzicrmXA",
user_agent="script:redditWatch:v1.0 (by u/EyeLoveJazz)",
username ="EyeLoveJazz",
password ="aeriallidar")

#confirm that reddit instance works and can write/make posts as well as read
print(reddit.read_only)
############################################################################



#searches the newest 20 posts for posts with >20 upvotes, then all grabs words from the commenta section and adds them to giant list
#init some lists
allwords = []

wsb = reddit.subreddit("wallstreetbets")
count = 0


sid = SentimentIntensityAnalyzer()
sentences = []
'''
for a in wsb.search("What are your moves", limit=1):
    print(a.title)
    comments = a.comments
    for com in comments:
        string = str(com.body)
        print(string)
        lines_list = tokenize.sent_tokenize(string)
        ss = sid.polarity_scores(lines_list)
        for k in sorted(ss):
            print('{0}: {1}, '.format(k, ss[k]), end='')
'''
with open('sentences.txt','w',encoding="utf-8",errors="ignore") as f:   
    for a in wsb.search("What are your moves", limit=1):
        print(a.title)
        comments = a.comments
        for com in comments:
            if hasattr(com,"body"):
                string = [com.body]
                #print(string)
                sentences.extend(string)
for sen in sentences:
    ss = sid.polarity_scores(sen)
    print("begin new comment:")
    print(sen)
    for k in sorted(ss):
        print('{0}: {1}, '.format(k, ss[k]), end='')
    print("\n end of comment")



"""

#with open('sentences.txt', 'w',encoding="utf-8",errors="ignore") as f:
    #for item in sentences:
        #f.write("%s\n" % item)


    
#from nltk import tokenize
#lines_list = tokenize.sent_tokenize(paragraph)
#sentences.extend(lines_list)

sentences.extend(tricky_sentences)
sid = SentimentIntensityAnalyzer()
for sentence in sentences:
    print(sentence)
    ss = sid.polarity_scores(sentence)
    for k in sorted(ss):
        print('{0}: {1}, '.format(k, ss[k]), end='')
    print()

print(tricky_sentences)"""


""" for i in wsb.new(limit=5):#for each post in New(limit to 30 posts)
    count+=1
    if (i.score>1):#if post has 20 or more upvotes
        print("new post: ", i.title)  
        forest = i.comments#get comments of the post
        com = 0
        for n in forest:#for each comment
            #print("comment ", com, ": ", n.body)
            strv = str(n.body).split()#get comment body and split
            #listy = strv.split()
            allwords.extend(strv)#extend allwords list to include text from comments
            com += 1
######################################################

#tries to make a list of only useful words by sorting out "stopwords"
usefulwords = []

for word in allwords:
    if word in stopwords.words('english'):
        pass
    else:
        usefulwords.append(word)

c = Counter()
for d in usefulwords:
    c[d] += 1
print(c.most_common(20)) """#print 20 most common "useful words"

#make a shitty bar plot
#df = pd.DataFrame.from_dict(c,orient='index')
#df.plot(kind='bar')
#plt.show()
