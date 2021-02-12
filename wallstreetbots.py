import praw
import csv
import os

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
from datetime import datetime, tzinfo, timedelta;

from wallstreetbots_data import Data
from wallsteetsbots_filter import Filter

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

data = Data(nyseSymbols)
############################################################################


# process submissions since last market close (4pm Eastern)
# lastClose = datetime.now().replace(hour=16,minute=0,second=0,microsecond=0,tzinfo=tzinfo.tzname('US/Eastern'))
# if (lastClose > datetime.now()):
#    lastClose -= timedelta(hours=24);
lastClose = datetime.now() - timedelta(hours=24)


# this is the main processing loop for submissions
# this will iterate and filter sumissions, and then iterate through comments in that submission
for submission in wsb.new(limit=10):
    timePosted = datetime.utcfromtimestamp(submission.created)
    
    if (timePosted > lastClose):
        # FILTERING
        if (not Filter.minScore(submission, 2)): # reject score < 2
            continue

        # FLAGS
        isDailyDiscussion = (submission.link_flair_text == "Daily Discussion")

        for comment in submission.comments:
            # FILTERING
            if (not Filter.hasBody(comment)):
                continue

            data.processSymbols(comment)
            