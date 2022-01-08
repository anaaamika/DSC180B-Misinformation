from twarc.client2 import Twarc2
from twarckeys import consumer_key, consumer_secret, access_token, access_token_secret
from dask import dataframe as df1
import jsonlines

t = Twarc2(consumer_key, consumer_secret, access_token, access_token_secret)
subset_size = 200

def fetch_tweets(subset_size, tweets_ids_fn, tweets_fn):
    tweets = df1.read_csv(tweets_ids_fn, sep='\t', dtype={'tweet_id': 'object'})

    subset = tweets.sample(frac=0.1)
    tweet_ids = subset['tweet_id']

    hydrated_tweets = t.tweet_lookup(tweet_ids)

    tweet_cnt = 0
    for batch in hydrated_tweets:
        if tweet_cnt < subset_size:
            for tweet in batch['data']:
                # add filters for healthcare terms and youtube links 
                if tweet_cnt < subset_size:
                    tweet_cnt += 1
                    with jsonlines.open(tweets_fn, 'a') as writer:
                        writer.write(tweet)
                else:
                    break
        else:
            break
    return

def check_link(tweet):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.46'}
    try:
        if 'urls' in tweet['entities'].keys():
            url = tweet['entities']['url']
            response = requests.get(url, headers=headers)
            if str(response.url).contains("youtube.com"):
                return True
    except KeyError:
        pass
    return False

