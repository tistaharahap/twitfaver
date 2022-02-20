# Twitfaver [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)

A modern (as of 2022) rework of a Twitter Faver based on your own tweets. Simplest explanation of that this does:

* Get your last 200 tweets
* Create keywords from your tweets
* Search the keywords on Twitter
* Favorite all relevant search results

This is supposedly will invite people that gets their tweets favorited to visit your profile.

Earlier incomplete version of this is available on a [blog post of mine from 2013](https://bango29.com/machine-favorited-tweets-organically-improve-followers-count/).

Today's work is fully dockerized and Python 3.10 is required.

## Running Locally

```bash
$ git clone git@github.com:tistaharahap/twitfaver.git
$ cd twitfaver
$ poetry install
$ cp run-local.sh.example run-local.sh
$ vim run-local.sh # Populate with your credentials
$ chmod +x run-local.sh
$ ./run-local.sh
```

## Docker Run

```bash
$ docker run -d --name twitfaver \
-e API_KEY='' \
-e API_SECRET_KEY='' \
-e ACCESS_TOKEN='' \
-e ACCESS_TOKEN_SECRET='' \
-e MY_SCREEN_NAME='' \
tistaharahap/twitfaver:latest
```

## Environment Variable

| Name             | Required            |
|:-----------------|:--------------------|
| `API_KEY`        | Yes                 |
| `API_SECRET_KEY` | Yes  |
| `ACCESS_TOKEN`   | Yes  |
| `ACCESS_TOKEN_SECRET` | Yes |
| `MY_SCREEN_NAME` | Yes  |

