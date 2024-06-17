import importlib
import itertools
import warnings
from enum import Enum
from functools import lru_cache

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
import scanpy
import scipy.optimize as spo
import sklearn.decomposition as skld
import sklearn.metrics as sklm
import sklearn.utils as sklu
import sklearn.utils.multiclass as sklum
from matplotlib import pyplot as plt, patches as mpatches
from pandas.api.types import is_categorical_dtype

from scaae import utilities
from scaae.data import utilities as data_utilities
from scaae.models import VALIDATION_METRIC_PREFIX

ORIGINAL_GROUPING_NAME = "original_grouping"
LATENT_GROUPING_NAME = "latent_grouping"
ORIGINAL_MAIN_GROUPING_GUESSING_PATTERNS = [r"cell[_-]?types?"]
CLUSTERING_METRICS = {}
CLUSTERING_DEFAULTS = {}
LATENT_CLUSTERERS = {}
LATENT_DECOMPOSERS = {}
_METRIC_SUPPORTS = {
    "discriminator_accuracy": (0, 1),
    "generator_accuracy": (0, 1)}
_SCANPY_DEFAULT_NEIGHBORS_KEY = "neighbors"
_ORIGINAL_ANNOTATION_KEY_SUFFIX = "-original_before_fixing_for_scaae"

_RAPIDS_CHUNK_SIZE = 16_000


class BestDirection(Enum):
    POSITIVE = 1
    NEGATIVE = -1


class Preparation(Enum):
    PAIRWISE_DISTANCES = 1
    DENSE_FORMAT = 2


_SORT_ASCENDING = {
    BestDirection.POSITIVE: False,
    BestDirection.NEGATIVE: True}


def cluster_latent_representation(data_set, method="louvain",
                                  resolution=None, neighbourhood_size=None,
                                  principal_component_count=None):
    cluster = LATENT_CLUSTERERS.get(method)
    if not cluster:
        raise ValueError(f"Method `{method}` not found.")
    cluster(
        data_set,
        resolution=resolution,
        n_neighbors=neighbourhood_size,
        n_pcs=principal_component_count)


def cluster_latent_representation_with_configs(data_set, *configs,
                                               enable_progress_bar=False):
    for config in utilities.ProgressBar(
            configs, total=len(configs),
            unit="clustering", unit_plural="clusterings",
            disable=not enable_progress_bar):
        cluster_latent_representation(data_set, **config)


def clustering_configs(methods, resolutions=None, neighbourhood_sizes=None,
                       principal_component_counts=None):
    methods = utilities.check_list(methods)
    resolutions = utilities.check_list(resolutions, wrap_none=True)
    neighbourhood_sizes = utilities.check_list(
        neighbourhood_sizes, wrap_none=True)
    principal_component_counts = utilities.check_list(
        principal_component_counts, wrap_none=True)

    if len(methods) == 0:
        raise ValueError(
            "No clustering method(s) specified for clustering latent space.")

    configs = []
    for method, neighbourhood_size, principal_component_count, resolution in (
            itertools.product(methods, neighbourhood_sizes,
                              principal_component_counts, resolutions)):
        configs.append({
            "method": method,
            "resolution": resolution,
            "neighbourhood_size": neighbourhood_size,
            "principal_component_count": principal_component_count})

    return configs


def evaluate_clusterings(data_set, metric_names=None,
                         ground_truth_annotation_key_match_patterns=None,
                         ground_truth_annotation_key_ignore_patterns=None,
                         sort_keys=None,
                         distance_metric="euclidean",
                         enable_progress_bar=False):
    latent_grouping_keys = data_utilities.categorical_annotation_keys(
        data_set.obs, latent_only=True)
    original_grouping_keys = data_utilities.categorical_annotation_keys(
        data_set.obs,
        match_patterns=ground_truth_annotation_key_match_patterns,
        ignore_patterns=ground_truth_annotation_key_ignore_patterns)
    original_grouping_keys = [
        key for key in original_grouping_keys
        if key not in latent_grouping_keys]

    supervised_metrics = []
    supervised_metric_names = clustering_metric_names(
        metric_names, supervised=True)
    for metric_name in supervised_metric_names:
        supervised_metric_column = []
        key_pairs = list(itertools.product(
            original_grouping_keys, latent_grouping_keys))
        for original_key, latent_key in utilities.ProgressBar(
                key_pairs, desc=metric_name,
                unit="evaluation", unit_plural="evalutaions",
                disable=not enable_progress_bar):
            supervised_metrics_row = {
                ORIGINAL_GROUPING_NAME: original_key,
                LATENT_GROUPING_NAME: latent_key}
            supervised_metrics_row[metric_name] = compare_groupings(
                original_grouping=data_set.obs[original_key],
                other_grouping=data_set.obs[latent_key],
                metric=metric_name)
            supervised_metric_column.append(supervised_metrics_row)
        supervised_metric_column = pd.DataFrame(
            supervised_metric_column).set_index([
                ORIGINAL_GROUPING_NAME, LATENT_GROUPING_NAME])
        supervised_metrics.append(supervised_metric_column)
    supervised_metrics = pd.concat(
        supervised_metrics, axis="columns").dropna(axis="columns", how="all")

    unsupervised_metrics = []
    representation, distance_metric = (
        pairwise_distances_otherwise_representation(
            data_set, distance_metric=distance_metric))
    unsupervised_metric_names = clustering_metric_names(
        metric_names, supervised=False)
    for metric_name in unsupervised_metric_names:
        unsupervised_metric_column = []
        for latent_key in utilities.ProgressBar(
                latent_grouping_keys, desc=metric_name,
                unit="evaluation", unit_plural="evalutaions",
                disable=not enable_progress_bar):
            unsupervised_metrics_row = {LATENT_GROUPING_NAME: latent_key}
            unsupervised_metrics_row[metric_name] = (
                evaluate_grouping_on_representation(
                    representation=representation,
                    grouping=data_set.obs[latent_key],
                    metric=metric_name,
                    distance_metric=distance_metric))
            unsupervised_metric_column.append(unsupervised_metrics_row)
        unsupervised_metric_column = pd.DataFrame(
            unsupervised_metric_column).set_index(LATENT_GROUPING_NAME)
        unsupervised_metrics.append(unsupervised_metric_column)
    unsupervised_metrics = pd.concat(
        unsupervised_metrics, axis="columns").dropna(axis="columns", how="all")

    sort_keys = sort_keys or CLUSTERING_DEFAULTS.get(
        "sort_keys")
    if sort_keys:
        sort_keys = sort_keys.copy()
        sort_keys.insert(0, ORIGINAL_GROUPING_NAME)
        supervised_metrics = _sort_clustering_metrics(
            supervised_metrics, sort_keys)
        unsupervised_metrics = _sort_clustering_metrics(
            unsupervised_metrics, sort_keys)

    return {
        "supervised": supervised_metrics,
        "unsupervised": unsupervised_metrics}


