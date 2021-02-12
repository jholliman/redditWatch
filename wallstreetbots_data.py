import nltk
from nltk.corpus import stopwords
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from datetime import datetime

class Data:
	# this is a dict of symbol: company name
	nyseSymbols = {}

	#	'symbolCounts': {
	#		'GME': {
	#			'2020-01-22': 10,
	#			'2020-01-23': 11
	#			},
	#		'AMC': {
	#			'2020-01-22': 10,
	#			'2020-01-23': 11
	#			}
	#		}
	symbolCounts = {}

	
	#	'symbolSentiments': {
	#		'GME': {
	#			'2020-01-22': 0.5,
	#			'2020-01-23': 1.3
	#			},
	#		'AMC': {
	#			'2020-01-22': 3.0,
	#			'2020-01-23': 33.3
	#			}
	#		}
	symbolSentiments = {}


	def __init__(self, nyseSymbols):
		self.nyseSymbols = nyseSymbols

	def load(self):
		print('load')

	def save(self):
		print('save')

	def processSymbols(self, comment):
		tokenized = tokenize.word_tokenize(comment.body)

		# comment date
		dateString = datetime.utcfromtimestamp(comment.created).date().isoformat()

		# process counts
		for word in tokenized:
			if (word in self.nyseSymbols.keys()):
				# todo check nyseSymbols.values()
				
				# create symbol dict if doesnt exist
				if word not in self.symbolCounts:
					self.symbolCounts[word] = {}

				# create date in symbol dict if doesnt exist
				if dateString not in self.symbolCounts[word]:
					self.symbolCounts[word][dateString] = 0

				# add one to the count
				self.symbolCounts[word][dateString] += 1

		print(self.symbolCounts)

	def debug(self):
		print(self.nyseSymbols)
