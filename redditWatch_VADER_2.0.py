import praw
import nltk
#nltk.download()  #nead to uncomment this nltk.download to download the language packs (I downloaded all of them)
from nltk.corpus import stopwords
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os
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



wsb = reddit.subreddit("wallstreetbets")
os.chdir(r"/Users/Joel/Documents/redditWatch")

##################do some sentiment stuff
sid = SentimentIntensityAnalyzer()#initialize

new_words = {
    #positive words
    'buy': 2.0,
    'buying':2.0,
    'bought':2.0,
    'mooning':2.0,
    'moon': 2.0,
    'up': 2.0,
    'gainz': 2.0,
    'gain':2.0,
    'gains':2.0,
    'bull':2.0,
    'bullish':2.0,
    'tendies':2.0,
    'hold':2.0,
    'holding':2.0,
    'diamond':2.0,
    'rise':2.0,
    'rising':2.0,
    'calls':2.0,
    'call':2.0,
    'long':2.0,
    'skyrocket':2.0,
    'rocket':2.0,
    #negative words
    'sell':-2.0,
    'selling':-2.0,
    'sold':-2.0,
    'tank':-2.0,
    'tanking':-2.0,
    'loss':-2.0,
    'put':-2.0,
    'puts':-2.0,
    'short':-2.0,
    'shorting':-2.0
}

sid.lexicon.update(new_words)
sentences = []
###########################

########find discussion thread and extract comments
dailyFound = False
discussionId = None
while dailyFound == False:
    for a in wsb.new(limit=80):
        if a.link_flair_text == "Daily Discussion":
            print("found daily discussion")
            discussionId = a.id
            print(a.title)
            dailyFound = True
ddt = reddit.submission(id=discussionId)
comments = ddt.comments
for com in comments:
    if hasattr(com,"body"):
        string = [com.body]
        sentences.extend(string)

#do the sentiment thingy
for sen in sentences:
    ss = sid.polarity_scores(sen)
    print("begin new comment:")
    print(sen)
    compScore = ss.get("compound")
    print("comp score:", compScore)

    #for k in sorted(ss):
        #print('{0}: {1}, '.format(k, ss[k]), end='')
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
