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
import tensorflow as tf

from ... import layers as keras_qml_layers
from ...layers.layers_base import QuantizedLayer
from ...tensors import QTensor
from ...models.transforms import sanitize as keras_sanitize
from ..tools import generate_keras_random_samples
from .common import (compare, make_fn_on_list, remove_outliers, eval_metrics, merge_metrics,
                     compute_saturation)

skippable_layers = (keras_qml_layers.QuantizedDropout, keras_qml_layers.QuantizedFlatten,
                    keras_qml_layers.QuantizedReshape, keras_qml_layers.QuantizedRescaling)
conditional_skippable_layers = (keras_qml_layers.QuantizedMaxPool2D,
                                keras_qml_layers.QuantizedGlobalAveragePooling2D)


def _convert_to_list(x):
    if not isinstance(x, (tuple, list)):
        x = [x]
    return x


@make_fn_on_list
def _dequantize(x, /):
    return x.to_float() if isinstance(x, QTensor) else x


def _compute_mask(x, /):
    min_value = -2**x.value_bits
    max_value = 2**x.value_bits - 1
    values = x.values.numpy()
    return (values > min_value) & (values < max_value)


def _is_measurable(qlayer):
    if isinstance(qlayer, conditional_skippable_layers):
        return getattr(qlayer, "out_quantizer", None) is not None
    return not isinstance(qlayer, skippable_layers) and isinstance(qlayer, QuantizedLayer)


def _get_layer(layer_name, model):
    try:
        layer = model.get_layer(layer_name)
    except Exception:
        raise RuntimeError(f"{model.name} must have layer '{layer_name}'")
    return layer


def _search_quantized_target_layers(model, target_layer_name=None):
    if target_layer_name is not None:
        target_layers = [_get_layer(target_layer_name, model)]
    else:
        target_layers = model.layers
    # Filter target layers
    target_layers = [ly for ly in target_layers if _is_measurable(ly)]
    if len(target_layers) == 0:
        raise ValueError(f"{model.name} does not contain layers that generate quantization error!")
    return target_layers


@make_fn_on_list
def compare_outputs(foutputs, qoutputs, /, per_channel=False):
    """Measures the error in a set of tensors

    Args:
        foutputs (tf.Tensor or list): the output of a float layer.
        qoutputs (QTensor or list): the quantized output to be compare with ``foutputs``.
        per_channel (bool, optional): comparison is done for each channel. Defaults to False.

    Returns:
        dict or list: the quantization error.
    """
    assert isinstance(qoutputs, QTensor), f"{qoutputs} must be a QTensor"
    axis = -1 if per_channel else None

    # Compute saturation and mask where is indicated if a value saturate or not
    saturation = compute_saturation(qoutputs, axis=axis)
    mask = _compute_mask(qoutputs)

    # Dequantize and convert tensors to numpy
    foutputs = foutputs.numpy()
    qoutputs = qoutputs.to_float().numpy()

    # Exclude samples that saturate since the error is ambiguous out of range.
    foutputs = remove_outliers(foutputs, mask, axis=axis)
    qoutputs = remove_outliers(qoutputs, mask, axis=axis)
    return compare(foutputs, qoutputs, saturation)


def quantization_error(fmodel, qmodel, target_layer=None, batch_size=1, seed=None):
    """Measures the layer quantization error in a set of Keras models

    Args:
        fmodel (tf.keras.Model): the float model.
        qmodel (tf.keras.Model): the quantized version of `fmodel`.
        target_layer (str, optional): computation error is performed only in the target layer,
            expanding the analysis to each output channel. Defaults to None.
        batch_size (int, optional): the batch size. Defaults to 1.
        seed (int, optional): a random seed. Defaults to None.

    Returns:
        dict: the quantization error of the target layers
    """
    per_channel = target_layer is not None

    # Sanitize float model
    fmodel = keras_sanitize(fmodel)

    # Create an intermediary quantized model that will compute the inputs for both models
    target_qlayers = _search_quantized_target_layers(qmodel, target_layer_name=target_layer)
    qmodel = tf.keras.Model(qmodel.input, [qly.input for qly in target_qlayers])

    # Generate a random set of samples
    samples = generate_keras_random_samples(qmodel, batch_size=batch_size, seed=seed)

    # Compute quantization error per layer:
    # Generate the set of input quantized samples
    summary = {}
    qinputs = qmodel(samples)
    for qlayer, qx in zip(target_qlayers, _convert_to_list(qinputs)):
        # Match quantized layer in fmodel
        flayer = _get_layer(qlayer.name, fmodel)

        # Forward qx in both qlayer and flayer.
        # Note there is no error provided by inputs quantization
        qoutputs = qlayer(qx)
        foutputs = flayer(_dequantize(qx))

        # Compute quantization error per layer
        key = f"{qlayer.name} ({qlayer.__class__.__name__})"
        summary[key] = eval_metrics(compare_outputs(foutputs, qoutputs, per_channel=per_channel))
    return summary


def cumulative_quantization_error(fmodel, qmodel, target_layer=None, batch_size=1, seed=None):
    """Measures the cumulative quantization error in a set of Keras models

    Args:
        fmodel (tf.keras.Model): the float model.
        qmodel (tf.keras.Model): the quantized version of `fmodel`.
        target_layer (str, optional): error computation is performed only in the target layer,
            expanding the analysis to each output channel. Defaults to None.
        batch_size (int, optional): the batch size. Defaults to 1.
        seed (int, optional): a random seed. Defaults to None.

    Returns:
        dict: the quantization error by each layer
    """
    per_channel = target_layer is not None

    # Sanitize float model
    fmodel = keras_sanitize(fmodel)

    # Create intermediary models with the target outputs
    target_qlayers = _search_quantized_target_layers(qmodel, target_layer_name=target_layer)
    qmodel = tf.keras.Model(qmodel.input, [qly.output for qly in target_qlayers])
    foutputs = [_get_layer(ly.name, fmodel).output for ly in target_qlayers]
    fmodel = tf.keras.Model(fmodel.input, foutputs)

    # Generate a random set of samples
    samples = generate_keras_random_samples(qmodel, batch_size=batch_size, seed=seed)

    # Compute cumulative quantization error
    summary = {}
    samples = tf.expand_dims(samples, axis=1)
    for x in samples:
        # To avoid out-of-memory problems, we pass sample by sample
        outputs = _convert_to_list(fmodel(x)), _convert_to_list(qmodel(x))
        for qlayer, foutputs, qoutputs in zip(target_qlayers, *outputs):
            key = f"{qlayer.name} ({qlayer.__class__.__name__})"
            qerror = compare_outputs(foutputs, qoutputs, per_channel=per_channel)
            if key in summary:
                # Accumulates the error with previous results
                qerror = merge_metrics(qerror, summary[key])
            summary[key] = qerror

    # Finally, evaluate the result of all metrics
    for key in summary:
        summary[key] = eval_metrics(summary[key])
    return summary
