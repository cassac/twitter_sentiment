"""
ASSIGNMENT 1 FOR UOW COURSERA DATA SCI COURSE

DATE: 2015/07/03

Summary: Displays top terms in tweet file, number
of occurrences and average sentiment score. Terms which
are not included in AFINN-111.txt file are assigned
scores based on the averaged sentiment score for all the
tweets they appeared in.

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

# Stores amount of tweets containing legitimate non afinn words
tweets_with_non_afinn_words_count = 0

# List of words to filter out in get_tweet_words()
garbage = ['http', 'https']
# -------------------

def start_prompt():
	"""
	Send prompt when program starts
	"""

	print 'Staring term sentiment analysis...'

def finish_prompt():
	"""
	Prints when program is finished running
	"""

	print 'Finished sentiment analysis.'

def initiate_sent_file_tweet_file(sent_file, tweet_file):
	"""
	Initiates sentiment scores passed in through AFINN-111.txt file
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
	Returns list of words in tweet. A couple methods
	have been used to "filter". Best method TBD...
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
	Words in tweet which are also in sentiment file will be assigned
	their corresponding point value. Words NOT found in file will be
	assigned first assigned score of 0 then assigned calculated score
	in a second_round_analysis function.
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

		# Reference and update variable. Will be used to normalize words
		# across all tweets.
		global tweets_with_non_afinn_words_count
		tweets_with_non_afinn_words_count += 1

		for word in non_afinn_words_set:
			non_afinn_word_scores_dict[word]['occurrences'] += 1
			non_afinn_word_scores_dict[word]['accumulatave_points'] += tweet_initial_sent_score

def assign_sent_scores_for_non_afinn_words():
	for word in non_afinn_word_scores_dict:
		non_afinn_word_scores_dict[word]['final_sent_score'] = (
			non_afinn_word_scores_dict[word]['accumulatave_points'] /
			non_afinn_word_scores_dict[word]['occurrences']
			)

def calculate_tweet_sent_score(afinn_word_scores_dict, filtered_tweets_list):

	for tweet in filtered_tweets_list[:100]:

		tweet_sent_points = 0
		tweet_word_count = 0
		tweet_words = tweet_word_filter(tweet)
		
		for word in tweet_words:

			tweet_word_count += 1

			if word in non_afinn_word_scores_dict:
				print 'non-afinn word: ', word, non_afinn_word_scores_dict[word]['final_sent_score']
			
			elif word in afinn_word_scores_dict:
				print 'afinn word: ', word, afinn_word_scores_dict[word]
				
			else:
				'word not found: ', word

	# return sent_score

def tweet_analysis(afinn_word_scores_dict, filtered_tweets_list):
	"""
	Iterates tweets list through two functions. The first function
	will create a dictionary for non-afinn words and assign its cumulative
	sentiment points (based off the tweet it appeared in) and number
	of occurences. The second function will assign sentiment scores to
	the tweet based using afinn and non-afinn word scores. *Remember afinn
	words already have sentiment scores while non-afinn word scores are
	dynamically assigned based on the sentiment of the tweets they appeared
	in.
	"""
	for tweet in filtered_tweets_list:

		# Filters tweet for real words
		tweet_words = tweet_word_filter(tweet)

		# Creates non-afinn word dict so we may assign sent
		# points to words not included in AFINN-111.txt file
		create_non_afinn_words_scores_dict(afinn_word_scores_dict, tweet_words)

	# Assign sent scores to non afinn words based on
	# the sent score of tweets they appeared in
	assign_sent_scores_for_non_afinn_words()


	calculate_tweet_sent_score(afinn_word_scores_dict, filtered_tweets_list)
	# Reiterate through tweets and utilize both sent score
	# lists to assign sent score for tweet
	# for tweet in filtered_tweets_list[:10]:
	# 	tweet_words = tweet_word_filter(tweet)
	# 	sent_score = calculate_tweet_sent_score(tweet_words)
		

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

# def display_non_afinn_word_scores_dict():
# 	'''
# 	Prints out the occurrences of words and their
# 	sentiment score. The integers below may be
# 	adjusted to display certain ranges of results
# 	'''
# 	for k,v in non_afinn_word_scores_dict.iteritems():
# 		if v['occurrences'] > 20 and v['final_sent_score'] > 2.5:
# 			print k, v['occurrences'], v['final_sent_score']
# 		else:
# 			pass

def main():
	sent_file = open(sys.argv[1])
	tweet_file = open(sys.argv[2])
	start_prompt()
	afinn_word_scores_dict, tweet_content_block = initiate_sent_file_tweet_file(sent_file, tweet_file)
	filtered_tweets_list = filter_tweets(tweet_content_block)
	tweet_analysis(afinn_word_scores_dict, filtered_tweets_list)
	# display_non_afinn_word_scores_dict()
	# print non_afinn_word_scores_dict, len(non_afinn_word_scores_dict)
	finish_prompt()

if __name__ == '__main__':
    main()