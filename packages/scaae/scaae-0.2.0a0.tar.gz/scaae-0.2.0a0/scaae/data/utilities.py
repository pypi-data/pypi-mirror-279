import re

import numpy as np
import pandas as pd
import scipy.sparse as sps
from anndata import AnnData

from scaae import utilities

LATENT_NAME = "latent"
LATENT_REPRESENTATION_KEY = f"X_{LATENT_NAME}"
LATENT_MODEL_GROUP_KEY = f"{LATENT_NAME}_model_category"
LATENT_ANNOTATION_KEY_PREFIX = LATENT_NAME
ANNOTATION_KINDS = ["obs", "obsm", "obsp", "var", "varm", "varp", "uns"]
_ONTOLOGY_TERM_ID_SUFFIX = "_ontology_term_id"


def add_latent_representation_to_data_set(latent_representation,
                                          data_set,
                                          add_annotations=False,
                                          latent_categories=None):
    remove_latent_values_from_data_set(data_set)
    if isinstance(latent_representation, AnnData):
        latent_values = latent_representation.X
    else:
        latent_values = latent_representation
    data_set.obsm[LATENT_REPRESENTATION_KEY] = latent_values
    if add_annotations:
        copy_annotations(latent_representation, data_set, prefix="latent")
    if latent_categories is not None:
        latent_categories = utilities.as_categorical_series(
            latent_categories, index=data_set.obs_names)
        data_set.obs[LATENT_MODEL_GROUP_KEY] = latent_categories


def remove_latent_values_from_data_set(data_set):
    def only_latent_keys(keys):
        return [key for key in keys if any([
            key.startswith("latent_"), key.startswith(
                LATENT_REPRESENTATION_KEY)])]
    latent_patterns = [
        f"^{LATENT_NAME}.*", f"^{LATENT_REPRESENTATION_KEY}.*"]
    for latent_pattern in latent_patterns:
        remove_annotations_from_data_set(data_set, pattern=latent_pattern)


def remove_annotations_from_data_set(data_set, pattern=r".*",
                                     ignore_case=False):
    match_flags = 0
    if ignore_case:
        match_flags = re.IGNORECASE

    def keys_to_remove(keys):
        return [
            key for key in keys
            if re.fullmatch(pattern, key, flags=match_flags)]

    for key in keys_to_remove(data_set.obs_keys()):
        data_set.obs.pop(key)

    for key in keys_to_remove(data_set.obsm_keys()):
        data_set.obsm.pop(key)

    for key in keys_to_remove(data_set.obsp.keys()):
        data_set.obsp.pop(key)

    for key in keys_to_remove(data_set.obs_keys()):
        data_set.var.pop(key)

    for key in keys_to_remove(data_set.varm_keys()):
        data_set.varm.pop(key)

    for key in keys_to_remove(data_set.varp.keys()):
        data_set.varp.pop(key)

    for key in keys_to_remove(data_set.uns_keys()):
        data_set.uns.pop(key)


def data_set_difference(data_set, other_data_set,
                        skip_checking_data_matrices=True):
    difference_data_set = data_set.copy()

    if skip_checking_data_matrices or (data_set.X == other_data_set.X).all():
        difference_data_set.X = None

    for annotation_kind in ANNOTATION_KINDS:
        other_annotations = getattr(other_data_set, annotation_kind)
        for key in other_annotations.keys():
            difference_annotations = getattr(
                difference_data_set, annotation_kind)
            if key in difference_annotations.keys() and _annotations_are_equal(
                    difference_annotations[key], other_annotations[key]):
                difference_annotations.pop(key)

    return difference_data_set


def _annotations_are_equal(annotation, other_annotation):
    try:
        comparison = annotation == other_annotation
        if sps.issparse(comparison):
            is_equal = comparison.sum() == np.prod(comparison.shape)
        elif isinstance(comparison, (np.ndarray, pd.Series, pd.DataFrame)):
            is_equal = comparison.all()
        else:
            is_equal = comparison
    except TypeError as error:
        if str(error).startswith("Categoricals"):
            is_equal = False
        else:
            raise error
    return is_equal


