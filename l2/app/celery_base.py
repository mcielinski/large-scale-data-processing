from celery import Celery
import praw
import datetime
import time
from database import InfluxDB
import json
from docker_logs import get_logger
logging = get_logger("task")
logging.propagate = False


SUBREDDIT = 'funny'
FETCHING_INTERVAL = 60.0
FETCHING_LIMIT = 20


app = Celery()
db = InfluxDB(database_name='subreddit_funny_database', table_name='submissions_2')

credentials_file = open('reddit_credentials.json')
reddit_credentials = json.load(credentials_file)

reddit = praw.Reddit(client_id=reddit_credentials['CLIENT_ID'],
                     client_secret=reddit_credentials['CLIENT_SECRET'],
                     user_agent=reddit_credentials['USER_AGENT'])
subreddit = reddit.subreddit(SUBREDDIT)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    logging.info(f"New periodic task")
    sender.add_periodic_task(FETCHING_INTERVAL,
                             get_submissions.s(subreddit_name=SUBREDDIT, 
                                               limit=FETCHING_LIMIT,))


@app.task(bind=True, name='task')  
def task(self, param):  
    logging.info(f"Celery task executed with param: {param}")
    return f"Result of task for param {param}"


@app.task(bind=True, name="get_submission_data")
def get_submission_data(self, submission_id):
    logging.info(f'Fetching data from submission: {submission_id}')

    start_timer = time.time()
    submission = reddit.submission(id=submission_id)
    exec_time = time.time() - start_timer

    submission_data = {'post_id': submission_id, 
                       'post_title': submission.title.replace("'", "''"), 
                       'post_title_length': len(submission.title), 
                       'post_author': submission.author.name, 
                       'post_score': submission.score, 
                       'post_url': submission.url, 
                       'num_ups': submission.ups, 
                       'num_downs': submission.downs, 
                       'num_shares': submission.num_crossposts, 
                       'num_comments': submission.num_comments, 
                       'post_timestamp': submission.created_utc, 
                       'exec_time': exec_time}

    logging.info(f'Fetching data from submission: {submission_id} completed')
    db.insert_data(submission_data=submission_data)


@app.task(bind=True, name='get_submissions')
def get_submissions(self, subreddit_name=SUBREDDIT, limit=FETCHING_LIMIT):
    logging.info(f'Fetching new submissions from subreddit: {subreddit_name}')
    submissions = subreddit.new(limit=limit)
    counter = 0

    latest_timestamp = db.get_latest_timestamp()
    if latest_timestamp is not None:
        submissions_to_fetch = [submission for submission in submissions 
                                           if submission.created_utc > latest_timestamp]
    else:
        submissions_to_fetch = submissions

    for submission in submissions_to_fetch:
        get_submission_data.delay(submission.id)
        counter += 1
    
    logging.info(f'Fetching completed - {counter} new submissions')