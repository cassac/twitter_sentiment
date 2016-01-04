"""
ASSIGNMENT 1.4 FOR UOW COURSERA DATA SCI COURSE

DATE: 2015/07/03

SUMMARY: Calculates and prints out the frequency 
of terms in all tweets.

RUN IN TERMINAL:
python frequency.py [filename of tweets].txt
"""

import sys
import json
import re
import collections

# Accumulatves total terms from tweets including
# unfiltered terms
total_term_count = 0
# Stores all filtered terms from tweets
filterered_term_list = []
# Used as filter to view results without these words. 
# These words are still counted in total_term_count variable.
skip_these_words = []
# skip_these_words = ['this', 'that', 'your', '&amp;', 'they',
# 					'with', 'like', 'have', 'just', "don't",
# 					'want', 'about', 'will', 'what', 'when',
# 					'from', "can't", "you're", 'been', 'much',
# 					'even', 'their']

def start_prompt():
    print 'Program has started...'

def finished_prompt():
    print 'Program has finished.'

def add_terms_from_tweet(tweet_file):
	"""
	Assigns filtered words to filterered_term_list variable.
	Utilizes len(word) to apply minimum character filter 
	and ignores words in skip_these_words list.
	"""
	# Reads tweets from text file
	tweet_content = tweet_file.readlines()
	for tweet in tweet_content:
		# Turns each tweet into JSON format
		tweet = json.loads(tweet)
		# Some tweets aren't proprly formated because 
		# they have been deleted, therefore
		# utilize try/except
		try:
			# Filter tweets in English language
			if tweet['lang'] == 'en':
				tweet_text = tweet['text']
				for word in tweet_text.split():
					word = word.lower()
					# Increase global variable by one
					global total_term_count
					total_term_count += 1
					# Serves as filter requiring minmimum length
					# and exclusion for words in dictionary
					if len(word) > 3 and word not in skip_these_words:
						filterered_term_list.append(word)
		except:
			pass

def get_term_freq(filterered_term_list):
	"""
	Terms is a list of words and is converted
	to dictionary with term occurrences (total number 
	of times term appeared in all tweets) as values.
	Divides occurrences by total terms in tweets
	to calculate and print out term frequency.
	"""
	# Counter converts list into dictionary with
	# term occurrences 
	c = collections.Counter(filterered_term_list)
	# May adjust number inside most_common(n)
	# to display more or less resutls
	for term in c.most_common(25):
		frequency_percentage = (float(term[1]) / total_term_count) * 100
		print term[0], format(frequency_percentage, '.2f') + '%'

def main():
    tweet_file = open(sys.argv[1])
    start_prompt()
    add_terms_from_tweet(tweet_file)
    get_term_freq(filterered_term_list)
    finished_prompt()

if __name__ == '__main__':
    main()