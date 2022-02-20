import time
from typing import List
from os import environ

import twitter

from twitfaver.logging import logger


API_KEY = environ.get('API_KEY')
API_SECRET_KEY = environ.get('API_SECRET_KEY')
ACCESS_TOKEN = environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = environ.get('ACCESS_TOKEN_SECRET')
MY_SCREEN_NAME = environ.get('MY_SCREEN_NAME')
IN_BETWEEN_SLEEP_TIME = 0.5


def get_client() -> twitter.Api:
    if not API_KEY or not API_SECRET_KEY or not ACCESS_TOKEN or not ACCESS_TOKEN_SECRET:
        raise ValueError()
    return twitter.Api(
        consumer_key=API_KEY,
        consumer_secret=API_SECRET_KEY,
        access_token_key=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET,
    )


def my_tweets(since_id: int | None = None, count: int | None = 100) -> List[twitter.Status]:
    client = get_client()
    return client.GetUserTimeline(screen_name=MY_SCREEN_NAME, since_id=since_id, count=count)


def search_tweets(q: str, count: int = 100, max_id: int | None = None) -> List[twitter.Status]:
    logger.info(f'Searching Twitter: q={q}')
    client = get_client()
    return client.GetSearch(term=q, count=count, max_id=max_id)


def favorite_tweet(tweet: twitter.Status, force_sleep: bool = True) -> bool:
    client = get_client()
    tweet_id = getattr(tweet, 'id')
    logger.info(f'Creating favorite: id={tweet_id},text={getattr(tweet, "text")}')

    try:
        client.CreateFavorite(status_id=tweet_id)

        if force_sleep:
            time.sleep(IN_BETWEEN_SLEEP_TIME)

        return True
    except twitter.error.TwitterError:
        return False


def search_and_fave(q: str, count: int | None = 100, max_id: int | None = None, force_sleep: bool = True):
    try:
        results = search_tweets(q=q, count=count, max_id=max_id)
        first_id = getattr(results[0], 'id')
        last_id = getattr(results[-1], 'id')

        faves = list(filter(lambda x: x is True, [favorite_tweet(tweet=x) for x in results]))
        logger.info(f'Created favorite for {len(faves)} tweets')
        logger.info(f'First ID={first_id}, Last ID={last_id}')

        if force_sleep:
            time.sleep(IN_BETWEEN_SLEEP_TIME)
    except twitter.error.TwitterError as exc:
        logger.error(f'Got an error: {exc.message}')