def pairwise_distances_otherwise_representation(data_set,
                                                representation_key=None,
                                                distance_metric="euclidean"):
    distance_key = _distance_key(
        representation_key=representation_key, distance_metric=distance_metric)
    if distance_key in data_set.obsp:
        representation = data_set.obsp[distance_key]
        distance_metric = "precomputed"
    else:
        representation = data_utilities.get_representation(
            data_set, key=representation_key)
    return representation, distance_metric


def _sort_clustering_metrics(metrics, sort_keys):
    sort_keys = list(filter(
        lambda k: k in metrics.columns or k in metrics.index.names,
        sort_keys))
    if sort_keys:
        sort_ascending = [
            _SORT_ASCENDING.get(
                CLUSTERING_METRICS.get(key, {}).get("best_direction"), True)
            for key in sort_keys]
        metrics = metrics.sort_values(
            by=sort_keys, ascending=sort_ascending)
    return metrics


def compare_groupings(original_grouping, other_grouping, metric):
    metric_function = clustering_metric_attribute(
        metric, "function", needs_attribute=False)
    if callable(metric):
        metric_function = metric
    if not metric_function:
        raise ValueError(f"Clustering metric \"{metric}\" not supported.")
    try:
        unknown_original_group_indices = original_grouping.isna()
        metric_value = metric_function(
            original_grouping[~unknown_original_group_indices],
            other_grouping[~unknown_original_group_indices])
    except ValueError:
        metric_value = np.nan
    return metric_value


def evaluate_grouping_on_representation(representation, grouping, metric,
                                        distance_metric="euclidean"):
    metric_function = clustering_metric_attribute(
        metric, "function", needs_attribute=False)
    if callable(metric):
        metric_function = metric
    if not metric_function:
        raise ValueError(f"Clustering metric \"{metric}\" not supported.")
    metric_value = metric_function(
        representation, grouping, distance_metric=distance_metric)
    return metric_value


def limit_latent_clustering_annotation_keys(annotation_keys, limit,
                                            clustering_metric_sets,
                                            clustering_sort_keys=None,
                                            additional_keys=None,
                                            include_median=True):

    clustering_metric_sets = utilities.check_list(
        clustering_metric_sets, use_dictionary_values=True)

    clustering_sort_keys = (
        clustering_sort_keys or CLUSTERING_DEFAULTS.get("sort_keys"))
    if clustering_sort_keys is None:
        raise ValueError("No clustering sorting keys specified.")
    additional_keys = utilities.check_list(additional_keys)

    latent_keys = data_utilities.latent_keys(annotation_keys)
    limited_annotation_keys = set(
        key for key in annotation_keys if key not in latent_keys)
    if additional_keys:
        limited_annotation_keys.update(additional_keys)

    def _update_limited_annotation_keys(clustering_metrics,
                                        clustering_sort_key):
        clustering_metric = clustering_metrics.reset_index(
            ).set_index(LATENT_GROUPING_NAME)[clustering_sort_key]
        sort_ascending = _SORT_ASCENDING[clustering_metric_attribute(
            clustering_metric.name, "best_direction")]
        sorted_clustering_metric = clustering_metric.sort_values(
            ascending=sort_ascending)
        limited_latent_annotation_key_subset = set(
            sorted_clustering_metric.index[:limit])
        if include_median:
            nearest_to_median = sorted_clustering_metric.quantile(
                0.5, interpolation="nearest")
            median_indices = sorted_clustering_metric[
                sorted_clustering_metric == nearest_to_median].index
            limited_latent_annotation_key_subset.update(median_indices)
        limited_latent_annotation_key_subset = (
            limited_latent_annotation_key_subset.intersection(latent_keys))
        limited_annotation_keys.update(limited_latent_annotation_key_subset)

    for clustering_sort_key in clustering_sort_keys:
        for clustering_metric_set in clustering_metric_sets:
            if clustering_sort_key in clustering_metric_set.columns:
                if ORIGINAL_GROUPING_NAME in clustering_metric_set.index.names:
                    for original_key, clustering_metric_subset in (
                            clustering_metric_set.groupby(
                                level=ORIGINAL_GROUPING_NAME)):
                        _update_limited_annotation_keys(
                            clustering_metric_subset, clustering_sort_key)
                else:
                    _update_limited_annotation_keys(
                        clustering_metric_set, clustering_sort_key)

    return sorted(limited_annotation_keys)