def latent_data_set_from_data_set(data_set):
    _check_data_set_for_latent_representation(data_set)

    latent_values = data_set.obsm[LATENT_REPRESENTATION_KEY]
    observation_annotations = pd.DataFrame(index=data_set.obs_names)
    variable_names = [
        f"latent unit {i + 1}" for i in range(latent_values.shape[1])]
    variable_annotations = pd.DataFrame(index=variable_names)
    latent_data_set = AnnData(
        latent_values, obs=observation_annotations, var=variable_annotations)

    for key in data_set.obs_keys():
        if key.startswith("latent_"):
            latent_key = utilities.remove_prefix(key, prefix="latent_")
            latent_data_set.obs[latent_key] = data_set.obs[key]
    for key in data_set.obsm_keys():
        if key.startswith("latent_"):
            latent_key = utilities.remove_prefix(key, prefix="latent_")
            latent_data_set.obsm[latent_key] = data_set.obsm[key]
        elif key.startswith(f"{LATENT_REPRESENTATION_KEY}_"):
            latent_key = utilities.remove_prefix(
                key, prefix=f"{LATENT_REPRESENTATION_KEY}_")
            latent_key = f"X_{latent_key}"
            latent_data_set.obsm[latent_key] = data_set.obsm[key]
    for key in data_set.obsp.keys():
        if key.startswith("latent_"):
            latent_key = utilities.remove_prefix(key, prefix="latent_")
            latent_data_set.obsp[latent_key] = data_set.obsp[key]
    for key, value in data_set.uns.items():
        if key.startswith("latent_"):
            latent_key = utilities.remove_prefix(key, prefix="latent_")
            if isinstance(value, dict):
                latent_value = value.copy()
                for latent_subkey, latent_subvalue in latent_value.items():
                    if (isinstance(latent_subkey, str) and
                            latent_subkey.endswith("_key") and
                            isinstance(latent_subvalue, str) and
                            latent_subvalue.startswith("latent_")):
                        latent_value[latent_subkey] = utilities.remove_prefix(
                            latent_subvalue, prefix="latent_")
                if latent_value != value:
                    value = latent_value
            latent_data_set.uns[latent_key] = value

    return latent_data_set


def add_observation_annotations_to_data_set(data_set, annotations):
    data_set.obs = data_set.obs.join(annotations, how="left")


def copy_annotations(source_data_set, target_data_set, prefix=None):
    prefix = utilities.ensure_suffix(prefix, "_") if prefix else ""
    for source_key in source_data_set.obs_keys():
        target_key = f"{prefix}{source_key}"
        target_data_set.obs[target_key] = source_data_set.obs[source_key]
    for source_key in source_data_set.obsm_keys():
        if source_key.startswith("X_"):
            target_key = utilities.remove_prefix(source_key, prefix="X_")
            target_key = f"X_{prefix}{target_key}"
        else:
            target_key = f"{prefix}{source_key}"
        target_data_set.obsm[target_key] = source_data_set.obsm[source_key]
    for source_key in source_data_set.obsp.keys():
        target_key = f"{prefix}{source_key}"
        target_data_set.obsp[target_key] = source_data_set.obsp[source_key]
    for source_key, source_value in source_data_set.uns.items():
        target_key = f"{prefix}{source_key}"
        if isinstance(source_value, dict):
            value = source_value.copy()
            for subkey, subvalue in value.items():
                if isinstance(subkey, str) and subkey.endswith("_key"):
                    value[subkey] = f"{prefix}{subvalue}"
            if value != source_value:
                source_value = value
        target_data_set.uns[target_key] = source_value


def has_latent_representation(data_set):
    return LATENT_REPRESENTATION_KEY in data_set.obsm_keys()


def latent_representation_size(data_set):
    _check_data_set_for_latent_representation(data_set)
    return data_set.obsm[LATENT_REPRESENTATION_KEY].shape[1]


def filter_annotation_keys(annotations, keys=None,
                           keep_categorical=None, keep_numerical=None,
                           remove_redundant_keys=True,
                           categorical_criterion="multiple_or_latent"):
    if keys is None:
        keys = annotations.columns

    kept_keys = []

    for key in keys:
        if (remove_redundant_keys and key.endswith(_ONTOLOGY_TERM_ID_SUFFIX)
                and utilities.remove_suffix(
                    key, _ONTOLOGY_TERM_ID_SUFFIX) in annotations):
            continue

        if keep_categorical is not None or keep_numerical is not None:
            annotation = annotations.get(key)

            if annotation is None:
                raise RuntimeError(f"`{key}` not in `annotations`.")

            if keep_categorical is True and _is_truly_categorical(
                    annotation, criterion=categorical_criterion):
                pass
            elif keep_categorical is False and _is_categorical_or_boolean(
                    annotation):
                continue
            elif keep_numerical is True and _is_numeric(annotation):
                pass
            elif keep_numerical is False and _is_numeric(annotation):
                continue
            else:
                continue

        kept_keys.append(key)

    return kept_keys


