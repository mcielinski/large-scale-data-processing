from app import app

import numpy as np
from flask import request
from pymagnitude import Magnitude


vectors = Magnitude('glove.6B.50d.magnitude')

@app.route('/')
def home():
    text_to_embedded = request.args.get('text')
    embeddings = vectors.query(text_to_embedded.split())
    embedding = np.mean(embeddings, axis=0)
    embedding = str(embedding)

    return embedding


# was
# @app.route('/')
# def home():
#    return "hello world!"