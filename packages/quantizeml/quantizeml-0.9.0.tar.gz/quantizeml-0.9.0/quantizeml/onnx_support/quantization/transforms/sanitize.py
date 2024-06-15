#!/usr/bin/env python
# ******************************************************************************
# Copyright 2023 Brainchip Holdings Ltd.
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
__all__ = ['sanitize']

import os
import tempfile
from pathlib import Path

from onnxruntime.quantization.quant_utils import load_model

from .remove_pad_nodes import fold_pad_into_conv
from ..model import ONNXModel


def sanitize(model):
    """Sanitize a model preparing it for quantization.

    This is a wrapping successive calls to several model transformations
    which aims at making the model quantization ready.

    Args:
        model: the input model

    Returns:
        the sanitized model
    """
    assert isinstance(model, ONNXModel)

    # Clone model to prevent modification of the original one
    model = model.clone()

    # Replace operations to match with current ONNX version
    model.update_model_version()

    # Clean inputs/outputs
    model.clean_graph_io()

    # Perform optimization only if model is not quantized
    if not any(node.domain == "com.brainchip" for node in model.nodes()):
        with tempfile.TemporaryDirectory(prefix="pre.quant.") as quant_tmp_dir:
            # To perfom ONNXRuntime optimization, we would like to use
            # onnxruntime.quantization.load_model, to optimize the model (when required)
            # and infer the intermediate shapes.
            # However, it always expects to read the model from a path. That is why we
            # save the input model if it is not a path.
            tmp_model_path = os.path.join(quant_tmp_dir, "model.onnx")
            model.save_model_to_file(tmp_model_path)

            # Perform preprocessing
            model = ONNXModel(load_model(Path(tmp_model_path), need_optimize=True))

    # Fold pad into conv when possible
    fold_pad_into_conv(model)

    return model
