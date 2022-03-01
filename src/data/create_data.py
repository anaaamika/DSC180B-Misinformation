import sys

sys.path.insert(0, 'secrets')

from twarc.client2 import Twarc2
from twarckeys import consumer_key, consumer_secret, access_token, access_token_secret
from dask import dataframe as df1
import jsonlines
import requests
import pandas as pd
import csv
from urllib import parse
import numpy as np
from scipy import stats

t = Twarc2(consumer_key, consumer_secret, access_token, access_token_secret)


def fetch_tweets(subset_size, tweets_ids_fn, tweets_fn, video_ids_fn, outfolder="data"):
    tweets = df1.read_csv(tweets_ids_fn, sep='\t', dtype={'tweet_id': 'object'})
    tweet_cnt = 0
    total_urls = 0
    total_youtube_urls = 0
    youtube_tweets = 0

    sampled = []
    while total_youtube_urls < int(subset_size):

        try:
            subset = tweets.sample(frac=0.001)
            tweet_ids = subset[subset['tweet_id'] not in sampled]['tweet_id']

            sampled = sampled.extend(tweet_ids)

            hydrated_tweets = t.tweet_lookup(tweet_ids)

            for batch in hydrated_tweets:
                if total_youtube_urls < int(subset_size):
                    for tweet in batch['data']:
                        # add filters for healthcare terms and youtube links 
                        if health_filter(tweet, "src/data/health_corpus.txt") and (
                                total_youtube_urls < int(subset_size)):
                            tweet_cnt += 1
                            url_cnt, num_youtube_links = check_links(tweet, video_ids_fn)
                            total_urls += url_cnt
                            total_youtube_urls += num_youtube_links
                            youtube_tweets += 1

                            if num_youtube_links > 0:
                                with jsonlines.open(tweets_fn, 'a') as writer:
                                    writer.write(tweet)
                        else:
                            break
                else:
                    break
        except:
            pass
    with open(outfolder + "/outputs.txt", "a") as text_file:
        text_file.write('The number of public health-related tweets with urls was'+ str(tweet_cnt)+ '.\n')
        text_file.write('The number of urls was' + str(total_urls) + '.\n')
        text_file.write('The number of YouTube urls was' + str(total_youtube_urls) + '.\n')
        text_file.write('The number of tweets with YouTube urls was' + str(youtube_tweets) + '.\n')

    return


def check_links(tweet, video_ids_fn):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.46'}
    youtube_links = 0
    num_urls = 0
    try:
        if 'urls' in tweet['entities'].keys():
            url_list = [link['expanded_url'] for link in tweet['entities']['urls']]
            num_urls = len(url_list)
            for url in url_list:
                try:
                    response = requests.get(url, headers=headers, allow_redirects=True)
                except Exception as e:
                    print(e)
                    try:
                        response = requests.get(url, headers=headers, allow_redirects=True, verify=False)
                    except:
                        response = None
                        add_bad_url(url)

                if response is not None:
                    if any(x in str(response.url) for x in ["youtube", "youtu.be"]):
                        video_id = get_video_id(response.url)
                        if video_id is not None:
                            youtube_links += 1
                            f = open(video_ids_fn, "a")
                            writer = csv.writer(f)
                            writer.writerow(video_id)
                            f.close()
                            print(video_id)
    except KeyError:
        pass
    return num_urls, youtube_links


def add_bad_url(url):
    fn = open('data/bad_urls.csv', 'a')
    writer = csv.writer(fn)
    writer.writerow([url])
    fn.close()


def get_video_id(youtube_url):
    url_parsed = parse.urlparse(youtube_url)
    qsl = parse.parse_qs(url_parsed.query)
    if "v" in qsl.keys():
        video_id = qsl['v']
    elif "url" in qsl.keys():
        video_id = url_parsed.path.split('/')[-1]
    else:
        add_bad_url(youtube_url)
        return None
    return video_id


def health_filter(tweet, health_terms_fn):
    keywords = pd.read_csv(health_terms_fn, header=None).dropna(axis=1)
    keywords.columns = ['Term']
    keywords['Term'] = keywords['Term'].str.lower()
    try:
        if set(tweet['text'].lower().split()).intersection(set(keywords['Term'])):
            return True
    except KeyError:
        pass
    return False


def missingness(tweet_ids_fn, outfolder='data'):

    num_samples = 100
    missing = []
    tweets = df1.read_csv(tweet_ids_fn, sep='\t', dtype={'tweet_id': 'object'})
    for i in range(num_samples):
        subset = tweets.sample(frac=0.1)
        tweet_ids = subset['tweet_id']

        hydrated_tweets = t.tweet_lookup(tweet_ids)
        tweet_cnt = 0
        for batch in hydrated_tweets:
            tweet_cnt += len(batch['data'])
        missing_prop = tweet_cnt / len(tweet_ids)
        missing.append(missing_prop)

        missing_interval = stats.norm.interval(alpha=0.95, loc=np.mean(missing), scale=stats.sem(missing))

    with open("/outputs.txt", "a") as text_file:
        text_file.write('The 95% confidence interval for the proportion of missing tweets is' + str(missing_interval) + '.\n')
    return




