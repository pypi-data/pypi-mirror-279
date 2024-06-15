#!/usr/bin/env python
# ******************************************************************************
# Copyright 2024 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************
__all__ = ["make_fn_on_list", "remove_outliers", "compare", "merge_metrics", "eval_metrics"]

import numpy as np

from ..tools import WeightedMAPE, Saturation


def make_fn_on_list(func):
    """Decorator that handles list arguments to a function.

    Call the function recursively for each iterable-element in the arguments.
    Stops when the arguments are no longer a list.

    Note auxiliary key-arguments are propagated for each call with their value.

    Args:
        func (callable): function to call.
    """
    def wrapper_fn(*args, **kwargs):
        types = (list, tuple)
        if any(isinstance(x, types) for x in args):
            assert all(isinstance(x, types) for x in args), "All args must be a list or tuple"
            assert all(len(args[0]) == len(x) for x in args), "All args must have the same length"
            return [wrapper_fn(*new_args, **kwargs) for new_args in zip(*args)]
        return func(*args, **kwargs)
    return wrapper_fn


def make_fn_on_dict(func):
    """Decorator that handles dictionaries arguments to a function.

    Call the function recursively for each iterable-element in the arguments.
    Stops when the arguments are no longer a dictionnary.

    Note auxiliary key-arguments are propagated for each call with their value.

    Args:
        func (callable): function to call.
    """
    def wrapper_fn(*args, **kwargs):
        if any(isinstance(x, dict) for x in args):
            assert all(isinstance(x, dict) for x in args), "All args must be a dict"
            keys = args[0].keys()
            if not all(k in keys for x in args for k in x):
                raise KeyError("All args must have the same keys")
            return {k: wrapper_fn(*tuple(x[k] for x in args), **kwargs) for k in keys}
        return func(*args, **kwargs)
    return wrapper_fn


def remove_outliers(values, mask, /, axis=None):
    """Remove outliers marked by mask

    Args:
        x (np.ndarray): values to remove outliers
        mask (np.ndarray): boolean mask where True is consider as an outlier
        axis (int, optional): outliers are removed through this dimension,
            returning a list instead of an array. Defaults to None.

    Returns:
        np.ndarray or list: the masked values
    """
    assert values.shape == mask.shape, "Both values and mask must have same shape"
    if axis is not None:
        result = []
        for idx in range(values.shape[axis]):
            result.append(np.take(values, idx, axis=axis)[np.take(mask, idx, axis=axis)])
        return result
    return values[mask]


def compute_saturation(x, /, axis=None, min_value=None, max_value=None):
    """Returns the percentage of saturating values.

    Args:
        x (np.ndarray or QTensor): the values to verify.
        axis (int, optional): saturation is computed through this dimension,
            returning a list instead of an array. Defaults to None.
        min_value (np.ndarray, optional): the minimum of values.
            If not provided, it is inferred from the values type. Defaults to None.
        max_value (np.ndarray, optional): the maximum of values.
            If not provided, it is inferred from the values type. Defaults to None.

    Returns:
        np.ndarray or list: the saturation percentage
    """
    try:
        # Overwrit max_value, min_value if x is a QTensor
        min_value = -2**x.value_bits
        max_value = 2**x.value_bits - 1
        x = x.values.numpy()
    except AttributeError:
        pass
    if axis is not None:
        saturation = []
        for idx in range(x.shape[axis]):
            metric = Saturation(min_value=min_value, max_value=max_value, dtype=x.dtype)
            # Compute saturation over axis
            metric.update_state(np.take(x, idx, axis=axis))
            saturation.append(metric)
        return saturation
    # Compute saturation over x
    metric = Saturation(min_value=min_value, max_value=max_value, dtype=x.dtype)
    metric.update_state(x)
    return metric


@make_fn_on_list
def compare(x, y, saturation, /):
    """Compare the set (x, y) element-wise

    Args:
        x (np.ndarray or list): the ground truth.
        y (np.ndarray or list): the array to compare with x.
        saturation (Saturation or list): saturation metric to be included in the result.

    Returns:
        dict or list: list of measures
    """
    wmape = WeightedMAPE()
    wmape.update_state(x, y)
    return {"wMAPE": wmape, "Saturation (%)": saturation}


@make_fn_on_list
@make_fn_on_dict
def merge_metrics(metric1, metric2, /):
    """Creates a metric from the variables in a set of metrics

    Args:
        metric1 (list or dict or keras.Metric): first metric to be merged
        metric2 (list or dict or keras.Metric): second metric to be merged

    Returns:
        list or dict or keras.Metric: the merged metric
    """
    if not isinstance(metric1, metric2.__class__):
        raise RuntimeError("Only metrics with the same type can be merged")
    if metric1.get_config() != metric2.get_config():
        raise ValueError("Both metrics must be compiled with the same config to be merged")

    # Create a new metric with config
    merged_metric = metric1.from_config(metric1.get_config())
    # Update states
    for tvar, v1, v2 in zip(merged_metric.variables, metric1.variables, metric2.variables):
        tvar.assign(v1 + v2)
    return merged_metric


@make_fn_on_list
@make_fn_on_dict
def eval_metrics(metric, /):
    """Call 'result' function in a set of metrics

    Args:
        metric (list or dict or keras.Metric): the metric to be evaluated

    Returns:
        list or dict or np.ndarray: the evaluated metrics
    """
    return metric.result().numpy()
