import pandas as pd

import json
import time

import requests
from newspaper import Article

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.linear_model import PassiveAggressiveClassifier

def training_data():
    fake_df = pd.read_csv("politifact_fake.csv")
    real_df = pd.read_csv("politifact_real.csv")
    
    fake_df["article_text"] = fake_df["news_url"].apply(crawl_news_article)
    fake_df["label"] = "fake"
    
    real_df["article_text"] = real_df["news_url"].apply(crawl_news_article)
    real_df["label"] = "real"

    news_df = pd.concat([fake_df, real_df])
    model_data = news_df.apply(create_model_df, axis=1).dropna().reset_index(drop=True)
    
    return model_data
    
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
        top_image = article.top_image
        images = article.images
        keywords = article.keywords
        authors = article.authors
        canonical_link = article.canonical_link
        title = article.title
        meta_data = article.meta_data
        movies = article.movies
        publish_date = article.publish_date
        source = article.source_url
        summary = article.summary

        result_json = {'url': url, 'text': visible_text, 'images': list(images), 'top_img': top_image,
                       'keywords': keywords,
                       'authors': authors, 'canonical_link': canonical_link, 'title': title, 'meta_data': meta_data,
                       'movies': movies, 'publish_date': get_epoch_time(publish_date), 'source': source,
                       'summary': summary}
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

def create_model_df(row):
    row = row[["article_text", "title", "label"]]
    row["article_text"] = text_cleaning(row["article_text"])
    row["title"] = text_cleaning(row["title"])
    row["label"] = int(row["label"] == "real")
    return row

def model_selection(models_list):
    Data = model_data["article_text"]
    Target = model_data["label"]
    
    count_vectorizer = CountVectorizer()
    count_vectorizer.fit_transform(Data)
    freq_term_matrix = count_vectorizer.transform(Data)
    tfidf = TfidfTransformer(norm = "l2")
    tfidf.fit(freq_term_matrix)
    tf_idf_matrix = tfidf.fit_transform(freq_term_matrix)
    
    X_train, X_test, y_train, y_test = train_test_split(tf_idf_matrix, Target, test_size=0.2, random_state=0, stratify=Target)
    
    model_scores = {}
    models_list = models_list.split(",")
    
    for str_model in models_list:
        model = eval(str_model)
        model.fit(X_train, y_train)
        accuracy = model.score(X_test, y_test)
        
        model_scores[model] = accuracy
        
    best_model = min(model_scores, key=model_scores.get)
    model_name = type(best_model).__name__
    
    with open("results/"+model_name+"model.pk", 'wb') as pickle_file:
        pickle.dump(best_model, pickle_file)
    
    
    