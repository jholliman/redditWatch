import pandas as pd
import matplotlib.pyplot as plt
import os
import shutil

from datetime import datetime

from wallstreetbots_data import Data
from wallstreetbots_filter import Filter

class Visualize:
    def __init__(self, date, data, reddit):#need to pass it current date, data instance, reddit instance
        self.currentDate = date
        self.allData = data
        self.reddit = reddit
        reportDir= "report_" + self.currentDate#create directory to put the html report and img figures
        if not os.path.exists(reportDir):#overwrite directory if it exists
            os.makedirs(reportDir)
        else:
            shutil.rmtree(reportDir)           
            os.makedirs(reportDir)
        os.chdir(reportDir)
    
    #daily chart method, only for count really
    def dailyTickersHistogram(self):
        #filter hypes
        symbolCountsCleaned = self.allData.getHypeRemoved(self.allData.symbolCounts, 0.2)

        #filter minimum mentions
        symbolCountsCleaned = self.allData.getMinCount(self.allData.symbolCounts, 10)

        dailyTickerNames = []
        dailyTickerMentions = []

        for symbol in symbolCountsCleaned.keys():#for every symbol

            for date in symbolCountsCleaned[symbol]:

                if (date == self.currentDate):#see if the symbol has mentions today

                    dailyTickerNames.append(symbol)#append symbol
                    dailyTickerMentions.append(symbolCountsCleaned[symbol][date])#append mentions of symbol
        
        #make plot
        df = pd.DataFrame({'tickers': dailyTickerNames, 'mentions': dailyTickerMentions})
        df.plot(x='tickers', y='mentions',kind='bar',title = "Symbols Mentioned Today")
        imgName = "dailyTickers_" + self.currentDate + ".jpg"
        plt.savefig(imgName)

        return(imgName)#return name of img for html report builder
    
    def makeReport(self):
        
        dailyChart = self.dailyTickersHistogram()#get daily chart name
        
        html = """<html><head><body bgcolor = \"#8A8786\"; style=\"font-family:verdana\"><h1 style = \"color: #BA5437\"> 
        Good Reads from WSB</h1><br>
        """ 
        html+="<img src="+dailyChart+" alt=dailyChart>"

        #searches the newest 150 posts for posts with >3000 upvotes and selftext > 2
        #selftext len is zero if post is a link/media
        posts = ""
        wsb = self.reddit.subreddit("wallstreetbets")
        count = 0
        for i in wsb.new(limit=150):
            if (i.score>1000 and len(i.selftext) > 2):
                posts += "<h2>" + i.title + "</h2>"
                posts += "<h3 style = \"color: #274C7D\"> Upvotes: " + str(i.score) + "    Comments: " + str(i.num_comments) + "   Upvote Ratio: " + str(i.upvote_ratio) + "</h3>"
                posts += "<p>" + i.selftext + "</p><br>"
            #get comments of the post

        html += posts + "</body></head></html>"

        #report name
        reportName = "dailyReport_" + self.currentDate + ".html" 

        with open(reportName, 'w',encoding="utf-8",errors="ignore") as text:
            text.write(html)
        text.close()

    





