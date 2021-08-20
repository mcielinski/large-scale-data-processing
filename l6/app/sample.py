"""Sample pySpark app."""

import json

import pyspark.sql.functions as psf
from pyspark.sql.functions import udf
from pyspark import SparkContext, SparkConf
from pyspark.ml.linalg import Vectors, VectorUDT
from pyspark.sql import SparkSession
from pyspark.sql.types import FloatType
from pyspark.ml.classification import LogisticRegression, \
    DecisionTreeClassifier, RandomForestClassifier

from models import linear_regression, binary_classification, \
    multiclass_classification


conf = SparkConf().setAppName('appName').setMaster('local')\
    .set('spark.jars.packages',
         'org.mongodb.spark:mongo-spark-connector_2.11:2.4.1')

sc = SparkContext(conf=conf)
sc.setLogLevel('ERROR')  # ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN

# ________________________________________________________________________
# data = range(1000)
# dist_data = sc.parallelize(data)

# large_data = dist_data.flatMap(lambda a: range(1000))


# def add(x, y):
#     """Add operation for pySpark."""
#     return x + y


# print(large_data.reduce(add))
# ________________________________________________________________________

credentials_file = open('mongodb_credentials.json')
mongodb_credentials = json.load(credentials_file)

db_user = mongodb_credentials['DB_USER']
db_password = mongodb_credentials['DB_PASSWORD']
db_name = mongodb_credentials['DB_NAME']
db_collection = mongodb_credentials['DB_COLLECTION']

input_uri = 'mongodb://' + db_user + ':' + db_password + '@mongodb:27017'

# Spark mongoDB Connector
#   (https://docs.mongodb.com/spark-connector/master/python-api)
spark_sess = SparkSession \
    .builder \
    .appName("myApp") \
    .config("spark.mongodb.input.uri", input_uri) \
    .config("spark.mongodb.input.database", db_name) \
    .config("spark.mongodb.input.collection", db_collection) \
    .getOrCreate()

# spark_sess = SparkSession.builder \
#     .appName("myApp") \
#     .master('local') \
#     .config("spark.mongodb.input.uri", input_uri) \
#     .config("spark.mongodb.input.database", db_name) \
#     .config("spark.mongodb.input.collection", db_collection) \
#     .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:3.0.0,ml.combust.mleap:mleap-spark_2.12:0.16.0') \
#     .getOrCreate()

# Read from MongoDB
df = spark_sess.read.format("mongo").load()

df.printSchema()
num_row = df.count()
print("Number of instances %g" % num_row)

spark_sess.udf.register(
    'udf_vec', lambda v: Vectors.dense(v), VectorUDT())


# df = df.withColumn("post_text_embedding",  psf.flatten(df.post_text_embedding))
# df = df.withColumn("post_text_embedding", functions.slice("post_text_embedding", start=1, length=50))
udf_vec = udf(lambda l: Vectors.dense(l), VectorUDT())

cols = ["is_nsfw"]
for col in cols:
    df = df.withColumn(
        col, 
        psf.when(
            psf.col(col) == 'N',
            'False'
        ).when(
            psf.col(col) == 'Y',
            'True'
        ).when(
            psf.col(col).cast('string') == 'true',
            'True'
        ).when(
            psf.col(col).cast('string') == 'false',
            'False'
        ).otherwise(psf.col(col).cast('string'))
    )

df = df.select(
    df["post_id"], 
    df["subreddit_name"], 
    df["is_nsfw"], 
    df["num_votes"], 
    df["num_comments"], 
    df["num_shares"], 
    df["post_length"], 
    df["is_nsfw"], # double(df["is_nsfw"]).alias("is_nsfw_numeric"), 
    udf_vec(df["post_text_embedding"]).alias("post_text_embedding_vector")
)

train_ds, test_ds = df.randomSplit([0.75, 0.25], seed=1234)


def get_class_balance(dataframe):
    count = dataframe.groupBy('subreddit_name').agg(psf.countDistinct('post_id'))
    posts_sum = count.select(psf.sum('count(DISTINCT post_id)')).collect()[0][0]

    udf_func = psf.udf(
        lambda col: round(col / posts_sum, 4) * 100,
        FloatType()
    )
    count = count.withColumn(
        'percentage',
        udf_func('count(DISTINCT post_id)')
    )

    return count.withColumnRenamed('count(DISTINCT post_id)', 'conut')


train_ds_balance = get_class_balance(train_ds)
print('\n' * 2)
print('______________ Train set ______________')
print(train_ds_balance.show())
print('_______________________________________')

test_ds_balance = get_class_balance(test_ds)
print('\n' * 2)
print('______________ Test set _______________')
print(test_ds_balance.show())
print('_______________________________________')


print('\n' * 2)
print('__________ Linear regression __________')
rmse = linear_regression(train_ds, test_ds, save=True)
print(f'RMSE: {rmse}')
print('_______________________________________')

print('________ Binary classification ________')
f1 = binary_classification(train_ds, test_ds, classifier=LogisticRegression, save=True)
print(f'LogRegr F1: {f1}')
f1 = binary_classification(train_ds, test_ds, classifier=DecisionTreeClassifier, save=False)
print(f'DecTree F1: {f1}')
f1 = binary_classification(train_ds, test_ds, classifier=RandomForestClassifier, save=False)
print(f'RandFor F1: {f1}')
print('_______________________________________')

print('______ Multi-class classification _____')
f1 = multiclass_classification(
    train_ds, test_ds, classifier=LogisticRegression, save=True)
print(f'LogRegr F1: {f1}')
f1 = multiclass_classification(
    train_ds, test_ds, classifier=DecisionTreeClassifier, save=False)
print(f'DecTree F1: {f1}')
f1 = multiclass_classification(
    train_ds, test_ds, classifier=RandomForestClassifier, save=False)
print(f'RandFor F1: {f1}')
print('_______________________________________')
print('\n' * 2)

#       ___________ Train set ___________
#       +--------------+-----+----------+
#       |subreddit_name|conut|percentage|
#       +--------------+-----+----------+
#       |     AskReddit|10789|     76.52|
#       |          food|  574|      4.07|
#       |          pics| 1194|      8.47|
#       |     worldnews|  492|      3.49|
#       |         funny| 1051|      7.45|
#       +--------------+-----+----------+
#       |           all|14100|       100|
#       +--------------+-----+----------+

#       ___________ Test set ____________
#       +--------------+-----+----------+
#       |subreddit_name|conut|percentage|
#       +--------------+-----+----------+
#       |     AskReddit| 3669|      78.2|
#       |          food|  184|      3.92|
#       |          pics|  379|      8.08|
#       |     worldnews|  149|      3.18|
#       |         funny|  311|      6.63|
#       +--------------+-----+----------+
#       |           all| 4692|       100|
#       +--------------+-----+----------+

