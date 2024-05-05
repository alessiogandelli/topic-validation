import os
import csv
import ast
import pandas as pd
from flask import Flask, render_template, request, jsonify, url_for
import logging

def create_labeled_file(file_path):
    """Creates a CSV file to store human-labeled data."""
   

    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['tweet_id', 'label'])

def get_data(path):
    """Reads data from a CSV file and returns a dictionary and a DataFrame."""
    df = pd.read_csv(os.path.join(path, 'topics_cop22.csv'))
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.rename(columns={'Representative_Docs': 'docs'})
    topic_data = {row['Topic']: row.drop('Topic').to_dict() for _, row in df.iterrows()}

    for topic in topic_data:
        topic_data[topic]['docs'] = ast.literal_eval(topic_data[topic]['docs'])

    return topic_data, df

def get_random_tweet(df_tweets, topic):
    if topic is None:
        return {'id': None, 'text': None}
    try: 
        tweets = df_tweets[df_tweets['topic'] == int(topic)]
        tweets = tweets[~tweets['reviewed']]
        tweet = tweets.sample(1)
        return {'id' : tweet.index.tolist()[0], 'text': tweet['text'].values[0]}
    except ValueError:
        return {'id': None, 'text': None}





