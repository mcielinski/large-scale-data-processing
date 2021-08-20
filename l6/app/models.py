from pyspark.ml.evaluation import RegressionEvaluator, \
    MulticlassClassificationEvaluator
from pyspark.ml.feature import StringIndexer, SQLTransformer, VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.ml.classification import LogisticRegression, \
    DecisionTreeClassifier, RandomForestClassifier  # noqa
from pyspark.ml import Pipeline


# ---- db_table_cols ----
# 'post_id'
# 'url'
# 'author_name'
# 'subreddit_name'
# 'post_title'
# 'post_text'
# 'post_text_embedding'
# 'post_length'
# 'num_votes'
# 'is_nsfw'
# 'num_comments'
# 'num_shares'
# 'post_timestamp'
# 'exec_time'


def linear_regression(train_ds, test_ds, save=False):
    # stage 1: transform the column 'subreddit_name' to numeric
    stage_1 = StringIndexer(
        inputCol='subreddit_name',
        outputCol='subreddit_name_numeric'
    )
    # stage 2: transform the column 'is_nsfw' to numeric
    stage_2 = StringIndexer(
        inputCol='is_nsfw',
        outputCol='is_nsfw_numeric'
    )
    # stage 3: create a vector of all the features required to train model
    stage_3 = VectorAssembler(
        inputCols=['subreddit_name_numeric', 'num_votes', 'is_nsfw_numeric',
                   'num_comments', 'num_shares', 'post_text_embedding_vector'],
        outputCol='features'
    )
    # stage 4: LinearRegression model
    stage_4 = LinearRegression(
        featuresCol='features',
        labelCol='post_length'
    )

    # setup the pipeline
    # regression_pipeline = Pipeline(stages=[stage_1, stage_2, stage_3, stage_4])
    regression_pipeline = Pipeline(stages=[stage_1, stage_2, stage_3, stage_4])

    # fit the pipeline to the train data and get predictions
    model = regression_pipeline.fit(train_ds)

    if save:
        model.save('models/linear_regression')
    
    predictions = model.transform(test_ds)

    # setup evaluator and evaluate predictions
    evaluator = RegressionEvaluator(
        predictionCol='prediction',
        labelCol='post_length',
        metricName='rmse'
    )
    rmse = evaluator.evaluate(predictions)

    return rmse


def binary_classification(train_ds, test_ds, classifier=LogisticRegression, save=False):
    # stage 1: transform the column 'subreddit_name' to numeric
    stage_1 = StringIndexer(
        inputCol='subreddit_name',
        outputCol='subreddit_name_numeric'
    )
    # stage 2: transform the column 'is_nsfw' to numeric
    stage_2 = StringIndexer(
        inputCol='is_nsfw',
        outputCol='is_nsfw_numeric'
    )
    # stage 3: create a vector of all the features required to train model
    stage_3 = VectorAssembler(
        inputCols=['subreddit_name_numeric', 'post_length', 'num_votes',
                   'num_comments', 'num_shares', 'post_text_embedding_vector'],
        outputCol='features'
    )
    # stage 4: classifier model
    stage_4 = classifier(
        featuresCol='features',
        labelCol='is_nsfw_numeric'
    )

    # setup the pipeline
    classifier_pipeline = Pipeline(stages=[stage_1, stage_2, stage_3, stage_4])

    # fit the pipeline to the train data and get predictions
    model = classifier_pipeline.fit(train_ds)

    if save:
        model.save('models/binary_classification')

    predictions = model.transform(test_ds)

    # setup evaluator and evaluate predictions
    evaluator = MulticlassClassificationEvaluator(
        predictionCol='prediction',
        labelCol='is_nsfw_numeric',
        metricName='f1'
    )
    f1 = evaluator.evaluate(predictions)

    return f1


def multiclass_classification(train_ds, test_ds, classifier=LogisticRegression, save=False):
    # stage 1: transform the column 'subreddit_name' to numeric
    stage_1 = StringIndexer(
        inputCol='subreddit_name',
        outputCol='subreddit_name_numeric'
    )
    # stage 2: transform the column 'is_nsfw' to numeric
    stage_2 = StringIndexer(
        inputCol='is_nsfw',
        outputCol='is_nsfw_numeric'
    )
    # stage 3: create a vector of all the features required to train model
    stage_3 = VectorAssembler(
        inputCols=['is_nsfw_numeric', 'post_length', 'num_votes',
                   'num_comments', 'num_shares', 'post_text_embedding_vector'],
        outputCol='features'
    )
    # stage 4: classifier model
    stage_4 = classifier(
        featuresCol='features',
        labelCol='subreddit_name_numeric'
    )

    # setup the pipeline
    classifier_pipeline = Pipeline(stages=[stage_1, stage_2, stage_3, stage_4])

    # fit the pipeline to the train data and get predictions
    model = classifier_pipeline.fit(train_ds)

    if save:
        model.save('models/multiclass_classification')

    predictions = model.transform(test_ds)

    # setup evaluator and evaluate predictions
    evaluator = MulticlassClassificationEvaluator(
        predictionCol='prediction',
        labelCol='subreddit_name_numeric',
        metricName='f1'
    )
    f1 = evaluator.evaluate(predictions)

    return f1
