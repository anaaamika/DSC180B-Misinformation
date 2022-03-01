import json
import pandas as pd

def make_twitter_data(tweet_jsonlines_fn, outfile="data/youtube_tweets.csv"):
    with open(tweet_jsonlines_fn) as f:
        lines = f.read().splitlines()
        
    df_inter = pd.DataFrame(lines)
    df_inter.columns = ['json_element']
    
    df_inter['json_element'].apply(json.loads)
    
    df_final = pd.json_normalize(df_inter['json_element'].apply(json.loads))
    df_final.to_csv(outfile, index = False)
    
    return 