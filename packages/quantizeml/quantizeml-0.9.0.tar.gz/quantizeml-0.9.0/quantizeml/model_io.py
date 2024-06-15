__all__ = ["load_model", "save_model"]

import os
import keras
import onnx
from .models import load_model as load_model_keras


def load_model(model_path):
    """
    Loads an Onnx or Keras model. An error is raised if the provided model
        extension is not supported.

    Args:
        model_path (str): path of the model to load.

    Returns:
        keras.models.Model or onnx.ModelProto: Loaded model.
    """
    _, model_extension = os.path.splitext(model_path.lower())

    if model_extension == '.h5':
        model = load_model_keras(model_path)
    elif model_extension == '.onnx':
        model = onnx.load_model(model_path)
    else:
        raise ValueError(
            f"Unsupported model extension: '{model_extension}'. "
            f"Expected model with extension(s): {['h5', 'onnx']}"
        )

    return model


def save_model(model, path):
    """
    Save an ONNX or Keras model into a path.

    Note extension is overwritten given the model type.

    Args:
        model (keras.Model, keras.Sequential or onnx.ModelProto): model to serialize.
        model_path (str): path to save the model.

    Returns:
        str: the path where the model was saved.
    """
    model_name, _ = os.path.splitext(path)
    if isinstance(model, (keras.Model, keras.Sequential)):
        model_path_with_ext = model_name + ".h5"
        model.save(model_path_with_ext, include_optimizer=False)
    elif isinstance(model, onnx.ModelProto):
        model_path_with_ext = model_name + ".onnx"
        onnx.save_model(model, model_path_with_ext)
    else:
        raise ValueError(f"Unrecognized {type(model)} model type. Expected a keras or ONNX model.")
    return model_path_with_ext
