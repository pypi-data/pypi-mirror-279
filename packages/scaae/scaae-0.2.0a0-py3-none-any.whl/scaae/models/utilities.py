import json
from pathlib import Path

from scaae.utilities import check_path, check_dict, save_as_json


def save_model_config(config, path, replace=True):
    config = check_dict(config)
    path = check_path(path)
    save_as_json(config, path=path, replace=replace)


def load_model_config(config_or_path=None, data_interval=None,
                      model_kind=None, feature_size=None, **kwargs):

    config = _load_config(config_or_path)

    if model_kind:
        configured_model_kind = config.get("feature_size")

        if configured_model_kind and configured_model_kind != model_kind:
            raise ValueError(
                f"The model kind (`{model_kind}`) differs from the kind "
                f"specified for the model (`{configured_model_kind}`).")
        else:
            config["model_kind"] = model_kind

    if feature_size:
        configured_feature_size = config.get("feature_size")

        if configured_feature_size and configured_feature_size != feature_size:
            raise ValueError(
                f"The feature size of the data set ({feature_size}) differs "
                "from the feature size specified for the model "
                f"({configured_feature_size}).")
        else:
            config["feature_size"] = feature_size

    for argument_name, argument_value in kwargs.items():
        if argument_value:
            config[argument_name] = argument_value

    if data_interval == "unit":
        autoencoder_distribution = config.get("autoencoder_distribution")
        if autoencoder_distribution is None:
            config.setdefault("autoencoder_activation", "sigmoid")

    return config


def load_optimisation_config(config_or_path=None, **kwargs):

    config = _load_config(config_or_path)

    for argument_name, argument_value in kwargs.items():
        if argument_value:
            config[argument_name] = argument_value

    return config


def _load_config(config_or_path=None):

    if isinstance(config_or_path, (Path, str)):
        path = check_path(config_or_path)
        config = json.loads(path.read_text())
    else:
        config = config_or_path

    config = check_dict(config)

    return config


def configure_optimiser(optimiser,
                        learning_rate=None,
                        decay=None,
                        clipnorm=None,
                        clipvalue=None,
                        distribution_modelling=False,
                        distribution_clipnorm=None):

    if distribution_modelling and clipnorm is None and clipvalue is None:
        clipnorm = distribution_clipnorm

    optimiser = adjust_optimiser(
        optimiser=optimiser,
        learning_rate=learning_rate,
        decay=decay,
        clipnorm=clipnorm,
        clipvalue=clipvalue)

    return optimiser


def adjust_optimiser(optimiser, **kwargs):

    if isinstance(optimiser, str):
        optimiser = {"class_name": optimiser, "config": {}}

    if isinstance(optimiser, dict):
        _check_optimiser_configuration_dictionary(optimiser)
        config = optimiser.get("config", {})

        for argument_name, argument_value in kwargs.items():
            if argument_name not in config and argument_value is not None:
                config[argument_name] = argument_value

    return optimiser


def _check_optimiser_configuration_dictionary(dictionary):
    for key in ["class_name", "config"]:
        if key not in dictionary:
            raise KeyError(
                f"Key `{key}` not provided in "
                "optimiser configuration_dictionary")
