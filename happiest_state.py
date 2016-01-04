"""
ASSIGNMENT 1.5 FOR UOW COURSERA DATA SCI COURSE

SUMMARY: Calculates happiest state in continental
USA based on sentimental scores of tweets grouped
by states.

Run script: 
python happiest_state.py AFINN-111.txt [tweets filename].txt

DATE: 2015/07/09
"""

import sys
import json
import re
from collections import defaultdict
from states_helper import states, timezone_list

def start_prompt():
	print 'Program running...'

def get_points_dict(sent_file):
	sent_content = sent_file.readlines()
	scores = {}
	sentiment_score = 0
	for line in sent_content:
		term, score = line.split("\t")
		scores[term] = int(score)
	return scores

def get_sent_score(terms_list, sent_dict):
	sent_score = 0
	for term in terms_list:
		if term in sent_dict:
			sent_score += sent_dict[term]
	return float(sent_score) / len(terms_list)

def get_tweets(tweet_file, sent_dict):
	sent_by_state = defaultdict(int)
	tweet_content = tweet_file.readlines()
	for tweet in tweet_content:
		tweet = json.loads(tweet)
		try:
			if tweet['user']['time_zone'] in timezone_list and tweet['lang'] == 'en':
				location = re.split('[\W\d]', tweet['user']['location'].lower())
				for k, v in states.iteritems():
					if k.lower() in location or v.lower() in location:
						terms_list = tweet['text'].split()
						if len(terms_list) > 0:
							sent_score = get_sent_score(terms_list, sent_dict)
							sent_by_state[k] += sent_score
		except:
			pass

	return sent_by_state

def display_results(sent_scores):
	happiest_state = ''
	happiest_score = 0
	for k, v in sent_scores.iteritems():
		if v > happiest_score:
			happiest_state = k
			happiest_score = v
	print 'The happiest state is', happiest_state,\
		'with a score of', happiest_score

def finish_prompt():
	print 'Program finished.'

def main():
	start_prompt()
	sent_file = open(sys.argv[1])
	tweet_file = open(sys.argv[2])
	sent_dict = get_points_dict(sent_file)
	sent_scores = get_tweets(tweet_file, sent_dict)
	display_results(sent_scores)
 	finish_prompt()

if __name__ == '__main__':
	main()
