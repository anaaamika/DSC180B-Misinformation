#!/usr/bin/env python

import sys
import json
import os

sys.path.insert(0, 'src/data')
sys.path.insert(0, 'src/analysis')
sys.path.insert(0, 'src/model')
sys.path.insert(0, 'test')

from create_data import fetch_tweets, missingness
from compile_tweet_ids import download_tweet_ids
from fetch_captions import caption_data
from fetch_youtube_data import youtube_data
from twitter_data import make_twitter_data
from youtube_comments import comment_data
import eda
import topic_modeling
import generate_data
import misinformation_model

def main(targets):
    if 'data' in targets:
        with open('config/data-params.json') as fh:
            data_cfg = json.load(fh)

        download_tweet_ids(**data_cfg["download_params"])
        fetch_tweets(**data_cfg["hydrate_params"])
        missingness(**data_cfg["missingness_params"])
        
        youtube_data(data_cfg["dataset_params"]["video_ids_fn"])
        caption_data(data_cfg["dataset_params"]["video_ids_fn"])
        make_twitter_data(data_cfg["dataset_params"]["tweet_jsonlines_fn"])
        
#         comment_data(data_cfg["dataset_params"]["video_ids_fn"])
        
    if 'analysis' in targets:
        with open('config/analysis-params.json') as fh:
            analysis_cfg = json.load(fh)
            
        eda.caption_analysis(**analysis_cfg["eda_params"])
        eda.topic_model(**analysis_cfg["topic_model_params"])


    if 'model' in targets:
        with open('config/model-params.json') as fh:
            model_cfg = json.load(fh)
        misinformation_model.model_selection(**model_cfg)
        
    if 'test' in targets:
        with open('config/test-params.json') as fh:
            test_cfg = json.load(fh)
        generate_data.create_test_data(test_cfg["test_data_params"]['num_tweets'])
    
    
if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)
