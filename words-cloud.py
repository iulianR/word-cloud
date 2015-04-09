#!/usr/bin/python
import tweepy
import json
import time
import sys
import redis
import operator

CLOUD = "cloud"
OTHER = "other"

consumer_key = "8adGill0tekm7zRcBlrBWzLaM"
consumer_secret = "2B876ONhUv6yQGbEYNlz8K2RT4MeAV2R03fgJ3mlhIVZgnjcAj"

tweets = []


class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        tweets.append(status.text)


def auth():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print ("Error! Failed to get authorization url")

    print("Enter the following URL in your browser and authorize the " +
          "application: \n" + redirect_url + "\n")

    verifier = input("Verifier: ")
    try:
        (access_token, access_token_secret) = auth.get_access_token(str (verifier))
    except tweepy.TweepError:
        print ("Error! Failed to get access_token")

    auth.set_access_token (access_token, access_token_secret)
    return tweepy.API(auth)


def get_stopwords ():
    """ Creates the stopwords list by reading the words from the file """
    stopwords = []
    with open('stopwords.txt', 'r') as f:
        for line in f:
            stopwords.append(line.strip('\n'))

    return stopwords


def create_stream(api):
    # Create a stream using our custom listener that appends the tweets to a list
    myStreamListener = MyStreamListener()
    return tweepy.Stream(auth=api.auth, listener=myStreamListener)


def get_json(r, stopwords, length):
    # Just to be able to see that words get pulled every time
    r.flushdb()

    # Other should be 0 for now
    r.hset(CLOUD, OTHER, 0)
    for e in tweets:
        words = e.split(' ')
        for word in words:
            word = word.lower()
            if word in stopwords:
                continue

            # If we haven't reached cloud's given size and we have a new word
            if r.hlen(CLOUD) <= int (length) or r.hexists(CLOUD, word):
                r.hincrby(CLOUD, word, 1)
            else:
                r.hincrby(CLOUD, OTHER, 1)

    # Format the output as a json list of objects
    final = [{"word": word, "count": int (count)} for word, count in r.hgetall(CLOUD).items() if word != OTHER]

    # Sort by number of occurances
    final.sort(key=operator.itemgetter('count'), reverse=True)

    # Add other at the end (according to widget picture in the pdf)
    final.append ({"word": OTHER, "count": int(r.hget(CLOUD, OTHER))})
    return final


def main(seconds, length):
    api = auth()
    stopwords = get_stopwords()
    stream = create_stream(api)

    stream.sample(languages=['en'], async=True)
    time.sleep(int(seconds))
    stream.disconnect()

    # Connect to redis
    r = redis.StrictRedis(host='redis', port=6379, db=0)

    # Get the final json
    json_text = get_json(r, stopwords, length)

    print(json_text)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[2])
    else:
        print("Please specify the command line arguments")
