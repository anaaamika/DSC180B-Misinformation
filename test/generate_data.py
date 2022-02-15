from random import random 
import json
import requests
import pandas as pd
import csv
from urllib import parse

def create_test_data(num_tweets, tweets_fn="data/tweets.jsonl", outfolder="test" ):
    lines = 0
    with open(tweets_fn, "r") as full_data:
        with open(outfolder + "/testdata/test_tweets.jsonl", "w") as test_data:
            for line in full_data:
                if lines < int(num_tweets):
                    if random() >= 0.8:
                        test_data.write(line)
                        lines += 1
                        tweet = json.loads(line)
                        
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

                                    if response is not None:
                                        if any(x in str(response.url) for x in ["youtube", "youtu.be"]):
                                            video_id = get_video_id(response.url)
                                            if video_id is not None:
                                                youtube_links += 1
                                                f = open(outfolder + "video_ids.csv", "a")
                                                writer = csv.writer(f)
                                                writer.writerow(video_id)
                                                f.close()
                                                print(video_id)
                        except KeyError:
                            pass
                else:
                    break
        
