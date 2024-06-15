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
__all__ = ["generate_keras_random_samples", "generate_onnx_random_samples"]


import numpy as np
import tensorflow as tf
import copy

from ...tensors import QFloat, FixedPoint
from ...models import get_model_input_dtype
from ...onnx_support.graph_tools import value_info_to_tensor_shape


def _get_np_deterministic(size, dtype, min_value=None, max_value=None, rng=None):
    rng = rng or np.random.default_rng()
    dtype = np.dtype(dtype)
    if np.issubdtype(dtype, np.integer):
        iinfo = np.iinfo(dtype)
        min_value = iinfo.min if min_value is None else min_value
        max_value = iinfo.max if max_value is None else max_value
        x = rng.integers(min_value, max_value, size, endpoint=True)
    else:
        min_value = 0.0 if min_value is None else min_value
        max_value = 1.0 if max_value is None else max_value
        x = rng.uniform(min_value, max_value, size)
    return x.astype(dtype)


def _get_tf_deterministic(tf_spec, batch_size=1, min_value=None, max_value=None, rng=None):
    assert isinstance(tf_spec, tf.TensorSpec)
    input_shape = (batch_size, *tf_spec.shape[1:])
    x = _get_np_deterministic(input_shape, tf_spec.dtype.as_numpy_dtype, min_value, max_value, rng)
    return tf.cast(x, tf_spec.dtype)


def _update_keras_spec(keras_spec, value_bits=None, dtype=None):
    def _replace_fp_spec(fp_spec, value_bits):
        if value_bits is not None:
            fp_spec.__dict__["value_bits"] = value_bits

    keras_spec = copy.deepcopy(keras_spec)
    if isinstance(keras_spec, FixedPoint.Spec):
        _replace_fp_spec(keras_spec, value_bits)
    elif isinstance(keras_spec, QFloat.Spec):
        _replace_fp_spec(keras_spec.fp, value_bits)
    elif isinstance(keras_spec, tf.TensorSpec) and dtype is not None:
        keras_spec._dtype = tf.as_dtype(dtype)
    return keras_spec


def generate_keras_random_samples(model, batch_size=1, seed=None):
    """Generate a random set of inputs for a model.

    Args:
        model (tf.keras.Model): the target model to generate inputs.
        batch_size (int, optional): a batch size. Defaults to 1.
        seed (int, optional): a random seed (reproducibility purpose). Defaults to None.

    Returns:
        tf.Tensor: a set of samples
    """
    rng = np.random.default_rng(seed=seed)
    input_dtype = get_model_input_dtype(model)
    input_specs_list = model.input if isinstance(model.input, (list, tuple)) else [model.input]
    gen_inputs = []
    for idx, keras_spec in enumerate(input_specs_list):
        if seed is not None:
            rng = np.random.default_rng(seed=seed + idx)
        # Replace dtype in spec to generate integer values
        integer_keras_spec = _update_keras_spec(keras_spec.type_spec, dtype=input_dtype)
        xq = _get_tf_deterministic(integer_keras_spec, batch_size, rng=rng)
        gen_inputs.append(tf.cast(xq, keras_spec.dtype))

    if not isinstance(model.input, (list, tuple)):
        return gen_inputs[0]
    return gen_inputs


def generate_onnx_random_samples(model, batch_size=1, seed=None):
    """Generate a random set of inputs for a model.

    Args:
        model (ONNXModel): the target model to generate inputs.
        batch_size (int, optional): a batch size. Defaults to 1.
        seed (int, optional): a random seed (reproducibility purpose). Defaults to None.

    Returns:
        np.ndarray: a set of samples
    """
    rng = np.random.default_rng(seed=seed)
    gen_inputs = {}
    for idx, input_vi in enumerate(model.input):
        if seed is not None:
            rng = np.random.default_rng(seed=seed + idx)

        # Retrieve shape from value info
        shape, dtype = value_info_to_tensor_shape(input_vi)
        gen_inputs[input_vi.name] = _get_np_deterministic((batch_size, *shape[1:]), dtype, rng=rng)
    return gen_inputs
