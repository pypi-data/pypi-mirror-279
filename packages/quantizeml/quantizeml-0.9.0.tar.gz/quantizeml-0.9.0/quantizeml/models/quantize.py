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

__all__ = ["quantize", "dump_config"]

import warnings
from collections import defaultdict

import numpy as np
import keras
from onnx import ModelProto
try:
    # Legacy support for keras 2.10
    from keras.utils.generic_utils import get_registered_object, get_registered_name
except ImportError:
    from keras.saving.object_registration import get_registered_object, get_registered_name

from .utils import apply_weights_to_model
from .transforms import sanitize
from .transforms.insert_layer import insert_in_config
from .transforms.transforms_utils import get_inbound_layers_config
from .calibrate import calibrate
from ..layers import (OutputQuantizer, WeightQuantizer, Dequantizer, quantization,
                      QuantizationParams, get_quantization_params, Attention, QuantizedConv2D,
                      QuantizedDepthwiseConv2D, QuantizedSeparableConv2D, QuantizedDense,
                      StatefulRecurrent)
from ..layers.layers_base import (_GLOBAL_LAYER_TO_QLAYER, _GLOBAL_NO_OUTPUT_QUANTIZER,
                                  _GLOBAL_ALIGNED_INPUTS)
from ..onnx_support.quantization.quantize import quantize as quantize_onnx


# List of Quantizer layer's that do not have a float layer representation
NO_FLOAT_CUSTOM_QLAYERS = [Dequantizer, OutputQuantizer, WeightQuantizer]


def get_quantized_layer(layer):
    """ Returns the quantized version of the layer.

    Args:
        layer (keras.layers.Layer or type): layer of interest

    Returns:
        keras.layer: quantized version of the layer if it exists, None otherwise.
    """
    if isinstance(layer, type):
        return _GLOBAL_LAYER_TO_QLAYER.get(layer.__name__, None)
    return _GLOBAL_LAYER_TO_QLAYER.get(layer.__class__.__name__, None)


def is_quantized_layer(layer):
    """ Returns True when the layer is a quantized layer.

    Args:
        layer (keras.layers.Layer or type): layer of interest

    Returns:
        bool: True when the layer is a quantized layer, False otherwise.
    """
    if isinstance(layer, type):
        return layer in _GLOBAL_LAYER_TO_QLAYER.values()
    return layer.__class__ in _GLOBAL_LAYER_TO_QLAYER.values()


def get_layer_class_from_name(name):
    """ Returns the class object of a registered keras layer.

    Args:
        name (str): the layer class name

    Returns:
        type: the class of the layer
    """
    if hasattr(keras.layers, name):
        return getattr(keras.layers, name)
    return get_registered_object(name)


def _handle_not_quantizable_layers(model, config, skip_warning=False):
    """ Includes a number of dequantizers such that the model is compatible.

    Args:
        model (keras.Model): model structure to check
        config (dict): config where Dequantizer(s) will be placed
        skip_warning (bool_optional): whether to skip warning provided by partial quantization.
            Defaults to False.

    Returns:
        bool: whether the model was fully quantized.
    """
    # Find where to insert the Dequantizer(s):
    # A dequantizer will be added for all links that connect a quantized layer to a floating one.
    num_no_quantizable_layers = 0
    dequantizer_inbounds = defaultdict(list)
    for layer in config['layers']:
        layer_class = get_layer_class_from_name(layer['class_name'])
        if layer_class == Dequantizer:
            # If a model has a Dequantizer is because it is requantizing.
            # In that case nothing has to be done (model already has the necessary dequantizers)
            return False
        elif not (is_quantized_layer(layer_class) or layer_class in NO_FLOAT_CUSTOM_QLAYERS):
            # The current layer is float.
            for inbound_layer in get_inbound_layers_config(layer, config):
                inbound_layer_class = get_layer_class_from_name(inbound_layer['class_name'])
                # A dequantizer will be added for each quantized inbound layer
                if is_quantized_layer(inbound_layer_class):
                    inbound_layer_name = inbound_layer['config']['name']
                    if len(dequantizer_inbounds) == 0 and not skip_warning:
                        # Print warning for the first non-quantizable layer
                        warnings.warn(f"'{layer['config']['name']}' of type {layer['class_name']} "
                                      "is not supported to quantize, a Dequantizer is added "
                                      "before it and quantization will stop at this layer.")
                    dequantizer_inbounds[inbound_layer_name].append(layer['config']['name'])
            num_no_quantizable_layers += 1

    if len(config['layers']) == num_no_quantizable_layers:
        raise RuntimeError(f"Impossible to quantize '{model.name}'. "
                           "At least one layer should be quantizable.")
    if len(dequantizer_inbounds) == 0:
        # Model was completely quantized.
        return True

    # Insert a Dequantizer on each target_layer -> outbound link
    for target_layer_name, outbound_names in dequantizer_inbounds.items():
        dequantizer = Dequantizer(name=f'{target_layer_name}/dequantizer')
        insert_in_config(model, target_layer_name, dequantizer, config, outbound_names)
    return False