def decompose_latent_representation(data_set, method="pca"):
    decompose = LATENT_DECOMPOSERS.get(method)
    if not decompose:
        raise ValueError(f"Method `{method}` not found.")
    decompose(data_set)


def plot_latent_representation(data_set, annotation_keys=None,
                               decomposition_method=None,
                               path=None):
    if path:
        path = utilities.check_path(path)
    basis = "X_latent"
    if decomposition_method:
        basis = f"{basis}_{decomposition_method}"
        if basis not in data_set.obsm_keys():
            decompose_latent_representation(
                data_set, method=decomposition_method)
    _fix_annotations(annotation_keys, data_set)
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore", message="No data for colormapping provided.+",
            category=UserWarning, module="scanpy")
        warnings.filterwarnings(
            "ignore", category=FutureWarning, module="scanpy")
        figure = scanpy.pl.embedding(
            data_set, basis, color=annotation_keys, legend_loc="right margin",
            return_fig=path is not None)
    _restore_original_annotations(data_set)
    if path:
        figure.savefig(
            path, bbox_inches="tight", bbox_extra_artists=(
                figure.legends + [
                    axis.get_legend()
                    for axis in figure.axes if axis.get_legend()]))
        plt.close(figure)


def _fix_annotations(annotation_keys, data_set):
    annotation_keys = utilities.check_list(annotation_keys)
    for annotation_key in annotation_keys:
        annotation = data_set.obs[annotation_key]
        original_annotation_key = (
            f"{annotation_key}{_ORIGINAL_ANNOTATION_KEY_SUFFIX}")
        data_set.obs[original_annotation_key] = annotation
        if (not isinstance(annotation.dtype, pd.CategoricalDtype)
                and np.issubdtype(annotation, bool)):
            annotation = annotation.astype("category")
        data_set.obs[annotation_key] = annotation


def _restore_original_annotations(data_set):
    annotation_keys = [
        annotation_key for annotation_key in data_set.obs_keys()
        if annotation_key.endswith(_ORIGINAL_ANNOTATION_KEY_SUFFIX)]
    for annotation_key in annotation_keys:
        original_annotation_key = utilities.remove_suffix(
            annotation_key, _ORIGINAL_ANNOTATION_KEY_SUFFIX)
        data_set.obs[original_annotation_key] = data_set.obs[annotation_key]
        data_set.obs.pop(annotation_key)


def plot_clusterings_in_sankey_diagram(data_set, clustering_annotation_keys,
                                       path=None):
    if path:
        path = utilities.check_path(path)

    clustering_connections, cluster_info = _clustering_connections(
        data_set, clustering_annotation_keys)

    cluster_ids = cluster_info.reset_index().set_index("full_name")["index"]
    figure = go.Figure()
    figure.add_trace(go.Sankey(
        node={
            "label": cluster_info["short_name"],
            "color": cluster_info["colour"].apply(_plotly_colour)},
        link={
            "source": clustering_connections["source"].map(cluster_ids),
            "target": clustering_connections["target"].map(cluster_ids),
            "value": clustering_connections["count"]}))
    clustering_count = len(clustering_annotation_keys)
    x_ticks = np.arange(clustering_count)
    figure.add_trace(go.Scatter(x=x_ticks, y=[None] * clustering_count))
    figure.update_xaxes(side="top")
    figure.update_layout(
        autosize=False,
        width=800,
        height=800,
        plot_bgcolor="white",
        xaxis={
            "showgrid": False,
            "tickmode": "array",
            "tickvals": x_ticks,
            "ticktext": clustering_annotation_keys},
        yaxis={
            "showgrid": False,
            "showticklabels": False})
    if path:
        figure.write_image(path)