def _is_categorical_or_boolean(series):
    return (
        isinstance(series.dtype, pd.CategoricalDtype)
        or pd.api.types.is_bool_dtype(series))


def _is_truly_categorical(series, criterion=None):
    is_truly_categorical = False
    if _is_categorical_or_boolean(series):
        if criterion is None:
            is_truly_categorical = True
        elif criterion == "multiple":
            is_truly_categorical = _has_multiple_categories(series)
        elif criterion == "multiple_or_latent":
            is_truly_categorical = (
                _has_multiple_categories(series)
                or series.name.startswith(LATENT_ANNOTATION_KEY_PREFIX))
        else:
            raise ValueError("Categorical criterion `{criterion}` unknown.")
    return is_truly_categorical


def _has_multiple_categories(series, less_than_size=True):
    has_multiple_categories = False
    if _is_categorical_or_boolean(series):
        series = series.astype("category")
        category_count = len(series.cat.categories)
        if 1 < category_count and (
                less_than_size and category_count < series.size
                or not less_than_size):
            has_multiple_categories = True
    return has_multiple_categories


def _is_numeric(series):
    return (
        pd.api.types.is_numeric_dtype(series)
        and not pd.api.types.is_bool_dtype(series))


def plottable_annotation_keys(annotations, keys=None,
                              match_patterns=None, ignore_patterns=None):
    if keys is None:
        keys = annotations.columns
    if match_patterns or ignore_patterns:
        keys = utilities.filter_texts(
            keys,
            match_patterns=match_patterns, ignore_patterns=ignore_patterns)
    keys = filter_annotation_keys(
        annotations, keys=keys,
        keep_categorical=True, keep_numerical=True,
        remove_redundant_keys=True)
    if len(keys) == 0:
        keys = None
    return keys


def categorical_annotation_keys(annotations, keys=None, latent_only=False,
                                match_patterns=None, ignore_patterns=None):
    if keys is None:
        keys = annotations.columns

    if latent_only and (match_patterns or ignore_patterns):
        raise RuntimeError(
            "Cannot keep latent annotations only when patterns are provided.")
    elif latent_only:
        keys = latent_keys(keys)
    elif match_patterns or ignore_patterns:
        keys = utilities.filter_texts(
            keys,
            match_patterns=match_patterns, ignore_patterns=ignore_patterns)

    keys = filter_annotation_keys(
        annotations, keys=keys,
        keep_categorical=True, keep_numerical=False,
        remove_redundant_keys=True)

    if len(keys) == 0:
        keys = None

    return keys


def latent_keys(keys):
    return [key for key in keys if key.startswith(
        LATENT_ANNOTATION_KEY_PREFIX)]


def _check_data_set_for_latent_representation(data_set):
    if LATENT_REPRESENTATION_KEY not in data_set.obsm_keys():
        raise ValueError(
            "Latent representation not found for data set. "
            "Data set has to be encoded beforehand.")


def as_dense_array(array, memory_limit_in_gigabytes=None):
    if sps.issparse(array):
        array_size_in_bytes = np.prod(array.shape) * array.dtype.itemsize
        if utilities.allow_memory_usage(
                array_size_in_bytes,
                memory_limit_in_gigabytes=memory_limit_in_gigabytes):
            array = array.A
    else:
        array = array
    return array


def get_representation(data_set, key=None):
    data_set_object, key = _find_representation(data_set=data_set, key=key)
    if hasattr(data_set_object, key):
        representation = getattr(data_set_object, key)
    elif hasattr(data_set_object, "get"):
        representation = data_set_object[key]
    else:
        raise NotImplementedError
    return representation


def set_representation(data_set, representation, key=None):
    data_set_object, key = _find_representation(data_set=data_set, key=key)
    if hasattr(data_set_object, key):
        setattr(data_set_object, key, representation)
    elif hasattr(data_set_object, "get"):
        data_set_object[key] = representation
    else:
        raise NotImplementedError


def transform_representation(data_set, function, key=None):
    representation = get_representation(data_set=data_set, key=key)
    transformed_representation = function(representation)
    set_representation(
        data_set=data_set, representation=transformed_representation, key=key)


def _find_representation(data_set, key=None):
    if key:
        obsm_key = utilities.ensure_prefix(key, prefix="X_")
        if key in data_set.layers:
            data_set_object = data_set.layers
        elif obsm_key in data_set.obsm:
            data_set_object = data_set.obsm
            key = obsm_key
        else:
            raise ValueError(
                f"Representation `{key}` not found.")
    else:
        data_set_object = data_set
        key = "X"
    return data_set_object, key
