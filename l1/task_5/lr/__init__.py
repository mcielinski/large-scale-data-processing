from . import base
from .lr_np import LinearRegressionNumpy
from .lr_proc import LinearRegressionProcess
from .lr_seq import LinearRegressionSequential
from .lr_thread import LinearRegressionThreads

__all__ = [
    'base',
    'LinearRegressionNumpy',
    'LinearRegressionProcess',
    'LinearRegressionSequential',
    'LinearRegressionThreads',
]
