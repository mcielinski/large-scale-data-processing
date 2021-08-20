from pymongo import MongoClient

# import celery_base as cb
from celery_base import app
import data_model  # noqa
from docker_logs import get_logger


logging = get_logger('database_worker')
logging.propagate = False


@app.task(bind=True, name='database_insert')
# serializer='pickle', queue='database_queue')
def database_insert(self, submission_data):
    logging.info(f'Inserting to database post: {submission_data.post_id} start')
    client = MongoClient('mongodb://user:password@mongodb:27017/')
    db = client.reddit_db
    collection = db['reddit_posts']

    post_dict = submission_data.to_dict()
    db_record = collection.insert_one(post_dict)

    logging.info(
        f'Inserting to database post: {submission_data.post_id} \
        completed - record id: {db_record.inserted_id}')
