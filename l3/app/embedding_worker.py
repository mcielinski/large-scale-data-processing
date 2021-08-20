from celery import signature
import numpy as np
from pymagnitude import Magnitude

from celery_base import app
import data_model  # noqa
# from database_worker import database_insert
from docker_logs import get_logger


logging = get_logger('embedding_worker')
logging.propagate = False


@app.task(bind=True, name='add_text_embedding')
# serializer='pickle', queue='embedding_queue')
def add_text_embedding(self, submission_data):
    logging.info(f'Embedding post: {submission_data.post_id} start')
    # vectors = Magnitude('word2vec/light/GoogleNews-vectors-negative300')
    vectors = Magnitude('magnitude/glove.6B.50d.magnitude')

    to_embedded = submission_data.post_title + ' ' + submission_data.post_text
    embeddings = vectors.query(to_embedded.split())
    embedding = np.mean(embeddings, axis=0)

    submission_data.post_text_embedding = embedding.tolist()
    # logging.info(f'Embedding: {submission_data.post_text_embedding}')
    logging.info(f'Embedding post: {submission_data.post_id} completed')

    # database_insert.delay(post)
    signature('database_insert', args=(submission_data,)).apply_async()

    return submission_data
