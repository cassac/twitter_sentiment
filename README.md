Twitter Sentiment Ananlysis
======

Individual tweet sentiment, top tags, happiest state and term sentiment.

```AFINN-111.txt``` List of approxiamtely 2500 terms and their corresponding sentiment scores.

```twitterstream.py``` supplied by UW online course. Must get ones own Twitter API credentials. Run script to extract tweets and write to ```.txt``` file.

Run files below with output text file from ```twitterstream.py```

```frequency.py``` Displays frequency (in percentages) of most popular words used in tweets.

```happiest_state.py``` Displays the happiest state solely based on term sentiment scores from ```AFINN-111.txt``` file.

```term_sentiment.py``` Calculates sentiment scores and displays most popular terms for terms not included in ```AFINN-111.txt``` file.

```tweet_sentiment_incl_non_afinn.py``` Calculates and displays sentiment scores for terms included and not included in ```AFINN-111.txt``` file. A different iteration of ```term_sentiment.py``` file.

```tweet_analysis.py``` Calculates sentiment score for individual tweets. Only considers words in ```AFINN-111.txt``` file. Can adjust float value to only display tweets from certain sentiment score range.

```tweet_sentiment.py``` Calculates sentiment score for individual tweets. Only considers words in ```AFINN-111.txt``` file. A different iteration of ```tweet_analysis.py``` file.





