#!/usr/bin/env python

import sys
import json
import os

sys.path.insert(0, 'src/data')
sys.path.insert(0, 'src/analysis')
sys.path.insert(0, 'test')

from create_data import fetch_tweets, missingness
from compile_tweet_ids import download_tweet_ids
from fetch_captions import caption_data
from fetch_youtube_data import youtube_data
from twitter_data import make_twitter_data
from youtube_comments import comment_data
# import eda
import generate_data
# import kcore

def main(targets):
    if 'data' in targets:
        with open('config/data-params.json') as fh:
            data_cfg = json.load(fh)

        download_tweet_ids(**data_cfg["download_params"])
        fetch_tweets(**data_cfg["hydrate_params"])
        missingness(**data_cfg["missingness_params"])
        
        youtube_data(data_cfg["dataset_params"]["video_ids_fn"])
        print("collected YT metadata")
        caption_data(data_cfg["dataset_params"]["video_ids_fn"])
        print("fetched subtitles")
        make_twitter_data(data_cfg["dataset_params"]["tweet_jsonlines_fn"])
        print("made twitter metadata")
#         comment_data(data_cfg["dataset_params"]["video_ids_fn"])
        
    if 'analysis' in targets:
        with open('config/analysis-params.json') as fh:
            analysis_cfg = json.load(fh)
            
#         eda.url_proportion(**analysis_cfg["url_prop_params"])
#         eda.urls(**analysis_cfg["urls_params"])
#         eda.misinformation_proportion(**analysis_cfg["misinformation_url_prop_params"])
#         kcore.rt_ids(**analysis_cfg["kcores_rt_params"])
#         kcore.create_kcore(**analysis_cfg["kcores_graph_params"])

    if 'model' in targets:
        print("Coming soon!")
        
    if 'test' in targets:
        with open('config/test-params.json') as fh:
            test_cfg = json.load(fh)
        generate_data.create_test_data(test_cfg["test_data_params"]['num_tweets'])
    
    
if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)
