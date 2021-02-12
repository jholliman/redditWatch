import praw

class Filter:
	def minScore(o, minScore):
		return (o.score > minScore)

	def hasBody(o):
		return (hasattr(o, 'body'))