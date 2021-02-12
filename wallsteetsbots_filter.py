import praw

class Filter:
	def minScore(o, minScore):
		return (o.score >= minScore)

	def hasBody(o):
		return (hasattr(o, 'body'))

	def isCaps(text, minRatio):
		alph = list(filter(str.isalpha, text))
		return ((sum(map(str.isupper, alph)) / max(1, len(alph))) > minRatio)