def _prepare_output_quantizers(model):
    """ Parse the model and prepare OutputQuantizer configurations for layers requiring them.

    To ensure that an OutputQuantizer will be added to the latest possible layer in a 'block', the
    model is parsed in reverse order. If a layer requires aligned inputs, the function will find the
    preceding layer that can accept an OutputQuantizer and set it in the returned dictionary.

    Args:
        model (keras.Model): the model to parse

    Returns:
        dict: dictionary mapping layer names to an OutputQuantizer config.
    """
    # Dictionary that will contain layers and their OutputQuantizer configurations
    out_quantizer_configs = {}

    # Get quantization parameters
    qparams = get_quantization_params()

    def set_output_quantizer(layer_names, next_layer):
        """ Populates `out_quantizer_configs` with layer names and their OutputQuantizer. """
        for name in layer_names:
            current_layer = model.get_layer(name)
            # Handle special cases were the OutputQuantizer must be per-tensor:
            # - when current_layer has vector outputs,
            # - when next_layer is an Attention layer and the layer is Query or Key
            #   (first and second inputs)
            # - when the layer is a StatefulRecurrent layer
            if isinstance(current_layer, Attention):
                output_shape = current_layer.output_shape[0]
            else:
                output_shape = current_layer.output_shape
            # remove batch_size dim
            output_shape = output_shape[1:]
            vector_outputs = np.prod(output_shape) == output_shape[-1]
            query_or_key = (isinstance(current_layer, keras.layers.Dense)
                            and isinstance(next_layer, Attention)
                            and next_layer.inbound_nodes[0].inbound_layers.
                            index(current_layer) in [0, 1])
            is_stateful_rec = isinstance(current_layer, StatefulRecurrent)
            per_tensor = (query_or_key or vector_outputs or is_stateful_rec or
                          qparams.per_tensor_activations)

            # If this is a new entry, set a default configuration
            if name not in out_quantizer_configs:
                axis = "per-tensor" if per_tensor else "per-axis"
                if isinstance(current_layer, keras.layers.ReLU):
                    params = dict(bitwidth=qparams.activation_bits,
                                  signed=qparams.activation_bits >= 8,
                                  axis=axis)
                else:
                    # StatefulRecurrent special: previous and self OutputQuantizer should be 16-bits
                    if is_stateful_rec or isinstance(next_layer, StatefulRecurrent):
                        bitwidth = 16
                    else:
                        bitwidth = qparams.output_bits
                    params = dict(bitwidth=bitwidth, axis=axis)
                out_quantizer_configs[name] = dict(output_quantizer=params)

            # If the layer OutputQuantizer configuration is already set, simply check the axis:
            # override the config if the outputs must be per-tensor
            else:
                current_axis = out_quantizer_configs[name]["output_quantizer"]["axis"]
                per_tensor = per_tensor or current_axis == "per-tensor"
                axis = "per-tensor" if per_tensor else "per-axis"
                out_quantizer_configs[name]["output_quantizer"]["axis"] = axis

    def cannot_have_output_quantizer(layer):
        """ Returns True when the layer cannot have an OutputQuantizer. """
        qlayer = get_quantized_layer(layer)
        return (isinstance(layer, Dequantizer)
                or qlayer is None
                or qlayer in _GLOBAL_NO_OUTPUT_QUANTIZER)

    def get_preceding_layer_names(layer):
        """ Retrieve inbounds layers names where an OutputQuantizer can be set. """
        previous_layers = []
        inbounds = layer.inbound_nodes[0].inbound_layers
        if not isinstance(inbounds, list):
            inbounds = [inbounds]
        for inbound in inbounds:
            # Skip input layers
            if isinstance(inbound, keras.layers.InputLayer):
                continue
            # When the given layer cannot have an OutputQuantizer, recursively call the function on
            # this layer
            if cannot_have_output_quantizer(inbound):
                previous_layers.extend(get_preceding_layer_names(inbound))
            else:
                previous_layers.append(inbound.name)
        return previous_layers

    # Parse the layers in reverse order
    for layer in model.layers[::-1]:
        # Find layers that will need aligned inputs
        if get_quantized_layer(layer) in _GLOBAL_ALIGNED_INPUTS:
            # Retrieve the inbounds that can have an OutputQuantizer
            previous_layers = get_preceding_layer_names(layer)
            # Set an OutputQuantizer in their inbounds
            set_output_quantizer(previous_layers, layer)

    return out_quantizer_configs


