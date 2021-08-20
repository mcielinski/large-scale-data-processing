# L1 - 2019

## Task 5
Parallelization of computations in Python. Use the prepared code from this directory  
to implement a linear regression model:
- Implement an artificial dataset generator.
```bash
$ python3 scripts/data-generator.py --num-samples <num-samples> --out-dir </path/to/datasets>
```
- Implement linear regression models using:
    - Sequential computations (baseline)
    - Numpy
    - Threaded computation parallelization
    - Process-based computation parallelization
- Generate plots, which show the execution times of the above models with respect to the size of the dataset
```bash
$ PYTHONPATH=. python3 scripts/run-experiments.py --datasets-dir </path/to/datasets>
```
- Ensure the code passes all tests and is well written using `tox`
```bash
$ tox -v
```

