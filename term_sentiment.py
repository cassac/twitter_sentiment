"""
ASSIGNMENT 1 FOR UOW COURSERA DATA SCI COURSE

DATE: 2015/07/03

Summary: Assigns sentiment sores for terms not found in
AFINN-111.txt file. Scores are calculated as follows:
1) Sentiment scores are calculated for tweets using
their AFINN-111.txt word scores.
2) A seperare dictionary stores non-afinn words, their
accumulatave points and number of occurrences based on
all the tweets they appeared in.
3) After each tweet has been accounted for the final
scores for non-afinn words are calculated by dividing
their accumulatave sentiment points by the number of
occurrences in all tweets.
4) Prints out [term] [occurrences] [sentiment score]

Run from terminal:
python term_sentiment.py AFINN-111.txt [tweets filename].txt
"""

import sys
import json
import re
from collections import defaultdict

# Global variable(s)
# -------------------
# Stores and combines all words in all tweets not found in afinn file
non_afinn_word_scores_dict = defaultdict(lambda: defaultdict(int))

# List of words to filter out in get_tweet_words()
garbage = ['http', 'https']
# -------------------

def start_prompt():
	"""
	Send prompt when program starts
	"""

	print 'Starting term sentiment analysis...'

def finish_prompt():
	"""
	Prints when program is finished running
	"""

	print 'Finished sentiment analysis.'

def initiate_sent_file_tweet_file(sent_file, tweet_file):
	"""
	Initiates sentiment scores passed in through AFINN-111.txt file
	and initiates tweet content block
	"""
	sent_content = sent_file.readlines()
	tweet_content_block = tweet_file.readlines()
	# Initialize afinn-111.txt word list into dicitionary
	afinn_word_scores_dict = {}
	for line in sent_content:
		term, score = line.split("\t")
		afinn_word_scores_dict[term] = float(score)
	return afinn_word_scores_dict, tweet_content_block

def tweet_word_filter(tweet):
	"""
	Returns list of filtered words in tweet. A couple methods
	have been used to "filter" - word length, "garbage" list, and
	regular expression have been used. Best method TBD...
	"""

	temp = ''
	for word in tweet.split():
		if '@' in word or '#' in word:
			pass
		else:
			temp += ' ' + word
	
	temp = re.split('[\W\d]', temp.lower())
	tweet_words_list = []
	for word in temp:
		if len(word) > 2 and word not in garbage:
			tweet_words_list.append(word)

	return tweet_words_list

def create_non_afinn_words_scores_dict(afinn_word_scores_dict, tweet_words):
	"""
	First, calculates tweet sentiment score based on words in AFINN-111.txt
	file and stores non-afinn words in set. Second, updates non-afinn words
	dictionary with 'occurrences' and 'accumulatave_points', which will
	later be used to calculate sentiment score for non-afinn word when
	all tweets have been processed.
	"""
	tweet_initial_sent_score = 0
	tweet_afinn_words_sent_points = 0
	tweet_afinn_word_count = 0
	non_afinn_words_set = set()

	for word in tweet_words:
		if word in afinn_word_scores_dict:
			tweet_afinn_word_count += 1
			tweet_afinn_words_sent_points += afinn_word_scores_dict[word]
		else:
			# Saves unique non-afinn words to set
			non_afinn_words_set.add(word)
	# Assigns sent score to tweet
	try:
		tweet_initial_sent_score = tweet_afinn_words_sent_points / tweet_afinn_word_count
	except:
		pass

	# Only if there are non afinn words in tweet run for loop
	if len(non_afinn_words_set) > 0:

		for word in non_afinn_words_set:
			non_afinn_word_scores_dict[word]['occurrences'] += 1
			non_afinn_word_scores_dict[word]['accumulatave_points'] += tweet_initial_sent_score

def assign_score_for_non_afinn_words(afinn_word_scores_dict, filtered_tweets_list):
	"""
	Iterates through tweets to create scores for non-afinn words. Then,
	reiterates through non-afinn words dict to assign a final sentiment
	score.
	"""
	for tweet in filtered_tweets_list:

		# Filters tweet for real words
		tweet_words = tweet_word_filter(tweet)

		# Creates non-afinn word dict so we may assign sent
		# points to words not included in AFINN-111.txt file
		create_non_afinn_words_scores_dict(afinn_word_scores_dict, tweet_words)

	# Assign sent scores to non afinn words based on
	# the sent score of tweets they appeared in
	for word in non_afinn_word_scores_dict:
		non_afinn_word_scores_dict[word]['final_sent_score'] = (
			non_afinn_word_scores_dict[word]['accumulatave_points'] /
			non_afinn_word_scores_dict[word]['occurrences']
			)

def filter_tweets(tweet_content_block):
	"""
	Filters for valid tweets where language
	is set to English and returns list
	"""
	filtered_tweets_list = []
	for tweet in tweet_content_block:
		tweet = json.loads(tweet)
		try:
			if tweet['lang'] == 'en':
				filtered_tweets_list.append(tweet['text'])
			else:
				continue
		except:
			pass
	return filtered_tweets_list

def display_non_afinn_word_scores_dict():
	'''
	Prints out the occurrences of words and their
	sentiment score. The integers below may be
	adjusted to display terms located in 
	certain ranges of results (ie. a negative sent score
		will display negative words and a high "occurrences"
		number will display the most popular words)
	'''
	for k, v in non_afinn_word_scores_dict.iteritems():
		if v['occurrences'] > 15 and v['final_sent_score'] > 2.5:
			print k, v['occurrences'], v['final_sent_score']
		else:
			pass

def main():
	sent_file = open(sys.argv[1])
	tweet_file = open(sys.argv[2])
	start_prompt()
	afinn_word_scores_dict, tweet_content_block = initiate_sent_file_tweet_file(sent_file, tweet_file)
	filtered_tweets_list = filter_tweets(tweet_content_block)
	assign_score_for_non_afinn_words(afinn_word_scores_dict, filtered_tweets_list)
	display_non_afinn_word_scores_dict()
	finish_prompt()

if __name__ == '__main__':
    main()