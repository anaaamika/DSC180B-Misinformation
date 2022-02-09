from random import random 
import json
def create_test_data(num_tweets, tweets_fn="data/tweets.jsonl", outfile="test/testdata/test_tweets.jsonl" ):
    lines = 0
    with open(tweets_fn, "r") as full_data:
        with open(outfile, "w") as test_data:
            for line in full_data:
                if lines < int(num_tweets):
                    if random() >= 0.8:
                        test_data.write(line)
                        print(json.loads(line).keys())
                        lines += 1
                else:
                    break
        
