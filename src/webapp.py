

# %%
import os
import csv
import ast
import pandas as pd
from flask import Flask, render_template, request, jsonify, url_for
import logging
from utils import get_data, get_random_tweet
from dotenv import load_dotenv

load_dotenv() 

logging.basicConfig(level=logging.INFO)


app = Flask(__name__, static_url_path='/static')


# home page
@app.route('/')
def index():
    """Renders the index page with a list of topics."""
    topics = list(topic_data.keys())
    return render_template('index.html', topics=topics)


# returns a JSON object containing all topics name and number
@app.route('/get_topics', methods=['GET'])
def get_topics():
    """Returns a JSON object containing all topics."""
    df_topic_copy = df_topic.copy()
    df_topic_copy.set_index('Topic', inplace=True)
    return jsonify(df_topic_copy['Name'].to_dict())



@app.route('/get_topic_data', methods=['GET'])
def get_topic_data():
    """Returns a JSON object containing data for a specific topic."""
    topic = request.args.get('topic')
    return jsonify(topic_data.get(int(topic)))

@app.route('/get_tweet', methods=['GET'])
def get_tweet():
    topic = request.args.get('topic')
    if topic is None:
        return jsonify({'error': 'The "topic" parameter is required.'}), 400
    return jsonify(get_random_tweet(df_tweets, topic))

@app.route('/label_tweet', methods=['POST'])
def label_tweet():
    """Updates the status of a tweet to 'reviewed' and appends the tweet's ID and label to a CSV file."""
    tweet_id = request.json.get('tweet')
    label = request.json.get('label')
    df_tweets.loc[tweet_id, 'reviewed'] = True

    with open(human_labeled, 'a') as f:
        writer = csv.writer(f)
        writer.writerow([tweet_id, label])

    logging.info('Tweet labeled: %s, %s', tweet_id, label)
    return jsonify({'status': 'success'})

# html page with a table containing a portion of the DataFrame
@app.route('/get_df', methods=['GET'])
def get_dataframe():
    """Returns an HTML table containing a portion of the DataFrame."""
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=100, type=int)
    columns = request.args.get('columns')
    topic = request.args.get('topic')


    start = (page - 1) * per_page
    end = start + per_page

    if columns is not None:
        columns = columns.split(',')
        df_subset = df_tweets[columns]
    else:
        df_subset = df_tweets

    if topic is not None and topic != '':
        df_subset = df_subset[df_subset['topic'] == int(topic)]

    topics = df_tweets['topic'].unique().tolist()  # Get the unique topics

    table = df_subset[start:end].to_html(classes='my-dataframe')
    return render_template('dataframe.html', table=table, page=page, topics=topics)  


if __name__ == '__main__':

    path = os.getenv('DATA_FOLDER')
    print(path)
    human_labeled = os.path.join(path, 'human_labeled.csv')
    topic_data, df_topic = get_data(path)

    df_tweets = pd.read_pickle(os.path.join(path, 'tweets_cop22_labeled.pkl'))
    df_tweets['reviewed'] = False
    
    app.run(debug=True)