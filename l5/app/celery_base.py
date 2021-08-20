import json

from celery import Celery
import praw

from database import InfluxDB
from docker_logs import get_logger


logging = get_logger("task")
logging.propagate = False


SUBREDDITS = ['funny', 'AskReddit', 'worldnews', 'food', 'pics']
FETCHING_INTERVAL = 60.0  # 60.0
FETCHING_LIMIT = 10


app = Celery()
db = InfluxDB(database_name='my_database', table_name='submissions')   # (database_name='subreddit_funny_database', table_name='submissions_2')

credentials_file = open('reddit_credentials.json')
reddit_credentials = json.load(credentials_file)

reddit = praw.Reddit(client_id=reddit_credentials['CLIENT_ID'],
                     client_secret=reddit_credentials['CLIENT_SECRET'],
                     user_agent=reddit_credentials['USER_AGENT'])


app.conf.task_serializer = 'pickle'
app.conf.result_serializer = 'pickle'
app.conf.accept_content = ['pickle']

app.conf.task_routes = ([
    ('get_submissions', {'queue': 'scraping_queue'}),
    ('get_submission_data', {'queue': 'scraping_queue'}),
    ('add_text_embedding', {'queue': 'embedding_queue'}),
    ('database_insert', {'queue': 'database_queue'}),
],)
