import pandas as pd
import re
import twarckeys
import gzip
import datetime
import wget
import shutil
import os

def download_tweet_ids(start_date, end_date, tweet_ids_fn):
    while start_date != end_date:
        str_date = start_date.strftime("%Y-%m-%d")
        dataset_url = f'https://github.com/thepanacealab/covid19_twitter/raw/master/dailies/{str_date}/{str_date}-dataset.tsv.gz'

        wget.download(dataset_url, out='dataset.tsv.gz')
        with gzip.open('dataset.tsv.gz', 'rb') as f_in:
            with open(tweet_ids_fn, 'ab') as f_out:
                shutil.copyfileobj(f_in, f_out)

        start_date += datetime.timedelta(days=1)

        os.unlink("dataset.tsv.gz")