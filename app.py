import time
import re
from os import environ

import twitter

from twitfaver.tweet import my_tweets, search_tweets, favorite_tweet
from twitfaver.statistics import score_me
from twitfaver.logging import logger


MY_SCREEN_NAME = environ.get('MY_SCREEN_NAME')
ONE_HOUR = 60 * 60

since_id = None
tweet_ids = set()

logger.info(f'Starting for screen name: {MY_SCREEN_NAME}')


def analyze_and_fave(tweet: twitter.Status):
    text = getattr(tweet, 'text')
    text = re.sub(
        r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''',
        " ",
        text,
    )

    scores = score_me(doc=text, min_score=0.07, bigram=True, trigram=True, count=10)
    keywords = [item[0] for item in scores]
    if not keywords:
        return

    for keyword in keywords:
        tweets = search_tweets(q=keyword, count=50)
        for tweet in tweets:
            tweet_id = getattr(tweet, 'id')
            if tweet_id not in tweet_ids:
                favorite_tweet(tweet=tweet)
                tweet_ids.add(tweet_id)


def main():
    global since_id
    if not MY_SCREEN_NAME:
        raise ValueError()

    while True:
        tweets = my_tweets(since_id=since_id, count=200)

        if tweets:
            since_id = getattr(tweets[0], 'id')
            [analyze_and_fave(tweet=x) for x in tweets if x]

        time.sleep(ONE_HOUR)


if __name__ == '__main__':
    try:
        main()
    except ValueError:
        logger.error('Environment variables for Twitter is not set up correctly')
    except KeyboardInterrupt:
        logger.info('Gracefully exiting..')
