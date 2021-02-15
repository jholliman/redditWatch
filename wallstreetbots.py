import praw
import csv
import os
import os.path

from datetime import datetime, timedelta;

from wallstreetbots_data import Data
from wallsteetsbots_filter import Filter
from wallstreetbots_visualize import Visualize

# SET UP ###################################################################

# initialize reddit instance
reddit = praw.Reddit(client_id="RjjQbu35GDhbbQ",
client_secret="EBVe62blBmVb_2cOJuCBHlnzicrmXA",
user_agent="script:redditWatch:v1.0 (by u/EyeLoveJazz)",
username ="EyeLoveJazz",
password ="aeriallidar")
wsb = reddit.subreddit("wallstreetbets")

# extract symbols and company names
nyseSymbols = {}
with open('stonks.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        nyseSymbols[row[0]] = row[1]

# create our data object and load it with the nyse symbols
data = Data(nyseSymbols)

#check if there is an existing database and load it if yes 

if os.path.isfile('database.json'):
    data.load()
    print ("Found existing WSB database")
else:
    pass

  

############################################################################

# only allow posts newer than 24hr ago
startDateTime = (datetime.now() - timedelta(hours=24))
commentsAdded = 0

# this is the main processing loop for submissions
for submission in wsb.new(limit=100):
    timePosted = datetime.utcfromtimestamp(submission.created_utc) - timedelta(hours=6) # utc -> central
    
    if (timePosted > startDateTime):
        # FILTERING
        if (not Filter.minScore(submission, 2)): # reject score < 2
            continue

        # FLAGS
        isDailyDiscussion = (submission.link_flair_text == "Daily Discussion")
        for comment in submission.comments:
            # FILTERING
            if (not Filter.hasBody(comment)):
                continue

            commentsAdded = data.processSymbols(comment, commentsAdded)

data.save()
print(str(commentsAdded) + " comments added to log")
symbolCounts = data.getHypeRemoved(data.symbolCounts, 0.2)
symbolCounts = data.getMinCount(symbolCounts, 3)
#print(symbolCounts)


visual = Visualize(datetime.today().strftime('%Y-%m-%d'),data, reddit)
reportTest = visual.makeReport()#makes report in sub directory
