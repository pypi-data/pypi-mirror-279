import itertools
import re
import warnings
from string import ascii_uppercase as uppercase_letters

import pandas as pd
import scanpy
import tensorflow as tf
from anndata import AnnData
from pandas.api.types import infer_dtype

from scaae import utilities

_DATA_SET_LOADERS = {}
_DELIMITERS = {".csv": ",", ".tsv": r"\s+"}
_CATEGORICAL_NAME_PATTERNS = [
    r"categor(?:y|ies)", r"clusters?", r"class(?:es)", r"groups?"]


def read(path, layer=None):

    raw_path = path
    path = utilities.check_path(path)
    load_data_set = _DATA_SET_LOADERS.get(raw_path)

    if path.exists():
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore", category=FutureWarning, module="anndata")
            data_set = scanpy.read(path)
    elif load_data_set:
        data_set = load_data_set()
    else:
        raise Exception(f"`{raw_path}` not found.")

    if layer:
        data_set.layers["X"] = data_set.X
        data_set.X = data_set.layers[layer].astype(float)

    return data_set


def read_latent_representation(path):
    path = utilities.check_path(path)
    latent_representation = scanpy.read(path)
    return latent_representation


def read_annotations(path):
    path = utilities.check_path(path)
    delimiter = _DELIMITERS.get(path.suffixes[0])
    annotations = pd.read_csv(
        path, delimiter=delimiter, index_col=0)
    annotations = annotations.apply(_infer_categorical_data)
    return annotations


def _register_data_set_loader(name):
    def decorator(function):
        _DATA_SET_LOADERS[name] = function
        return function
    return decorator


@_register_data_set_loader("development")
def _load_development_set():
    return _create_development_set(
        sample_size=1000,
        feature_size=25,
        category_count=5
    )


def _create_development_set(sample_size, feature_size, category_count):
    data_set = scanpy.datasets.blobs(
        n_variables=feature_size,
        n_centers=category_count,
        n_observations=sample_size
    )
    blobs = data_set.obs.pop("blobs").astype("category")
    categories = _create_unique_ids(size=len(blobs.cat.categories))
    data_set.obs["blob"] = blobs.cat.rename_categories(categories)
    import numpy as np
    data_set.obs["batch"] = pd.Series(
        np.random.randint(0, 3, data_set.n_obs),
        index=data_set.obs_names).astype("category")
    return data_set


def _create_unique_ids(size, pool=None, ids=None):
    if pool is None:
        pool = uppercase_letters
    pool = list(pool)

    if ids is None:
        ids = pool

    if len(ids) >= size:
        return ids[:size]
    else:
        ids = ["".join(id) for id in itertools.product(ids, pool)]
        return _create_unique_ids(size=size, ids=ids, pool=pool)


@_register_data_set_loader("mnist_training")
def _load_mnist_training_set():
    return _load_mnist_dataset("training")


@_register_data_set_loader("mnist_test")
def _load_mnist_test_set():
    return _load_mnist_dataset("test")


def _load_mnist_dataset(subset_name):
    subsets = tf.keras.datasets.mnist.load_data()
    if subset_name == "training":
        subset = subsets[0]
    elif subset_name == "test":
        subset = subsets[1]
    else:
        raise ValueError(f"Subset `{subset_name}` not found.")
    samples, labels = subset
    samples = samples.reshape(samples.shape[0], -1)
    sample_size, feature_size = samples.shape
    sample_names = [f"image {i + 1}" for i in range(sample_size)]
    sample_annotations = pd.DataFrame(
        {"digit": labels}, index=sample_names).astype("category")
    feature_names = [f"pixel {i + 1}" for i in range(feature_size)]
    feature_annotations = pd.DataFrame(index=feature_names)
    metadata = {
        "minimum": 0,
        "maximum": 255}
    data_set = AnnData(
        samples, obs=sample_annotations, var=feature_annotations, uns=metadata)
    return data_set


def _infer_categorical_data(series):
    is_string = infer_dtype(series) in ["string"]
    is_integer = infer_dtype(series) in ["integer"]
    is_categorical_name = any(
        re.search(pattern, series.name.lower())
        for pattern in _CATEGORICAL_NAME_PATTERNS) if series.name else False
    if is_string or (is_integer and is_categorical_name):
        try:
            categorical_series = utilities.as_categorical_series(
                series, check_uniqueness=True)
            series = categorical_series
        except utilities.AllValuesUniqueError:
            pass
    return series