def quantize_keras(model, q_config=None, qparams=QuantizationParams(), samples=None,
                   num_samples=1024, batch_size=None, epochs=1, quantize_until=None):
    """Quantizes a Keras model using the provided configuration or parameters.

    Details on how this function behaves:

    - `q_config` has priority over `qparams`, meaning that when a match is found in `q_config` the
      given configuration will be used instead of `qparams`. This is useful to handle specific cases
      (e.g per-tensor output quantizer).
    - when no configuration is given, quantization parameters are deduced from `qparams` and
      OutputQuantizers are automatically set on appropriate layers.
    - `qparams` are only applied to 'float' Keras layers when they are first quantized. As a result,
      when re-quantizing a model, one must provide a complete `q_config`. This is made easy with the
      `dump_config` helper.

    If not already present, a final Dequantizer will be added at the end of the Model.

    The model will also be calibrated using the provided (or randomly generated inputs).

    Args:
        model (keras.Model): the model to quantize
        q_config (dict, optional): quantization configuration as a dictionary mapping layer names to
            their quantization configuration. Defaults to None.
        qparams (QuantizationParams, optional): global quantization parameters. Defaults to
            QuantizationParams().
        samples (tf.Dataset, np.array or generator, optional): calibration samples. When no samples
            are provided, random samples are generated. Defaults to None.
        num_samples (int, optional): number of samples to use in the provided samples or number of
            samples to generate. Defaults to 1024.
        batch_size (int, optional): the batch size. Defaults to None.
        epochs (int, optional): the number of epochs. Defaults to 1.
        quantize_until (str, optional): name of the layer until which to quantize:
            other layers after it will stay unchanged. Defaults to None.

    Returns:
        keras.Model: the quantized model
    """
    q_config = q_config or dict()
    if quantize_until and not any(ly.name == quantize_until for ly in model.layers):
        raise ValueError(f"'{quantize_until}' is not a recognized layer in {model.name}")

    # Handle input_weight_bits using another QuantizationParams where
    # weight_bits = qparams.input_weight_bits, it will be set to False once the input layer has been
    # quantized.
    input_qparams = QuantizationParams(activation_bits=qparams.activation_bits,
                                       per_tensor_activations=qparams.per_tensor_activations,
                                       weight_bits=qparams.input_weight_bits,
                                       output_bits=qparams.output_bits,
                                       buffer_bits=qparams.buffer_bits)

    def get_quantize_layer(layer, quantize_config=None):
        """Get quantize config from float layer:
            - first, we get its quantized version,
            - then, we return the quantized layer with config updated
        """
        # Check if qlayer exists in custom layers and returns the float version of the layer if not
        l_class = get_layer_class_from_name(layer["class_name"])
        ql_class = get_quantized_layer(l_class)
        if ql_class is None:
            ql_class = l_class

        # Initialize quantized layer from the float config
        qlayer = layer

        # Instantiate quantized layer from configuration if there is one
        if quantize_config:
            qlayer['config']['quant_config'] = quantize_config
        # Set the preset default configuration otherwise
        elif qlayer['config']['name'] in out_quantizer_configs:
            qlayer['config']['quant_config'] = out_quantizer_configs[qlayer['config']['name']]

        # Retrieve the quantize config after initializing the quantized layer, in order to
        # configure the specific parameters given by the QuantizationParams context.
        qlayer['config'] = ql_class.from_config(qlayer['config']).get_config()

        # Update layer class name by the quantized one
        qlayer['class_name'] = get_registered_name(ql_class)
        return qlayer

    # Sanitize the model and make it quantization ready
    model = sanitize(model)

    # Determine where to set OutputQuantizers, the return dict will be used as a non-local
    # variable in the _replace_layer function.
    with quantization(qparams):
        out_quantizer_configs = _prepare_output_quantizers(model)

    # Quantize the model, modifying each layer config by its respective quantized version
    input_layers = (QuantizedConv2D, QuantizedDepthwiseConv2D, QuantizedSeparableConv2D,
                    QuantizedDense)
    qmodel_config = model.get_config()
    quantized_layers = set()
    for idx, layer in enumerate(qmodel_config['layers']):
        # If some layer is quantized then this is requantization.
        # Raise exception for this case if quantize_until is provided
        layer_class = get_layer_class_from_name(layer['class_name'])
        if is_quantized_layer(layer_class) and quantize_until:
            raise ValueError("'quantize_until' is not supported when requantizing.")

        # Retrieve quantize config from layer
        match_conf = q_config.get(layer['config']['name'], None)

        # Overwrite quantization context with input_qparams (if they are not None)
        with quantization(input_qparams or qparams):
            inbound_layers = get_inbound_layers_config(layer, qmodel_config)
            # Quantization is only performed if the inbound layers were quantized
            if all(x['config']['name'] in quantized_layers for x in inbound_layers):
                qlayer = get_quantize_layer(layer, match_conf)
            else:
                qlayer = layer

        # When the qlayer is an input layer that has been quantized, disable input_qparams
        qlayer_class = get_layer_class_from_name(qlayer['class_name'])
        if input_qparams and qlayer_class in input_layers:
            input_qparams = None

        # Skip input layers
        if qlayer_class == keras.layers.InputLayer:
            # Although InputLayer is not quantizable, layer is treated as one
            # so its outbounds can be quantized.
            quantized_layers.add(qlayer['config']['name'])
            continue

        # If it was not possible to quantize the layer, try to quantize the next one.
        # This ensures that as many layers as possible are quantized.
        if not is_quantized_layer(qlayer_class):
            continue

        # Finally, update model with quantize layer config
        # Note at this point, we know the layer was quantized successfully
        qmodel_config['layers'][idx] = qlayer
        if quantize_until != layer["config"]["name"]:
            # If quantize_until is provided, layer is quantized but is not added to
            # quantized_layers list, preventing the quantization of layers after it.
            # Note if layer is within a branch, quantization will end only for this branch
            quantized_layers.add(qlayer['config']['name'])

    # Insert the number of Dequantizers necessary for the model to be compatible
    is_full_quantized = _handle_not_quantizable_layers(model,
                                                       qmodel_config,
                                                       skip_warning=quantize_until is not None)

    # Build the model and transfer weights
    qmodel = model.from_config(qmodel_config)
    apply_weights_to_model(qmodel, {var.name: var for var in model.variables}, False)

    # Convert model into a functional one.
    # Note if model was completely quantized, we add a last dequantizer to produce a float output
    y = qmodel.output
    if is_full_quantized:
        y = Dequantizer()(y)
    qmodel = keras.Model(qmodel.input, y, name=model.name)

    # Now that the model is quantized, proceed to calibration
    calibrate(model, qmodel, samples=samples, num_samples=num_samples, batch_size=batch_size,
              epochs=epochs)
    return qmodel


