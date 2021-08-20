import celery_base as cb
from celery_base import app
from docker_logs import get_logger
from scraper_worker import get_submissions


logging = get_logger('scheduler_worker')
logging.propagate = False


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    logging.info('New periodic task')
    sender.add_periodic_task(cb.FETCHING_INTERVAL,
                             get_submissions.s(subreddit_names=cb.SUBREDDITS,
                                               limit=cb.FETCHING_LIMIT,
                                               interval=cb.FETCHING_INTERVAL))
