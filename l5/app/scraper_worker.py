from celery import signature
import datetime
import time

import celery_base as cb
from celery_base import app
from docker_logs import get_logger
from data_model import DataModel
# from embedding_worker import add_text_embedding


logging = get_logger('scraper_worker')
logging.propagate = False


@app.task(bind=True, name='get_submission_data')
# serializer='pickle', queue='scraping_queue')
def get_submission_data(self, submission_id, subreddit_name):
    logging.info(
        f'Fetching data from submission: {submission_id} \
        (subreddit: {subreddit_name})')

    start_timer = time.time()
    submission = cb.reddit.submission(id=submission_id)
    exec_time = time.time() - start_timer

    submission_data = DataModel(post_id=submission_id,
                                url=submission.url,
                                author_name=submission.author.name,
                                subreddit=submission.subreddit.display_name,
                                post_title=submission.title,
                                post_text=submission.selftext,
                                post_text_embedding=None,
                                post_length=len(submission.title) +
                                len(submission.selftext),
                                num_votes=submission.score,
                                is_nsfw=submission.over_18,
                                num_comments=submission.num_comments,
                                num_shares=submission.num_crossposts,
                                post_timestamp=submission.created_utc,
                                exec_time=exec_time)
    
    submission_data_influx = {'post_id': submission_id, 
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

    logging.info(
        f'Fetching data from submission: {submission_id} \
        completed (subreddit: {subreddit_name})')
    cb.db.insert_data(submission_data=submission_data_influx)
    # submission_data = add_text_embedding.delay(submission_data)
    signature('add_text_embedding', args=(submission_data,)).apply_async()


@app.task(bind=True, name='get_submissions')
# serializer='pickle', queue='scraping_queue')
def get_submissions(self, subreddit_names=cb.SUBREDDITS,
                    limit=cb.FETCHING_LIMIT, interval=cb.FETCHING_INTERVAL):
    for subreddit_name in subreddit_names:
        logging.info(
            f'Fetching new submissions from subreddit: {subreddit_name}')
        subreddit = cb.reddit.subreddit(subreddit_name)
        submissions = subreddit.new(limit=limit)

        # now = datetime.datetime.now(datetime.timezone.utc)
        # prev_interval_end = now - datetime.timedelta(seconds=interval)
        prev_interval_end = datetime.datetime.now().timestamp() - interval

        submissions_to_fetch = [submission for submission in submissions
                                if submission.created_utc > prev_interval_end]

        counter = 0
        for submission in submissions_to_fetch:
            # get_submission_data.delay(submission.id)
            signature('get_submission_data', args=(
                submission.id, subreddit_name,)).apply_async()
            counter += 1

        logging.info(
            f'Fetching completed - {counter} \
            new submissions from subreddit: {subreddit_name}')
