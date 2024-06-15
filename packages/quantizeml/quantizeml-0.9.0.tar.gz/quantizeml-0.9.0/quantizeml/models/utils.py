#!/usr/bin/env python
# ******************************************************************************
# Copyright 2022 Brainchip Holdings Ltd.
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
"""
Common utility methods used in quantization models.
"""

__all__ = ['load_model', 'apply_weights_to_model', 'get_model_input_dtype']

import warnings
import tensorflow as tf

from keras.models import load_model as kload_model
from ..layers import StatefulRecurrent


def load_model(model_path, custom_layers=None, compile_model=True):
    """Loads a model with quantizeml custom layers.

    Args:
        model_path (str): path of the model to load
        custom_layers (dict, optional): custom layers to add to the model. Defaults to None.
        compile_model (bool, optional): whether to compile the model. Defaults to True.

    Returns:
        keras.Model: the loaded model
    """
    return kload_model(model_path, custom_objects=custom_layers, compile=compile_model)


def apply_weights_to_model(model, weights, verbose=True):
    """Loads weights from a dictionary and apply it to a model.

    Go through the dictionary of weights, find the corresponding variable in the
    model and partially load its weights.

    Args:
        model (keras.Model): the model to update
        weights (dict): the dictionary of weights
        verbose (bool, optional): if True, throw warning messages if a dict item is not found in the
            model. Defaults to True.
    """
    if len(weights) == 0:
        warnings.warn("There is no weight to apply to the model.")
        return

    # Go through the dictionary of weights with each item
    for key, value in weights.items():
        value_applied = False
        for dest_var in model.variables:
            if key == dest_var.name:
                # Apply the current item value
                dest_var.assign(value)
                value_applied = True
                break
        if not value_applied and verbose:
            warnings.warn(f"Variable '{key}' not found in the model.")


def get_model_input_dtype(model):
    """Retrieve the common input dtype for a model

    Handle image like samples (channels in [1, 3]) as uint8, recurrent TENNs as int16 and
    other as int8

    Args:
        model (keras.Model or keras.Sequential): the model to get the input dtype.

    Returns:
        tf.dtype: the expected input type for the model
    """
    if any(isinstance(ly, StatefulRecurrent) for ly in model.layers):
        return tf.int16
    return tf.uint8 if model.input_shape[-1] in [1, 3] else tf.int8
