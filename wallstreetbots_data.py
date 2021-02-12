import nltk

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

		print(comment)

	def debug(self):
		print(self.nyseSymbols)
