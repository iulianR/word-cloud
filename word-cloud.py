import tweepy
import json
import time
import sys

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


def create_stream(api):
    myStreamListener = MyStreamListener()
    return tweepy.Stream(auth=api.auth, listener=myStreamListener)


def get_json():
    dict1 = {}
    for e in tweets:
        words = e.split(' ')
        for word in words:
            word = word.lower()

            if dict1.has_key(word):
                dict1[word] += 1
            else:
                dict1[word] = 0

    class Object:
        pass

    final = []
    for k, v in dict1.items():
        me = Object()
        me.word = k
        me.count = v
        final.append(me)

    return json.dumps([me.__dict__ for me in final])


def main(seconds):
    api = auth()
    stream = create_stream (api)

    stream.sample(languages=['en'], async=True)
    time.sleep(int(seconds))
    stream.disconnect()

    json_text = get_json()

    print(json_text)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Please specify the duration of the data stream fetch")
