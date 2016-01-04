"""
ASSIGNMENT 1.2 FOR UOW COURSERA DATA SCI COURSE

DATE: 2015/07/03

Summary: Assigns a sentiment score for individual tweets.
Sentiment scores are solely based on words found in 
AFINN-111.txt file. Words not in file will go unaccounted
for in sentiment score. Each tweet is printed out with
it's sentiment score and corresponding text.

RUN IN TERMINAL: 
python tweet_sentiment.py AFINN-111.txt [tweets filename].txt
"""

import sys
import json
import re
from collections import defaultdict

def start_prompt():
    print 'Starting sentiment analysis...'

def finished_prompt():
    print 'Finished analysis.'    

def lines(sent_file, tweet_file):
	# Stores AFINN word scores in dicitonary
	afinn_word_scores_dict = defaultdict(int)
	# Extract AFINN word scores fromt text file
	afinn_word_scores_temp = sent_file.readlines()
	# Iterate through scores and assign to dict
	for line in afinn_word_scores_temp:
		term, score = line.split("\t")
		afinn_word_scores_dict[term] = int(score)
	# Extract tweets from text file
	tweets = tweet_file.readlines()
	# Iterate through tweets
	for tweet in tweets: # Use tweets[:10] to test first 10
		# Turns tweet into JSON format
		tweet = json.loads(tweet)
		# Some tweets have been deleted,
		# so use try/except
		try:
			# Only use English language tweets
			if tweet['lang'] == 'en':
				# Start sent score at 0
				tweet_sent_score = 0
				# Strores amount of AFINN
				# words found in tweet
				afinn_word_count = 0
				# Iterate through words in tweet
				# and assign scores for AFINN words
				for word in tweet['text'].split():
					word = word.lower()
					if word in afinn_word_scores_dict:
						afinn_word_count += 1
						tweet_sent_score += afinn_word_scores_dict[word]
				# Calculate tweet sent score
				tweet_sent_score = tweet_sent_score / afinn_word_count
				# Prints sentiment score and text for tweet
				print tweet_sent_score, "-", tweet['text']
		except:
			pass

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    start_prompt()
    lines(sent_file, tweet_file)
    finished_prompt()

if __name__ == '__main__':
    main()