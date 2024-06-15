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
__all__ = ["CalibrationDataReader"]

import numpy as np
import warnings

import onnx
from onnxruntime.quantization import CalibrationDataReader as _CalibrationDataReader

from .model import ONNXModel


def gen_random_samples(input_shape, dtype="float32"):
    output_type = np.dtype(dtype)
    rng = np.random.default_rng()
    if issubclass(output_type.type, np.integer):
        iinfo = np.iinfo(output_type)
        return rng.integers(iinfo.min, iinfo.max, input_shape, dtype=dtype)
    return rng.uniform(-1.0, 1.0, input_shape).astype(dtype)


class CalibrationDataReader(_CalibrationDataReader):
    """Object to read or generate a set of samples to calibrate an ONNX model to be quantized.

    If samples are not specified, generate random samples in the range of [-1, 1]
    when input model type is float, otherwise infer ranges.

    Common use mode:
    >>> dr = CalibrationDataReader(onnx_path, num_samples=10, batch_size=1)
    >>> sample = dr.get_next()
    >>> assert sample[dr.inputs_name].shape[0] == 1
    >>> assert sample[dr.inputs_name].min() >= -1
    >>> assert sample[dr.inputs_name].max() <= 1

    Args:
        model (str or ModelProto or ONNXModel): the ONNX model (or its path) to be calibrated.
        samples (str or np.ndarray, optional): the samples (or its path) to process.
            If not provided, generate random samples following the model input shape
            and the batch_size attribute. Defaults to None.
        num_samples (int, optional): the number of samples to generate.
            Ignore it if samples are provided. Defaults to None.
        batch_size (int, optional): split samples in batches.
            Overwrite it when the model has static inputs. Defaults to 1.
    """

    def __init__(self,
                 model,
                 samples=None,
                 num_samples=None,
                 batch_size=1):

        # Read model
        model = _read_model(model)
        self.input_name = model.input[0].name
        input_shape = model.get_input_shape(input_name=self.input_name)
        input_type = model.get_input_dtype(input_name=self.input_name)

        # Read/Generate dataset
        self.batch_size = input_shape[0] if isinstance(input_shape[0], int) else batch_size or 1
        self.dataset = _read_dataset(samples, input_shape, input_type, num_samples=num_samples)

        # Truncate samples to fit model batch size (when is static)
        if isinstance(input_shape[0], int):
            N, res = divmod(self.dataset.shape[0], self.batch_size)
            N *= self.batch_size
            if res != 0:
                warnings.warn("Truncating samples to fit model batch size "
                              f"({N} instead of {self.dataset.shape[0]}).")
                self.dataset = self.dataset[:N]

        # Process samples
        self.index = 0
        self.num_samples = self.dataset.shape[0] / self.batch_size

    def get_next(self):
        if self.index >= self.num_samples:
            print(f"\rCalibrating with {self.index}/{self.num_samples} samples", end="")
            return print()

        sample = self.dataset[self.index * self.batch_size:(self.index + 1) * self.batch_size]
        self.index += 1
        return {self.input_name: sample}

    def rewind(self):
        self.index = 0


def _read_dataset(samples, input_shape, input_type, num_samples=None):
    # Parse sample
    if isinstance(samples, str):
        data = np.load(samples)
        samples = np.concatenate([data[item] for item in data.files])
    elif samples is None:
        if num_samples is None:
            raise ValueError("Either samples or num_samples must be specified")
        samples = gen_random_samples((num_samples, *input_shape[1:]), input_type)
    if not isinstance(samples, np.ndarray):
        raise ValueError(f"Unrecognized '{type(samples)}' samples.")

    # Check when samples comes from file
    assert samples.dtype == input_type, "Samples type does not match with model input one."
    if samples.shape[1:] != input_shape[1:]:
        raise RuntimeError("Samples shape does not match model input shape. "
                           f"Please verify samples are compatible with {input_shape}.")
    return samples


def _read_model(model):
    if isinstance(model, str):
        model = onnx.load_model(model)
    if isinstance(model, onnx.ModelProto):
        model = ONNXModel(model)
    if not isinstance(model, ONNXModel):
        raise ValueError(f"Unrecognized '{type(model)}' model.")

    assert len(model.input) == 1, "multi-input are not supported models yet"
    assert len(model.output) == 1, "multi-outputs are not supported models yet"
    return model
