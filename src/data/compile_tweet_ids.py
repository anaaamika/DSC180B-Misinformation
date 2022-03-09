import pandas as pd
import re
import twarckeys
import gzip
import datetime 
from datetime import timedelta as td
from datetime import datetime as dt
import wget
import shutil
import os

def download_tweet_ids(start_date, end_date, tweets_ids_fn):
    print("starting tweet id download")
    if os.path.exists(tweets_ids_fn) and os.path.getsize(tweets_ids_fn) > 0:
        return
    if type(start_date) == str:
        start_date = dt.strptime(start_date, '%Y, %m, %d')
    if type(end_date) == str:
        end_date = dt.strptime(end_date, '%Y, %m, %d')
    while start_date != end_date:
        str_date = start_date.strftime("%Y-%m-%d")
        dataset_url = f'https://github.com/thepanacealab/covid19_twitter/raw/master/dailies/{str_date}/{str_date}-dataset.tsv.gz'

        wget.download(dataset_url, out='data/dataset.tsv.gz')
        with gzip.open('data/dataset.tsv.gz', 'rb') as f_in:
            with open(tweets_ids_fn, 'ab') as f_out:
                shutil.copyfileobj(f_in, f_out)

        start_date += td(days=1)

        os.unlink("data/dataset.tsv.gz")