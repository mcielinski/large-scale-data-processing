"""Script for generation of artificial datasets."""
import argparse
import pickle
from typing import List
from typing import Tuple

from sklearn.datasets import make_regression


def get_args() -> argparse.Namespace:
    """Parses script arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--num-samples',
        required=True,
        help='Number of samples to generate',
        type=int,
    )
    parser.add_argument(
        '--out-dir',
        required=True,
        help='Name of directory to save generated data',
        type=str,
    )

    return parser.parse_args()


def generate_data(num_samples: int) -> Tuple[List[float], List[float]]:
    """Generated X, y with given number of data samples."""
    X, y = make_regression(n_samples=num_samples, n_features=1, noise=0.1)
    X = list(X.flatten())
    y = list(y)

    return X, y


def save_data(data, output_dir, name_part):
    file_name = output_dir + '/data_' + str(name_part)
    with open(file_name, 'wb') as file:
        pickle.dump(data, file)


def main() -> None:
    """Runs script."""
    args = get_args()
    num_samples = args.num_samples
    output_dir = args.out_dir
    data = generate_data(num_samples)
    save_data(data, output_dir, num_samples)


if __name__ == '__main__':
    main()
