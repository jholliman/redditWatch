import praw
import nltk
import csv
import os
from nltk.corpus import stopwords
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

os.chdir(r"C:/Users/Joel/Documents/redditWatch") 

#initialize reddit instance
reddit = praw.Reddit(client_id="RjjQbu35GDhbbQ",
client_secret="EBVe62blBmVb_2cOJuCBHlnzicrmXA",
user_agent="script:redditWatch:v1.0 (by u/EyeLoveJazz)",
username ="EyeLoveJazz",
password ="aeriallidar")

#confirm that reddit instance works and can write/make posts as well as read
print(reddit.read_only)
wsb = reddit.subreddit("wallstreetbets")
############################################################################

#create list of companies and symbols from NYSE list found online
companyList = []
symbolList = []

with open('stonks.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        name = [row[1]]
        symbol = [row[0]]
        companyList.extend(name)
        symbolList.extend(symbol)


#create list of sentences from WSB daily discussion thread
sentences = []
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

#everytime a ticker is mentioned in WSB discussion thread, add to globalSyms. GlobalSyms is all the tickers mentioned, thus there are numerous duplicates.
#duplicates are then counted to see most discussed symbols. If a stock symbol is mentioned in a sentence that is all (or mainly) capital letters, this is
#referred to as a hype sentence. Tickers mentioned in hype sentences are added to globalHypes. This helps to filter out noise later, as many english words
#become tickers when they are all caps, but real tickers will be mentioned in sentences that aren't hype as well as hype. 
########################################################################################################################################################3
def hotTickers(sentences, nameOfSource):
    #Init arrays for symbols, names, and symbols to potentially be dismissed(hypes)
    globalSyms = []
    globalNames = []
    globalHypes = []

    #name for labelling plots
    name = str(nameOfSource)

    #run all sentences through whichStock
    for sentence in sentences:
        #takes one sentence and finds any symbols, company names, or hype names to populate the global arrays 
        matchedSymbols = []
        matchedCompanies = []
        text = tokenize.word_tokenize(sentence)
        upperCaseCounter = 1
    
        for word in text:
            if word.isupper():
                upperCaseCounter += 1
            if word in symbolList:
                index = symbolList.index(word)
                matchedSymbols.extend([symbolList[index]])
                matchedCompanies.extend([companyList[index]])

        if upperCaseCounter/len(text) > 0.80: #check if this sentence is "hype af" (mainly uppercase letters)
            globalHypes.extend(matchedSymbols)
        globalSyms.extend(matchedSymbols)
        globalNames.extend(matchedCompanies)

    #do a raw count
    symbolC = Counter()
    for d in globalSyms:
        symbolC[d] += 1

    ###filtering around hype letters and mentions
    hypeC = Counter()
    for d in globalHypes:
        hypeC[d] += 1
    tickers = hypeC.keys()

    filteredTickers = []
    for i in tickers:
        sumReg = symbolC.get(i)
        sumHype = hypeC.get(i)
        if sumHype/sumReg > 0.25:
            filteredTickers.extend([i])

    #pop out hype only tickers
    for i in filteredTickers:
        symbolC.pop(i)
    #pop out tickers with few mentions
    nnn = []
    for i in symbolC.keys():
        mentions = symbolC.get(i)
        if mentions < 3:
            nnn.extend([i])
    for i in nnn:
        symbolC.pop(i)

    #make a shitty bar plot
    df = pd.DataFrame.from_dict(symbolC,orient='index')
    df.plot(kind='bar')
    name2 = "Filtered_" + name + ".pdf"
    plt.savefig(name2)
    
    return symbolC
###############################################################################################################################
###############################################################################################################################

hotTickers(sentences, "discussionThread")