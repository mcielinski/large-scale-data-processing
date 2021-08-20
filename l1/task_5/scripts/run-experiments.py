"""Script for time measurement experiments on linear regression models."""
import argparse
import pickle
import time
import datetime
import os
from typing import List
from typing import Tuple
from typing import Type

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import lr


def get_args() -> argparse.Namespace:
    """Parses script arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--datasets-dir',
        required=True,
        help='Name of directory with generated datasets',
        type=str,
    )

    return parser.parse_args()


def read_dataset(datasets_dir):
    datasets = []

    for f in os.listdir(datasets_dir):
        file_name = datasets_dir + '/' + f
        with open(file_name, 'rb') as file:
            data = pickle.load(file)
            datasets.append(data)

    return sorted(datasets, key=lambda x: len(x[0]))


def run_experiments(
    models: List[Type[lr.base.LinearRegression]],
    datasets: List[Tuple[List[float], List[float]]],
) -> pd.DataFrame:
    main_df = pd.DataFrame({'data_size': [], 'model_name': [], 'time [s]': []})

    for dataset in datasets:
        X, y = dataset
        data_size = len(X)
        for model in models:
            start = time.time()
            for _ in range(10):
                model.fit(model, X, y)
            exec_time = time.time() - start

            df = pd.DataFrame([(int(data_size), model.__name__, exec_time)],
                              columns=['data_size', 'model_name', 'time [s]'])
            main_df = main_df.append(df)

    return main_df


def make_plot(results: pd.DataFrame) -> None:
    sns.set(rc={'figure.figsize': (12, 8)})

    _ = sns.barplot(data=results, x="model_name", hue="data_size",
                    y="time [s]",)

    plt.savefig('figs/fig_{}.png'.format(datetime.datetime.now())
                .replace(":", "-").replace(" ", "_"))
    plt.show()


def make_line_plot(results):
    fig, ax = plt.subplots(figsize=(12, 8))
    for key, grp in results.groupby('model_name'):
        #if key != 'LinearRegressionProcess':
        if True:
            ax = grp.plot(ax=ax, kind='line', x='data_size', y='time [s]',
                          label=key, style='.-')

    plt.savefig('figs/fig_{}.png'.format(datetime.datetime.now())
                .replace(":", "-").replace(" ", "_"))
    plt.show()


def main() -> None:
    """Runs script."""
    args = get_args()
    datasets_dir = args.datasets_dir
    models = [
        lr.LinearRegressionNumpy,
        lr.LinearRegressionProcess,
        lr.LinearRegressionSequential,
        lr.LinearRegressionThreads,
    ]

    datasets = read_dataset(datasets_dir)

    results = run_experiments(models, datasets)

    print(results, "\n")
    #make_plot(results)
    make_line_plot(results)


if __name__ == '__main__':
    main()