def _clustering_connections(data_set, clustering_annotation_keys):
    clusterings = {}
    cluster_info = []
    for clustering_index, clustering_annotation_key in enumerate(
            clustering_annotation_keys):
        clustering_column = data_set.obs[clustering_annotation_key]
        clustering_palette = sns.cubehelix_palette(
            n_colors=len(clustering_column.cat.categories),
            start=clustering_index / len(clustering_annotation_keys) * 3)
        cluster_name_mapping = {}
        for cluster_index, cluster_name in enumerate(
                clustering_column.cat.categories):
            full_cluster_name = f"{clustering_annotation_key}_{cluster_name}"
            cluster_name_mapping[cluster_name] = full_cluster_name
            cluster_info.append({
                "full_name": full_cluster_name,
                "short_name": cluster_name,
                "colour": clustering_palette[cluster_index]})
        clusterings[clustering_annotation_key] = (
            clustering_column.cat.rename_categories(cluster_name_mapping))
    clusterings = pd.DataFrame(clusterings)
    cluster_info = pd.DataFrame(cluster_info)
    counts = pd.concat([
        clusterings.groupby(list(pair)).size().rename("count").rename_axis(
            index={pair[0]: "source", pair[1]: "target"})
        for pair in _sequential_pairs(clusterings.columns)])
    clustering_connections = counts[counts != 0].reset_index()
    return clustering_connections, cluster_info


