# from app import app

import numpy as np
from flask import Flask, request
from pyspark import SparkContext
from pyspark.ml import PipelineModel
from pyspark.ml.feature import StringIndexer, StringIndexerModel
from pyspark.ml.linalg import Vectors, VectorUDT
from pyspark.sql import SparkSession, SQLContext
from pyspark.sql.functions import udf
from pymagnitude import Magnitude


app = Flask(__name__)

sc = SparkContext('local')
sql_cont = SQLContext(sc)

udf_vec = udf(lambda l: Vectors.dense(l), VectorUDT())

lr_model = PipelineModel.load('models/linear_regression')
bc_model = PipelineModel.load('models/binary_classification')
mc_model = PipelineModel.load('models/multiclass_classification')

vectors = Magnitude('glove.6B.50d.magnitude')


def vectorize(text_to_embedded):
    embeddings = vectors.query(text_to_embedded.split())
    embedding = np.mean(embeddings, axis=0)
    embedding = embedding.tolist()

    return embedding


@app.route('/lr_model')
def lr_func():
    # inputCols=['subreddit_name_numeric', 'num_votes', 'is_nsfw_numeric',
    #            'num_comments', 'num_shares', 'post_text_embedding_vector']
    # labelCol='post_length'
    # sample_text = 'What book series did you love as a kid?'
    # embedding = vectorize(sample_text)
    
    subreddit_name = str(request.args.get('subreddit_name'))
    num_votes = int(request.args.get('num_votes'))
    is_nsfw = str(request.args.get('is_nsfw'))
    num_comments = int(request.args.get('num_comments'))
    num_shares = int(request.args.get('num_shares'))
    post_text_embedding = request.args.get('post_text_embedding')
    embedding = vectorize(post_text_embedding)

    df = sql_cont.createDataFrame(
        [
            (
                subreddit_name, 
                num_votes, 
                is_nsfw, 
                num_comments, 
                num_shares, 
                embedding
            )
        ],
        [
            'subreddit_name', 'num_votes', 'is_nsfw', 
            'num_comments', 'num_shares', 'post_text_embedding'
        ]
    )

    df = df.select(
        df["subreddit_name"], 
        df["num_votes"], 
        df["is_nsfw"], 
        df["num_comments"], 
        df["num_shares"], 
        udf_vec(df["post_text_embedding"]).alias("post_text_embedding_vector")
    )

    prediction = lr_model.transform(df)
    result = str(prediction.collect()[0]['prediction'])

    return result


@app.route('/bc_model')
def bc_func():
    # inputCols=['subreddit_name_numeric', 'post_length', 'num_votes',
    #            'num_comments', 'num_shares', 'post_text_embedding_vector']
    # labelCol='is_nsfw_numeric'
    # sample_text = 'What book series did you love as a kid?'
    # embedding = vectorize(sample_text)

    subreddit_name = str(request.args.get('subreddit_name'))
    post_length = int(request.args.get('post_length'))
    num_votes = int(request.args.get('num_votes'))
    num_comments = int(request.args.get('num_comments'))
    num_shares = int(request.args.get('num_shares'))
    post_text_embedding = request.args.get('post_text_embedding')
    embedding = vectorize(post_text_embedding)

    df = sql_cont.createDataFrame(
        [
            (
                subreddit_name, 
                post_length, 
                num_votes, 
                num_comments, 
                num_shares, 
                embedding
            )
        ],
        [
            'subreddit_name', 'post_length', 'num_votes', 
            'num_comments', 'num_shares', 'post_text_embedding'
        ]
    )

    df = df.select(
        df["subreddit_name"], 
        df["post_length"], 
        df["num_votes"], 
        df["num_comments"], 
        df["num_shares"], 
        udf_vec(df["post_text_embedding"]).alias("post_text_embedding_vector")
    )

    prediction = bc_model.transform(df)
    result = int(prediction.collect()[0]['prediction'])

    # print('\n\n')
    for x in bc_model.stages:
        if isinstance(x, StringIndexerModel) and x._java_obj.getOutputCol() == 'is_nsfw_numeric':
            # print(f'{x.labels}')
            labels = x.labels
    # print('\n\n')

    result = labels[result]

    return result


@app.route('/mc_model')
def mc_func():
    # inputCols=['is_nsfw_numeric', 'post_length', 'num_votes',
    #            'num_comments', 'num_shares', 'post_text_embedding_vector']
    # labelCol='subreddit_name_numeric'
    # sample_text = 'What book series did you love as a kid?'
    # embedding = vectorize(sample_text)

    is_nsfw = str(request.args.get('is_nsfw'))
    post_length = int(request.args.get('post_length'))
    num_votes = int(request.args.get('num_votes'))
    num_comments = int(request.args.get('num_comments'))
    num_shares = int(request.args.get('num_shares'))
    post_text_embedding = request.args.get('post_text_embedding')
    embedding = vectorize(post_text_embedding)

    df = sql_cont.createDataFrame(
        [
            (
                is_nsfw, 
                post_length, 
                num_votes, 
                num_comments, 
                num_shares, 
                embedding
            )
        ],
        [
            'is_nsfw', 'post_length', 'num_votes', 
            'num_comments', 'num_shares', 'post_text_embedding'
        ]
    )

    df = df.select(
        df["is_nsfw"], 
        df["post_length"], 
        df["num_votes"], 
        df["num_comments"], 
        df["num_shares"], 
        udf_vec(df["post_text_embedding"]).alias("post_text_embedding_vector")
    )

    prediction = mc_model.transform(df)
    result = int(prediction.collect()[0]['prediction'])

    # print('\n\n')
    for x in mc_model.stages:
        if isinstance(x, StringIndexerModel) and x._java_obj.getOutputCol() == 'subreddit_name_numeric':
            # print(f'{x.labels}')
            labels = x.labels
    # print('\n\n')

    result = labels[result]

    return result


if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8080)
      