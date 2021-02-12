import praw

class Filter:
	# filters will return True if they fail

	def submissionScore(submission, minScore):
		return (submission.score < minScore)