def _sequential_pairs(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def _plotly_colour(components):
    components = (255 * np.array(components)).astype(int)
    return "rgb({}, {}, {})".format(*components)


def plot_learning_curves(learning_curves,
                         metric_groups=None,
                         use_metric_support_for_plot_limits=False,
                         validation_prefix=VALIDATION_METRIC_PREFIX,
                         path=None):
    if path:
        path = utilities.check_path(path)

    if metric_groups is None:
        metric_groups = [
            metric_name for metric_name in learning_curves
            if not metric_name.startswith(validation_prefix)]
    metric_groups.extend(_clustering_metric_groups())
    metric_groups = _filter_metric_groups(
        metric_groups, valid_metric_names={
            utilities.remove_prefix(metric_name, validation_prefix)
            for metric_name in learning_curves.columns})

    figure, axes = plt.subplots(
        nrows=len(metric_groups), sharex=True, tight_layout=True,
        figsize=(8, 2.5 * len(metric_groups)))

    property_cycle_cls = plt.rcParams.get("axes.prop_cycle")
    if property_cycle_cls:
        property_cycle = property_cycle_cls()

    for i, (metric_group, axis) in enumerate(zip(metric_groups, axes)):
        if not isinstance(metric_group, (list, tuple)):
            metric_group = [metric_group]
        for metric_name in metric_group:
            colour = next(property_cycle).get("color")
            if metric_name in learning_curves:
                axis.plot(
                    learning_curves.index + 1, learning_curves[metric_name],
                    color=colour, label=metric_name)
            validation_metric_name = f"{validation_prefix}{metric_name}"
            if validation_metric_name in learning_curves:
                axis.plot(
                    learning_curves.index + 1,
                    learning_curves[validation_metric_name],
                    color=colour,
                    linestyle="--",
                    label=validation_metric_name)
            metric_support = _metric_support(metric_name)
            if use_metric_support_for_plot_limits and metric_support:
                metric_minimum, metric_maximum = metric_support
                y_min, y_max = axis.get_ylim()
                y_min = metric_minimum if metric_minimum is not None else y_min
                y_max = metric_maximum if metric_maximum is not None else y_max
                axis.set_ylim(y_min, y_max)
            axis.legend(bbox_to_anchor=(1, 1), loc="upper left")

    if path is not None:
        figure.savefig(path)
        plt.close(figure)
    else:
        plt.show()


def _clustering_metric_groups():
    groups = {}
    separate_group_count = 0
    for metric_name, metric_specifications in CLUSTERING_METRICS.items():
        group_name = metric_specifications.get("support")
        if group_name is None:
            group_name = f"separate_group_{separate_group_count}"
            separate_group_count += 1
        groups.setdefault(group_name, []).append(metric_name)
    return list(groups.values())


def _metric_support(name):
    support = _METRIC_SUPPORTS.get(name)
    if support is None and name in CLUSTERING_METRICS:
        support = clustering_metric_attribute(
            name, "support", needs_attribute=False)
    return support


def _filter_metric_groups(metric_groups, valid_metric_names=None):
    valid_metric_names = utilities.check_set(valid_metric_names)
    filtered_metric_groups = []
    for metric_group in metric_groups:
        filtered_metric_group = [
            metric_name for metric_name in metric_group
            if metric_name in valid_metric_names]
        if filtered_metric_group:
            filtered_metric_groups.append(filtered_metric_group)
    return filtered_metric_groups


def plot_normal_mixture_components(coefficients, means, covariances,
                                   path=None):

    category_count = len(coefficients)

    pca = skld.PCA(n_components=2)
    means = pca.fit_transform(means)
    covariances = _pca_transform_covariances(covariances, pca_model=pca)

    figure, (components_plot, coefficients_plot) = plt.subplots(
        ncols=2, tight_layout=True, gridspec_kw={"width_ratios": [4, 1]})
    sns.despine()

    colours = sns.husl_palette(category_count, l=.55)

    for k in range(category_count):
        ellipse = _covariance_matrix_as_ellipse(
            covariances[k], means[k], colour=colours[k])
        components_plot.add_patch(ellipse)
        components_plot.autoscale()

    components_plot.set_xlabel("PC 1")
    components_plot.set_ylabel("PC 2")

    coefficients_plot.barh(
        np.arange(category_count), coefficients, color=colours)
    coefficients_plot.set_yticks([])
    coefficients_plot.set_xlabel("Probability")
    coefficients_plot.set_ylabel("Prior mixture component")

    if path is not None:
        figure.savefig(path)
        plt.close(figure)
    else:
        plt.show()


def _pca_transform_covariances(covariances, pca_model):
    covariance_count = covariances.shape[0]
    component_size = pca_model.n_components
    components = pca_model.components_
    transformed_covariances = np.empty(
        (covariance_count, component_size, component_size))
    for k in range(covariance_count):
        transformed_covariances[k] = components @ covariances[k] @ components.T
    return transformed_covariances


def _covariance_matrix_as_ellipse(covariance_matrix, mean, colour="black",
                                  standard_deviations=1):

    eigenvalues, eigenvectors = np.linalg.eig(covariance_matrix)
    indices_sorted_ascending = eigenvalues.argsort()[::-1]
    eigenvalues = eigenvalues[indices_sorted_ascending]
    eigenvectors = eigenvectors[:, indices_sorted_ascending]
    lambda_1, lambda_2 = np.sqrt(eigenvalues)

    width = 2 * standard_deviations * lambda_1
    height = 2 * standard_deviations * lambda_2
    angle = np.degrees(np.arctan2(eigenvectors[1, 0], eigenvectors[0, 0]))

    ellipse = mpatches.Ellipse(
        xy=mean,
        width=width,
        height=height,
        angle=angle,
        linewidth=2,
        linestyle="solid",
        facecolor="none",
        edgecolor=colour)

    return ellipse


def save_latent_representation(data_set, path):
    path = utilities.check_path(path)
    latent_data_set = data_utilities.latent_data_set_from_data_set(data_set)
    latent_data_set.write(path, compression="gzip")


def save_additional_latent_annotations(data_set, original_latent_data_set,
                                       path):
    path = utilities.check_path(path)
    latent_data_set = data_utilities.latent_data_set_from_data_set(data_set)
    additional_latent_annotations = data_utilities.data_set_difference(
        latent_data_set, original_latent_data_set)
    additional_latent_annotations.write(path, compression="gzip")


def prepare_for_clustering_metrics(data_set, metric_names=None,
                                   representation_key=None,
                                   dense_memory_limit_in_gigabytes=None):

    using_latent_representation = representation_key in [
        data_utilities.LATENT_NAME,
        data_utilities.LATENT_REPRESENTATION_KEY]

    pairwise_distances_clustering_metric_names = clustering_metric_names(
        metric_names, preparations=Preparation.PAIRWISE_DISTANCES)
    if (pairwise_distances_clustering_metric_names
            and not using_latent_representation):
        _maybe_compute_pairwise_distances(
            data_set, representation_key=representation_key,
            memory_limit_in_gigabytes=dense_memory_limit_in_gigabytes)

    dense_format_clustering_metric_names = clustering_metric_names(
        metric_names, preparations=Preparation.DENSE_FORMAT)
    if (dense_format_clustering_metric_names
            and not using_latent_representation):
        data_utilities.transform_representation(
            data_set,
            function=lambda array: data_utilities.as_dense_array(
                array,
                memory_limit_in_gigabytes=dense_memory_limit_in_gigabytes),
            key=representation_key)


def _maybe_compute_pairwise_distances(data_set, representation_key=None,
                                      distance_metric="euclidean",
                                      memory_limit_in_gigabytes=None):
    representation = data_utilities.get_representation(
        data_set, key=representation_key)
    distance_key = _distance_key(
        representation_key=representation_key, distance_metric=distance_metric)
    distance_matrix_size_in_bytes = (
        pow(representation.shape[0], 2) * representation.dtype.itemsize)
    if (distance_key not in data_set.obsp.keys()
            and utilities.allow_memory_usage(
                distance_matrix_size_in_bytes,
                memory_limit_in_gigabytes=memory_limit_in_gigabytes)):
        method = _use_rapids_if_available()
        if method and method == "rapids":
            import cuml
            distances = cuml.metrics.pairwise_distances(
                representation, metric=distance_metric)
        else:
            distances = sklm.pairwise_distances(
                representation, metric=distance_metric)
        data_set.obsp[distance_key] = distances


def _distance_key(representation_key=None, distance_metric=None):
    distance_key = "pairwise_distances"
    if representation_key:
        distance_key = f"{representation_key}_{distance_key}"
    if distance_metric:
        distance_key = f"{distance_metric}_{distance_key}"
    return distance_key


def _register_clusterer(name):
    def decorator(function):
        LATENT_CLUSTERERS[name] = function
        return function
    return decorator


@_register_clusterer("louvain")
def latent_louvain(data_set, resolution=None, n_neighbors=None, n_pcs=None,
                   **kwargs):
    latent_data_set = data_utilities.latent_data_set_from_data_set(data_set)
    neighbors_key = _maybe_compute_neighbors(
        latent_data_set, n_neighbors=n_neighbors, n_pcs=n_pcs)
    clustering_key = _clustering_key(
        "louvain", resolution=resolution, n_neighbors=n_neighbors, n_pcs=n_pcs)
    flavour = _use_rapids_if_available(
        dependencies=["cudf", "cugraph"], fallback="vtraag")
    if flavour == "rapids":
        _clustering_rapids(
            latent_data_set, algorithm="louvain", resolution=resolution,
            neighbors_key=neighbors_key, key_added=clustering_key, **kwargs)
    else:
        scanpy.tl.louvain(
            latent_data_set, resolution=resolution, flavor=flavour,
            neighbors_key=neighbors_key, key_added=clustering_key, **kwargs)
    data_utilities.copy_annotations(latent_data_set, data_set, prefix="latent")


@_register_clusterer("leiden")
def latent_leiden(data_set, resolution=None, n_neighbors=None, n_pcs=None,
                  **kwargs):
    latent_data_set = data_utilities.latent_data_set_from_data_set(data_set)
    neighbors_key = _maybe_compute_neighbors(
        latent_data_set, n_neighbors=n_neighbors, n_pcs=n_pcs)
    clustering_key = _clustering_key(
        "leiden", resolution=resolution, n_neighbors=n_neighbors, n_pcs=n_pcs)
    flavour = _use_rapids_if_available(
        dependencies=["cudf", "cugraph"], fallback="igraph")
    if flavour == "rapids":
        _clustering_rapids(
            latent_data_set, algorithm="leiden", resolution=resolution,
            neighbors_key=neighbors_key, key_added=clustering_key, **kwargs)
    else:
        scanpy.tl.leiden(
            latent_data_set, resolution=resolution, flavor=flavour,
            neighbors_key=neighbors_key, key_added=clustering_key, **kwargs)
    data_utilities.copy_annotations(latent_data_set, data_set, prefix="latent")


def _clustering_rapids(adata, algorithm, resolution=1.0, *,
                       key_added=None, adjacency=None,
                       use_weights=True, n_iterations=-1,
                       neighbors_key=None, obsp=None, copy=False,
                       **kwargs):
    """Cluster data set using Rapids's Leiden or Louvain implementation.

    Based on similar functions in ScanPy.
    """

    import pandas as pd
    from natsort import natsorted
    from scanpy._utils import _choose_graph

    algorithm = algorithm.lower()
    if key_added is None:
        key_added = algorithm

    partition_kwargs = {}
    adata = adata.copy() if copy else adata
    if adjacency is None:
        adjacency = _choose_graph(adata, obsp, neighbors_key)

    if resolution is not None:
        partition_kwargs["resolution"] = resolution
    if n_iterations is not None and n_iterations > 0:
        partition_kwargs["max_iter"] = n_iterations

    import cudf
    import cugraph

    offsets = cudf.Series(adjacency.indptr)
    indices = cudf.Series(adjacency.indices)
    if use_weights:
        sources, targets = adjacency.nonzero()
        weights = adjacency[sources, targets]
        if isinstance(weights, np.matrix):
            weights = weights.A1
        weights = cudf.Series(weights)
    else:
        weights = None
    g = cugraph.Graph()

    if hasattr(g, "add_adj_list"):
        g.add_adj_list(offsets, indices, weights)
    else:
        g.from_cudf_adjlist(offsets, indices, weights)

    if algorithm == "leiden":
        clustering_parts, __ = cugraph.leiden(g, **partition_kwargs)
    elif algorithm == "louvain":
        clustering_parts, __ = cugraph.louvain(g, **partition_kwargs)
    else:
        raise ValueError(f"Algorithm `{algorithm}` not supported.")
    groups = clustering_parts.to_pandas().sort_values(
        "vertex")[["partition"]].to_numpy().ravel()

    adata.obs[key_added] = pd.Categorical(
        values=groups.astype("U"),
        categories=natsorted(map(str, np.unique(groups))))
    adata.uns[algorithm] = {}
    adata.uns[algorithm]["params"] = {
        "resolution": resolution,
        "n_iterations": n_iterations}
    return adata if copy else None


def _clustering_key(method_name, resolution=None, n_neighbors=None,
                    n_pcs=None):
    clustering_key = method_name
    if resolution is not None:
        clustering_key = f"{clustering_key}-r_{resolution}"
    if n_neighbors is not None:
        clustering_key = f"{clustering_key}-n_{n_neighbors}"
    if n_pcs is not None:
        clustering_key = f"{clustering_key}-pc_{n_pcs}"
    return clustering_key


def clustering_metric_names(metric_names=None, **kwargs):

    def _keep(metric_name, attribute_name, needed_attribute_value):
        keep = False
        attribute = clustering_metric_attribute(
            metric_name, attribute_name, needs_attribute=True)
        if isinstance(attribute, list):
            keep = needed_attribute_value in attribute
        else:
            keep = attribute == needed_attribute_value
        return keep

    clustering_metric_names = list(CLUSTERING_METRICS)
    for attribute_name, needed_attribute_value in kwargs.items():
        clustering_metric_names = list(filter(
            lambda metric_name: _keep(
                metric_name, attribute_name, needed_attribute_value),
            clustering_metric_names))

    if metric_names is not None:
        convert_to_set = isinstance(metric_names, set)
        metric_names = utilities.check_list(metric_names)
        clustering_metric_names = [
            metric_name
            for metric_name in metric_names
            if utilities.remove_prefix(
                metric_name, prefix=VALIDATION_METRIC_PREFIX)
            in clustering_metric_names]
        if convert_to_set:
            clustering_metric_names = set(clustering_metric_names)

    return clustering_metric_names


def clustering_metric(name):
    clustering_metric = CLUSTERING_METRICS.get(name)
    if not clustering_metric:
        raise ValueError(f"Clustering metric `{name}` not found.")
    return clustering_metric


def clustering_metric_attribute(metric_name, attribute_name,
                                needs_attribute=True):
    metric = clustering_metric(metric_name)
    if needs_attribute and attribute_name not in metric:
        raise ValueError(
            f"Attribute `{attribute_name}` not specified for "
            f"clustering metric `{metric_name}`.")
    attribute = metric.get(attribute_name)
    return attribute


@lru_cache
def clustering_metric_extrema(metric_name, dtype):
    minimum, maximum = clustering_metric_attribute(metric_name, "support")
    limits = np.finfo(dtype)
    if minimum is None:
        minimum = limits.min
    if maximum is None:
        maximum = limits.max
    return {"minimum": minimum, "maximum": maximum}


def _register_clustering_metric(name, supervised, best_direction, support=None,
                                preparations=None, sort_key=False,
                                default=False):
    if support is None:
        support = (None, None)
    preparations = utilities.check_list(preparations)

    def decorator(function):
        CLUSTERING_METRICS[name] = {
            "function": function,
            "supervised": supervised,
            "best_direction": best_direction,
            "support": support,
            "preparations": preparations}
        if sort_key:
            CLUSTERING_DEFAULTS.setdefault("sort_keys", []).append(name)
        if sort_key or default:
            CLUSTERING_DEFAULTS.setdefault("metric_names", []).append(name)
        CLUSTERING_DEFAULTS.setdefault("all_metric_names", []).append(name)
        return function

    return decorator


@_register_clustering_metric("adjusted_rand_index", supervised=True,
                             best_direction=BestDirection.POSITIVE,
                             support=(None, 1), sort_key=True)
def adjusted_rand_index(true_labels, predicted_labels):
    # scikit-learn's function cannot handle a large number of labels,
    # so a reimplementation is used below
    # return sklm.adjusted_rand_score(true_labels, predicted_labels)
    (tn, fp), (fn, tp) = sklm.pair_confusion_matrix(
        true_labels, predicted_labels)
    # convert to Python integer types, to avoid overflow or underflow
    tn, fp, fn, tp = int(tn), int(fp), int(fn), int(tp)

    # Special cases: empty data or full agreement
    if fn == 0 and fp == 0:
        return 1.0

    return 2. * (tp * tn - fn * fp) / (
        (tp + fn) * (fn + tn) + (tp + fp) * (fp + tn))


@_register_clustering_metric("adjusted_mutual_information", supervised=True,
                             best_direction=BestDirection.POSITIVE,
                             support=(None, 1))
def adjusted_mutual_information(true_labels, predicted_labels):
    return sklm.adjusted_mutual_info_score(true_labels, predicted_labels)


@_register_clustering_metric("cluster_accuracy", supervised=True,
                             best_direction=BestDirection.POSITIVE,
                             support=(0, 1))
def cluster_accuracy(true_labels, predicted_labels):
    """Compute cluster accuracy using Hungarian algorithm."""

    true_labels = _check_labels(true_labels)
    predicted_labels = _check_labels(predicted_labels)
    sklu.check_consistent_length(true_labels, predicted_labels)

    true_categories, true_codes = np.unique(true_labels, return_inverse=True)
    predicted_categories, predicted_codes = np.unique(
        predicted_labels, return_inverse=True)

    w = np.zeros((len(true_categories), len(predicted_categories)), dtype=int)
    for i in range(len(true_codes)):
        w[true_codes[i], predicted_codes[i]] += 1
    indices = spo.linear_sum_assignment(w.max() - w)
    accuracy = w[indices].sum() / len(true_codes)
    return accuracy


@_register_clustering_metric("cluster_purity", supervised=True,
                             best_direction=BestDirection.POSITIVE,
                             support=(0, 1))
def cluster_purity(true_labels, predicted_labels):
    # Adapted from https://stackoverflow.com/a/51672699.
    contingency_matrix = sklm.cluster.contingency_matrix(
        true_labels, predicted_labels)
    pure_count = np.sum(np.amax(contingency_matrix, axis=0))
    total_count = np.sum(contingency_matrix)
    purity = pure_count / total_count
    return purity


@_register_clustering_metric("f1_score", supervised=True,
                             best_direction=BestDirection.POSITIVE,
                             support=(0, 1))
def f1_score(true_labels, predicted_labels):
    (tn, fp), (fn, tp) = sklm.pair_confusion_matrix(
        true_labels, predicted_labels)
    # Convert to Python integer types to avoid overflow or underflow
    tn, fp, fn, tp = int(tn), int(fp), int(fn), int(tp)
    f1_score = 2 * tp / (2 * tp + fp + fn)
    return f1_score


@_register_clustering_metric("cluster_count_excess", supervised=True,
                             best_direction=BestDirection.POSITIVE)
def cluster_count_excess(true_labels, predicted_labels):
    true_cluster_count = len(np.unique(true_labels))
    predicted_cluster_count = len(np.unique(predicted_labels))
    return predicted_cluster_count - true_cluster_count


@_register_clustering_metric("silhouette_coefficient", supervised=False,
                             best_direction=BestDirection.POSITIVE,
                             support=(-1, 1),
                             preparations=Preparation.PAIRWISE_DISTANCES,
                             sort_key=True)
def silhouette_coefficient(samples, labels, distance_metric="euclidean"):
    label_count = len(np.unique(labels))
    if label_count == 1:
        result = np.nan
    else:
        result = None
        method = _use_rapids_if_available()
        if method and method == "rapids" and distance_metric != "precomputed":
            import cuml
            if is_categorical_dtype(labels):
                labels = labels.cat.codes.values
            try:
                result = cuml.metrics.cluster.silhouette_score(
                    samples, labels, metric=distance_metric,
                    chunksize=_RAPIDS_CHUNK_SIZE)
            except RuntimeError as error:
                if not str(error).startswith("radix_sort"):
                    raise error
                else:
                    warnings.warn(
                        "RAPIDS failed to compute silhouette coefficient, "
                        "using scikit-learn instead.")
        if result is None:
            result = sklm.silhouette_score(
                samples, labels, metric=distance_metric)
    return result


@_register_clustering_metric("calinski_harabasz_index", supervised=False,
                             best_direction=BestDirection.POSITIVE,
                             preparations=Preparation.DENSE_FORMAT)
def calinski_harabasz_index(samples, labels, **kwargs):
    label_count = len(np.unique(labels))
    if label_count == 1:
        result = np.nan
    else:
        result = sklm.calinski_harabasz_score(samples, labels)
    return result


@_register_clustering_metric("davies_bouldin_index", supervised=False,
                             best_direction=BestDirection.NEGATIVE,
                             support=(0, None),
                             preparations=Preparation.DENSE_FORMAT)
def davies_bouldin_index(samples, labels, **kwargs):
    label_count = len(np.unique(labels))
    if label_count == 1:
        result = np.nan
    else:
        result = sklm.davies_bouldin_score(samples, labels)
    return result


@_register_clustering_metric("cluster_count", supervised=False,
                             best_direction=BestDirection.POSITIVE,
                             support=(1, None))
def cluster_count(samples, labels, **kwargs):
    return len(np.unique(labels))


def _check_labels(labels):
    labels = sklu.check_array(
        labels, ensure_2d=False, ensure_min_samples=0, dtype=None)
    labels = sklu.column_or_1d(labels)
    sklum.check_classification_targets(labels)
    return labels


def _register_decomposer(name):
    def decorator(function):
        LATENT_DECOMPOSERS[name] = function
        return function
    return decorator


@_register_decomposer("pca")
def latent_pca(data_set, **kwargs):
    latent_data_set = data_utilities.latent_data_set_from_data_set(data_set)
    scanpy.tl.pca(latent_data_set, **kwargs)
    data_utilities.copy_annotations(latent_data_set, data_set, prefix="latent")


@_register_decomposer("tsne")
def latent_tsne(data_set, **kwargs):
    latent_data_set = data_utilities.latent_data_set_from_data_set(data_set)
    scanpy.tl.tsne(latent_data_set, **kwargs)
    data_utilities.copy_annotations(latent_data_set, data_set, prefix="latent")


@_register_decomposer("umap")
def latent_umap(data_set, **kwargs):
    latent_data_set = data_utilities.latent_data_set_from_data_set(data_set)
    neighbors_key = _maybe_compute_neighbors(latent_data_set)
    method = _use_rapids_if_available(dependencies="cuml", fallback="umap")
    scanpy.tl.umap(
        latent_data_set, method=method, neighbors_key=neighbors_key, **kwargs)
    data_utilities.copy_annotations(latent_data_set, data_set, prefix="latent")


def _maybe_compute_neighbors(data_set, n_neighbors=None, n_pcs=None):
    neighbors_key = _neighbor_key(n_neighbors=n_neighbors, n_pcs=n_pcs)
    if neighbors_key not in data_set.uns_keys():
        method = _use_rapids_if_available(dependencies="cuml", fallback="umap")
        neighbors_kw = {}
        if n_neighbors:
            neighbors_kw["n_neighbors"] = n_neighbors
        if n_pcs:
            neighbors_kw["n_pcs"] = n_pcs
        if neighbors_key and neighbors_key != _SCANPY_DEFAULT_NEIGHBORS_KEY:
            neighbors_kw["key_added"] = neighbors_key
        scanpy.pp.neighbors(data_set, method=method, **neighbors_kw)
    return neighbors_key


def _neighbor_key(n_neighbors=None, n_pcs=None):
    neighbors_key_parts = [_SCANPY_DEFAULT_NEIGHBORS_KEY]
    if n_neighbors is not None:
        neighbors_key_parts.append(f"n_{n_neighbors}")
    if n_pcs is not None:
        neighbors_key_parts.append(f"pc_{n_pcs}")
    neighbors_key = "-".join(neighbors_key_parts)
    return neighbors_key


def rapids_available():
    return bool(_use_rapids_if_available())


def _use_rapids_if_available(dependencies=None, fallback=None):
    dependencies = utilities.check_list(
        dependencies, default=["cudf", "cuml", "cugraph"])
    method = fallback
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "error", message=".+GPU", category=UserWarning, module="cudf")
        try:
            for dependency in dependencies:
                importlib.import_module(dependency)
            method = "rapids"
        except (ImportError, UserWarning):
            pass
    return method