def quantize(model, q_config=None, qparams=QuantizationParams(), samples=None, num_samples=1024,
             batch_size=None, epochs=1, quantize_until=None):
    """Quantizes a Keras or ONNX model using the provided configuration or parameters.

    Details on how this function behaves:

    - `q_config` has priority over `qparams`, meaning that when a match is found in `q_config` the
      given configuration will be used instead of `qparams`. This is useful to handle specific cases
      (e.g per-tensor output quantizer). This is only used when quantizing Keras models.
    - when no configuration is given, quantization parameters are deduced from `qparams` and
      OutputQuantizers are automatically set on appropriate layers.
    - `qparams` are only applied to 'float' Keras layers when they are first quantized. As a result,
      when re-quantizing a model, one must provide a complete `q_config`. This is made easy with the
      `dump_config` helper. Note the only configuration supported when quantizing ONNX models is
      8-bit for weights and activations, but per_tensor_activations param will be taken into
      account.

    If not already present, a final Dequantizer will be added at the end of the Model.

    The model will also be calibrated using the provided (or randomly generated inputs).

    Args:
        model (keras.Model or ModelProto): the model to quantize
        q_config (dict, optional): quantization configuration as a dictionary mapping layer names to
            their quantization configuration. Defaults to None.
        qparams (QuantizationParams, optional): global quantization parameters. Defaults to
            QuantizationParams().
        samples (tf.Dataset, np.array or generator, optional): calibration samples. When no samples
            are provided, random samples are generated. Defaults to None.
        num_samples (int, optional): number of samples to use in the provided samples or number of
            samples to generate. Defaults to 1024.
        batch_size (int, optional): the batch size. Defaults to None.
        epochs (int, optional): the number of epochs. This parameter must be 1 for ONNX models.
            Defaults to 1.
        quantize_until (str, optional): name of the layer/node until which to quantize:
            other ones after it will stay unchanged. Defaults to None.

    Returns:
        keras.Model or ModelProto: the quantized model
    """
    # Calibration with random samples will only provide meaningful results when quantizing
    # per-tensor
    if samples is None and not qparams.per_tensor_activations:
        warnings.warn("Quantizing per-axis with random calibration samples is not accurate.\
                       Set QuantizationParams.per_tensor_activations=True when calibrating with \
                       random samples.")
    if type(model) != ModelProto:
        return quantize_keras(model=model,
                              q_config=q_config,
                              qparams=qparams,
                              samples=samples,
                              num_samples=num_samples,
                              batch_size=batch_size,
                              epochs=epochs,
                              quantize_until=quantize_until)
    elif q_config:
        raise ValueError("unsupported parameter q_config for ONNX models quantization")
    elif epochs != 1:
        raise ValueError("unsupported parameter epochs != 1 for ONNX models quantization")
    return quantize_onnx(model=model,
                         qparams=qparams,
                         samples=samples,
                         num_samples=num_samples,
                         batch_size=batch_size,
                         quantize_until=quantize_until)


def dump_config(model):
    """Dump the quantization configuration of a quantized model, exporting the configuration for
    each quantized layer.

    Args:
        model (keras.Model): a quantized model.

    Returns:
        dict: the configuration of the model.
    """
    # Get the configuration of the model, iterating over each layer and updating on config.
    config = {}
    for layer in model.layers:
        # Try to take the current quantized configuration
        ly_config = layer.get_config().get('quant_config')

        # Only append quantized configuration
        if is_quantized_layer(layer) and ly_config:
            config[layer.name] = ly_config

    return config
