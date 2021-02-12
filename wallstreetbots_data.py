import json

from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from datetime import datetime, timedelta;

from wallsteetsbots_filter import Filter

class Data:
	# this is a dict of symbol: company name
	nyseSymbols = {}

	# actual data
	symbolCounts = {}
	symbolSentiments = {}
	symbolHype = {}


	def __init__(self, nyseSymbols):
		self.nyseSymbols = nyseSymbols

	def load(self):
		with open('database.json', 'r') as f:
			combinedObject = json.load(f)
			self.symbolCounts = combinedObject['symbolCounts']
			self.symbolSentiments = combinedObject['symbolSentiments']
			self.symbolHype = combinedObject['symbolHype']

	def save(self):
		combinedObject = {}
		combinedObject['symbolCounts'] = self.symbolCounts
		combinedObject['symbolSentiments'] = self.symbolSentiments
		combinedObject['symbolHype'] = self.symbolHype
		
		with open('database.json', 'w') as f:
			json.dump(combinedObject, f, indent=4)


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

		# process counts
		for word in tokenized:
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