import pandas as pd

import json
import logging
import time

import requests
from newspaper import Article

def fetch_news_data(real_news_fn="src/data/politifact_real.csv", fake_news_fn="src/data/politifact_fake.csv", outfile="data/news_data.csv"):
    fake_df = pd.read_csv(fake_news_fn)
    real_df = pd.read_csv(real_news_fn)
    
    fake_df["article_text"] = fake_df["news_url"].apply(crawl_news_article)
    real_df["article_text"] = real_df["news_url"].apply(crawl_news_article)

    real_df["label"] = "real"
    fake_df["label"] = "fake"
    
    news_df = pd.concat([fake_df, real_df])
    
    pd.to_csv(outfile, index=False)
    
    
def crawl_link_article(url):
    result_json = None

    try:
        if 'http' not in url:
            if url[0] == '/':
                url = url[1:]
            try:
                article = Article('http://' + url)
                article.download()
                time.sleep(2)
                article.parse()
                flag = True
            except:
                flag = False
                pass
            if flag == False:
                try:
                    article = Article('https://' + url)
                    article.download()
                    time.sleep(2)
                    article.parse()
                    flag = True
                except:
                    flag = False
                    pass
            if flag == False:
                return None
        else:
            try:
                article = Article(url)
                article.download()
                time.sleep(2)
                article.parse()
            except:
                return None

        if not article.is_parsed:
            return None

        visible_text = article.text

    except:
        return None

    return visible_text

def get_epoch_time(time_obj):
    if time_obj:
        return time_obj.timestamp()

    return None

def get_web_archieve_results(search_url):
    try:
        archieve_url = "http://web.archive.org/cdx/search/cdx?url={}&output=json".format(search_url)

        response = requests.get(archieve_url)
        response_json = json.loads(response.content)

        response_json = response_json[1:]

        return response_json

    except:
        return None
    
def get_website_url_from_arhieve(url):
    """ Get the url from http://web.archive.org/ for the passed url if exists."""
    archieve_results = get_web_archieve_results(url)
    if archieve_results:
        modified_url = "https://web.archive.org/web/{}/{}".format(archieve_results[0][1], archieve_results[0][2])
        return modified_url
    else:
        return None
    
def crawl_news_article(url):
    news_article = crawl_link_article(url)

    # If the news article could not be fetched from original website, fetch from archieve if it exists.
    if news_article is None:
        archieve_url = get_website_url_from_arhieve(url)
        if archieve_url is not None:
            news_article = crawl_link_article(archieve_url)

    return news_article