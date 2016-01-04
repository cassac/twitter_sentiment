"""
ASSIGNMENT 1 FOR UOW COURSERA DATA SCI COURSE
DATE: 2015/07/03

Summary: Retrieves top hash tags for tweets

Run from terminal: 
python top_tags.py [output filename].txt
"""

import sys
import json
from collections import defaultdict, Counter

def top_tags(tweets):
	tweets = tweets.readlines()
	tags = defaultdict(int)
	for tweet in tweets:
		tweet = json.loads(tweet)
		try:
			if tweet['lang'] == 'en':
				text = tweet['text']
				words = [word for word in text.split()]
				for word in words:
					if word[0] == '#':
						tags[word] += 1
		except:
			pass

	for k, v in Counter(tags).most_common(10):
		print k, v

def main():
	print 'Starting...'
	tweets_file = open(sys.argv[1])
	top_tags(tweets_file)
	print 'Finished.'

if __name__ == '__main__':	
	main()