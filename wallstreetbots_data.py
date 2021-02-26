import json
import os
import requests

from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from datetime import datetime, timedelta;

from wallstreetbots_filter import Filter

class Data:
	dbsecret = 'Vlrciba3zM5NbVfOnbNQS0F9juEhKMOTkt1Cmh9h'

	# this is a dict of symbol: company name
	nyseSymbols = {}

	# last polled timestamp (int)
	lastPolled = 0

	# actual data
	symbolCounts = {}
	symbolSentiments = {}
	symbolHype = {}



	def __init__(self, nyseSymbols):
		self.nyseSymbols = nyseSymbols

	def load(self):
		if os.path.exists('database.json'):
			with open('database.json', 'r') as f:
				combinedObject = json.load(f)
				self.loadJson(combinedObject)

	def loadJson(self, o):
		if ('symbolCounts' in o):
			self.symbolCounts = o['symbolCounts']
		if ('symbolSentiments' in o):
			self.symbolSentiments = o['symbolSentiments']
		if ('symbolHype' in o):
			self.symbolHype = o['symbolHype']
		if ('lastPolled' in o):
			self.lastPolled = o['lastPolled']

	def save(self):
		with open('database.json', 'w') as f:
			json.dump(self.getJson(), f, indent=4)

	def getJson(self):
		combinedObject = {}
		combinedObject['symbolCounts'] = self.symbolCounts
		combinedObject['symbolSentiments'] = self.symbolSentiments
		combinedObject['symbolHype'] = self.symbolHype
		combinedObject['lastPolled'] = self.lastPolled

		return combinedObject

	def putToFirebase(self):
		url = 'https://thewallstreetbots-default-rtdb.firebaseio.com/.json'
		url += '?auth=%s' % (self.dbsecret)
		response = requests.put(url, json.dumps(self.getJson()))

	def loadFromFirebase(self):
		url = 'https://thewallstreetbots-default-rtdb.firebaseio.com/.json'
		url += '?auth=%s' % (self.dbsecret)

		response = requests.get(url)
		
		if (response.status_code == requests.codes.ok):
			self.loadJson(json.loads(response.text))


	# helper function for adding to the nested dicts
	def feedSymbolDict(self, symbol, dateString, symbolDict, count=1):
		# create symbol dict if doesnt exist
		if symbol not in symbolDict:
			symbolDict[symbol] = {}

		# create date in symbol dict if doesnt exist
		if dateString not in symbolDict[symbol]:
			symbolDict[symbol][dateString] = 0

		# add one to the count
		symbolDict[symbol][dateString] += count


	def processSymbols(self, comment):
		tokenized = tokenize.word_tokenize(comment.body)
		
		# comment date (todo localtime)
		dateString = (datetime.utcfromtimestamp(comment.created_utc) - timedelta(hours=6)).date().isoformat()

		# is all caps?
		hype = Filter.isCaps(comment.body, 0.8)

		for word in tokenized:
			word = word.lstrip('$') # remove a leading $ so we can catch "$GME"

			if (word in self.nyseSymbols.keys()):
				self.feedSymbolDict(word, dateString, self.symbolCounts)

				if hype:
					self.feedSymbolDict(word, dateString, self.symbolHype)


	def getHypeRemoved(self, symbolDict, hypeRatio):
		filtered = {}
		
		for symbol in symbolDict:
			for dateString in symbolDict[symbol]:
				# if symbol exists in hype, check the ratio
				if symbol in self.symbolHype:
					if dateString in self.symbolHype[symbol]:
						ratio = self.symbolHype[symbol][dateString] / symbolDict[symbol][dateString]
						if (ratio > hypeRatio):
							continue # was seen in to many all caps sentences

				self.feedSymbolDict(symbol, dateString, filtered, symbolDict[symbol][dateString])

		return filtered

	def getMinCount(self, symbolDict, minCount):
		filtered = {}

		for symbol in symbolDict:
			for dateString in symbolDict[symbol]:
				if (symbolDict[symbol][dateString] >= minCount):
					self.feedSymbolDict(symbol, dateString, filtered, symbolDict[symbol][dateString])

		return filtered