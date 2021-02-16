import pandas as pd
import matplotlib.pyplot as plt
import os
import shutil

from datetime import datetime
from datetime import timedelta

from wallstreetbots_data import Data
from wallstreetbots_filter import Filter

class Visualize:
    def __init__(self, data, reddit):#need to pass it current date, data instance, reddit instance
        self.currentDate = datetime.today()
        self.dateString = self.currentDate.strftime('%Y-%m-%d')
        self.allData = data
        self.reddit = reddit
        reportDir= "report_" + self.dateString#create directory to put the html report and img figures
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

        for symbol in symbolCountsCleaned:#for every symbol

            for date in symbolCountsCleaned[symbol]:#for every date
              
                if (date == self.dateString):#see if the symbol has mentions today

                    dailyTickerNames.append(symbol)#append symbol
                    dailyTickerMentions.append(symbolCountsCleaned[symbol][date])#append mentions of symbol
        
        #make plot
        df = pd.DataFrame({'tickers': dailyTickerNames, 'mentions': dailyTickerMentions})
        df.plot(x='tickers', y='mentions',kind='bar',title = "Symbols Mentioned Today")
        plt.xlabel("")
        imgName = "dailyTickers_" + self.dateString + ".jpg"
        plt.savefig(imgName)

        return(imgName)#return name of img for html report builder


    #plots time series for specified period of days (e.g. 7, 30, 365 )
    def timeSeriesChart(self, period):

        #list of dates in the duration
        dateList = [self.currentDate - timedelta(days=x) for x in range(0,period)]
        
        #remove hype symbols and non mentioned symbols
        symbolCountsCleaned = self.allData.getHypeRemoved(self.allData.symbolCounts, 0.2)
        symbolCountsCleaned = self.allData.getMinCount(self.allData.symbolCounts, 20)

        metric = symbolCountsCleaned

        #this just formats the date nicely after datetime.timedelta... probably a better way
        def getDate(datetime):
            return(datetime.strftime('%Y-%m-%d'))

        dateStringList = list(map(getDate,dateList))
        #print(dateStringList)

        plotTitle = "Symbol mentions in the past " + str(period) + " days"
        periodDict = []
        symbolsIndex = []
        
        for symbol in metric:#for every symbol
            symbolsIndex.append(symbol)#append symbol name for index

            #if ticker mentioned in any of days during period
            intersection = list(set(metric[symbol].keys()) & set(dateStringList))

            if len(intersection)>0:
                metricArray = [0]*period#make array full of zeros

                #if symbol mentioned that day, replace zero with number of mentions
                for date in intersection:
                    metricArray[intersection.index(date)] = metric[symbol][date]

                #reverse array so latest day is on far right of graph
                periodDict.append(list(reversed(metricArray)))
        
        #make data frame(reverse column headers since lists were also reversed)
        df = pd.DataFrame(periodDict, columns = list(reversed(dateStringList)))
        df.index = symbolsIndex
        lines = df.transpose().plot.line(figsize=(9,6),title = plotTitle, fontsize=9)
        plt.legend(loc='upper left')
        imgName = str(period) +"_dayChart_count" + self.dateString + ".jpg"

        plt.savefig(imgName)
        return imgName #return img name for report making


    def makeReport(self):
        
        #build plots and get there figure.jpg name
        dailyChart = self.dailyTickersHistogram()
        weeklyChart = self.timeSeriesChart(4)
        monthlyChart = self.timeSeriesChart(7)
        
        html = """<html><head><body bgcolor = \"#8A8786\"; style=\"font-family:verdana\"><h1 style = \"color: #BA5437\">Wallstreet Bets News</h1><br>"""
    
        html+="<img src="+dailyChart+" alt=dailyChart><br><br>"
        html+="<img src="+weeklyChart+" alt=weeklyChart><br>"
        html+="<img src="+monthlyChart+" alt=monthlyChart><br>"

        html+="<h2>Good Reads from WSB</h2>"

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
        reportName = "dailyReport_" + self.dateString + ".html" 

        with open(reportName, 'w',encoding="utf-8",errors="ignore") as text:
            text.write(html)
        text.close()





