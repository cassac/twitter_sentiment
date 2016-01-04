"""
ASSIGNMENT 1 FOR UOW COURSERA DATA SCI COURSE
DATE: 2015/07/03

Summary: Displays individual tweets and their 
corresponding sentiment scores. Does not consider
terms which don't appear in AFINN-111.txt

Run from terminal: 
python tweet_sentiment.py AFINN-111.txt [output filename].txt
"""

import sys
import json
import re
from collections import defaultdict

def start_program():
    print 'Starting tweet analysis...'

def finished_prompt():
    print 'Finished analysis.'  

def lines(sent_file, tweet_file):
	'''
	Assisngs sentiment score to tweet.
	The float(n) may be adjusted to view
	negative/positive tweets. Most fall
	in the range of -15 to 15.
	'''

	sent_content = sent_file.readlines()
	tweet_content = tweet_file.readlines()

	scores = {}
	sentiment_score = 0
	for line in sent_content:
		term, score = line.split("\t")
		scores[term] = int(score)

	tweet_word_score = 0
	for item in tweet_content:
		tweet = json.loads(item)
		try:
			if tweet['lang'] == 'en':
				words_list = re.split('\W', tweet['text'].lower())
				tweet_score = 0
				for word in words_list:
					word = str(word)
					if word in scores:
						tweet_score += scores[word]
				if tweet_score > float(5):
					print tweet_score, tweet['text']
		except:
			pass


def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    start_program()
    lines(sent_file, tweet_file)
    finished_prompt()
    
if __name__ == '__main__':
    main()
