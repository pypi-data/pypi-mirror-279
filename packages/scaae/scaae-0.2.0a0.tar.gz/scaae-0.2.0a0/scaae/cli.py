#!/usr/bin/env python3

import argparse

import tensorflow as tf
from tensorflow import keras as tfk

import scaae

INTERMEDIATE_ANALYSIS_DIRECTORY_NAME = "intermediate_analysis"
LOG_DIRECTORY_NAME = "logs"
CONFIG_NAME = "config"
WEIGHTS_NAME = "weights"
TRAINING_NAME = "training"
VALIDATION_NAME = "validation"
EVALUATION_NAME = "test"
DEFAULT_DECOMPOSITION_METHOD = "pca"
DEFAULT_TRAINING_CLUSTERING_METHODS = ["louvain"]
DEFAULT_TRAINING_CLUSTERING_RESOLUTIONS = [0.4, 0.8, 1.2]
DEFAULT_EARLY_STOPPING_INITIAL_DELAY_CONFIG = {
    "sample_size_threshold": 10_000,
    "under_threshold": 10,
    "above_threshold": 1}


def train(path,
          data_set_layer=None,
          gene_mask_annotation_key=None,
          normalise=False,
          scaling_method=None,
          plot_annotation_key_match_patterns=None,
          plot_annotation_key_ignore_patterns=None,
          ground_truth_annotation_key=None,
          ground_truth_representation_key=None,
          batch_size=64,
          validation_path=None,
          model_kind="base",
          intermediate_sizes=None,
          discriminator_intermediate_sizes=None,
          latent_size=None,
          category_count=None,
          model_config=None,
          optimiser=None,
          autoencoder_learning_rate=None,
          discriminator_learning_rate=None,
          generator_learning_rate=None,
          learning_decay_rate=None,
          gradient_clipping_norm=None,
          gradient_clipping_value=None,
          optimisation_config=None,
          epoch_count=100,
          early_stopping_loss=None,
          early_stopping_patience=25,
          early_stopping_initial_delay=None,
          convergence_stopping_loss_pattern=None,
          convergence_stopping_threshold=1e-4,
          convergence_stopping_window_size=10,
          clustering_methods=None,
          clustering_resolutions=None,
          clustering_neighbourhood_sizes=None,
          clustering_principal_component_counts=None,
          clustering_metric_aggregator="optimum",
          output_directory=None,
          plotting=False,
          logging_options=None,
          dense_memory_limit_in_gigabytes=None,
          eagerly=False,
          verbose=1):

    printer = scaae.utilities.Printer(verbose=verbose)
    tf.config.run_functions_eagerly(eagerly)

    if output_directory:
        output_directory = scaae.utilities.check_path(output_directory)
        output_directory.mkdir(parents=True, exist_ok=True)

    training_set_name, validation_set_name = _subset_names_for_training(
        validation=validation_path is not None)

    printer.print(f"Loading {training_set_name}.")
    training_set = scaae.data.read(path, layer=data_set_layer)
    training_set.uns["name"] = training_set_name

    if validation_path:
        printer.print(f"Loading {validation_set_name}.")
        validation_set = scaae.data.read(validation_path, layer=data_set_layer)
        validation_set.uns["name"] = validation_set_name
        validation_set_otherwise_training_set = validation_set
        validation_otherwise_training = VALIDATION_NAME
        validation_metric_prefix = scaae.models.VALIDATION_METRIC_PREFIX
    else:
        validation_set = None
        validation_set_otherwise_training_set = training_set
        validation_otherwise_training = TRAINING_NAME
        validation_metric_prefix = ""

    if gene_mask_annotation_key or normalise or scaling_method:
        preprocessing_message = _preprocessing_message(
            gene_mask_annotation_key=gene_mask_annotation_key,
            normalise=normalise,
            scaling_method=scaling_method)
        printer.print(
            f"Preprocessing {training_set_name} by {preprocessing_message}.")
        training_set = scaae.data.preprocess(
            training_set,
            gene_mask_annotation_key=gene_mask_annotation_key,
            normalise=normalise,
            scaling_method=scaling_method)
        if validation_set is not None:
            printer.print(
                f"Preprocessing {validation_set_name} "
                f"by {preprocessing_message}.")
            validation_set = scaae.data.preprocess(
                validation_set,
                gene_mask_annotation_key=gene_mask_annotation_key,
                normalise=normalise,
                scaling_method=scaling_method)

    feature_size = training_set.shape[1]

    model_config = scaae.models.utilities.load_model_config(
        config_or_path=model_config,
        data_interval=training_set.uns.get("data_interval"),
        model_kind=model_kind,
        feature_size=feature_size,
        intermediate_sizes=intermediate_sizes,
        discriminator_intermediate_sizes=discriminator_intermediate_sizes,
        latent_size=latent_size,
        category_count=category_count)

    optimisation_config = scaae.models.utilities.load_optimisation_config(
        config_or_path=optimisation_config,
        default_optimiser_name=optimiser,
        autoencoder_learning_rate=autoencoder_learning_rate,
        discriminator_learning_rate=discriminator_learning_rate,
        generator_learning_rate=generator_learning_rate,
        default_learning_decay_rate=learning_decay_rate,
        default_gradient_clipping_norm=gradient_clipping_norm,
        default_gradient_clipping_value=gradient_clipping_value)

    distribution_strategy = _distribution_strategy(
        mode="training", verbose=printer.verbose)
    effective_batch_size = (
        batch_size * distribution_strategy.num_replicas_in_sync)

    _check_rapids_availability(verbose=printer.verbose)

    printer.print("Setting up model.")
    with distribution_strategy.scope():
        aae = scaae.models.get_adversarial_autoencoder(model_config)
        aae.compile(**optimisation_config, run_eagerly=eagerly)

    aae.summary(print_fn=printer.verbose_print)

    callbacks = []

    update_hyperparamters_callback = (
        scaae.callbacks.UpdateHyperparameters())
    callbacks.append(update_hyperparamters_callback)

    stop_on_invalid_loss_callback = scaae.callbacks.StopOnInvalidLoss(
        verbose=printer.verbose)
    callbacks.append(stop_on_invalid_loss_callback)

    clustering_methods = (
        clustering_methods or DEFAULT_TRAINING_CLUSTERING_METHODS)
    clustering_resolutions = (
        clustering_resolutions or DEFAULT_TRAINING_CLUSTERING_RESOLUTIONS)

    if early_stopping_loss:
        early_stopping_loss = scaae.utilities.ensure_prefix(
            early_stopping_loss, prefix=validation_metric_prefix)
        early_stopping_initial_delay = (
            early_stopping_initial_delay
            if early_stopping_initial_delay is not None
            else _default_early_stopping_initial_delay(
                sample_size=training_set.n_obs))
        early_stopping_callback = scaae.callbacks.EarlyStopping(
            monitor=early_stopping_loss,
            min_delta=0,
            patience=early_stopping_patience,
            initial_delay=early_stopping_initial_delay,
            verbose=printer.verbose,
            mode="auto",
            restore_best_weights=True,
            data_set=validation_set_otherwise_training_set,
            clustering_methods=clustering_methods,
            clustering_resolutions=clustering_resolutions,
            clustering_neighbourhood_sizes=clustering_neighbourhood_sizes,
            clustering_principal_component_counts=(
                clustering_principal_component_counts),
            ground_truth_annotation_key=ground_truth_annotation_key,
            ground_truth_representation_key=ground_truth_representation_key,
            clustering_metric_aggregator=clustering_metric_aggregator,
            batch_size=effective_batch_size)
        callbacks.append(early_stopping_callback)

    if convergence_stopping_loss_pattern:
        convergence_stopping_loss_pattern = scaae.utilities.ensure_prefix(
            convergence_stopping_loss_pattern, prefix=validation_metric_prefix)
        stop_at_convergence_callback = scaae.callbacks.StopAtConvergence(
            monitor_pattern=convergence_stopping_loss_pattern,
            threshold=convergence_stopping_threshold,
            window_size=convergence_stopping_window_size,
            smoothing_method="exponential_moving_average",
            data_set=validation_set_otherwise_training_set,
            clustering_methods=clustering_methods,
            clustering_resolutions=clustering_resolutions,
            clustering_neighbourhood_sizes=clustering_neighbourhood_sizes,
            clustering_principal_component_counts=(
                clustering_principal_component_counts),
            ground_truth_annotation_key=ground_truth_annotation_key,
            ground_truth_representation_key=ground_truth_representation_key,
            clustering_metric_aggregator=clustering_metric_aggregator,
            batch_size=effective_batch_size,
            verbose=printer.verbose)
        callbacks.append(stop_at_convergence_callback)

    initial_epoch = 0
    callback_duration_log_path = None

    if output_directory:
        backup_and_restoration_callback = scaae.callbacks.BackUpAndRestore(
            directory=output_directory,
            config_name=CONFIG_NAME,
            weights_name=WEIGHTS_NAME)
        initial_epoch = backup_and_restoration_callback.initial_epoch()
        callbacks.append(backup_and_restoration_callback)

        training_info_logger_callback = (
            scaae.callbacks.TrainingInfoLogger(
                batch_size=batch_size,
                total_epoch_count=epoch_count,
                early_stopping_loss=early_stopping_loss,
                early_stopping_patience=early_stopping_patience,
                early_stopping_initial_delay=early_stopping_initial_delay,
                convergence_stopping_loss_pattern=(
                    convergence_stopping_loss_pattern),
                convergence_stopping_threshold=(
                    convergence_stopping_threshold),
                convergence_stopping_window_size=(
                    convergence_stopping_window_size),
                clustering_methods=clustering_methods,
                clustering_resolutions=clustering_resolutions,
                clustering_neighbourhood_sizes=clustering_neighbourhood_sizes,
                clustering_principal_component_counts=(
                    clustering_principal_component_counts),
                ground_truth_annotation_key=ground_truth_annotation_key,
                ground_truth_representation_key=(
                    ground_truth_representation_key),
                clustering_metric_aggregator=clustering_metric_aggregator,
                output_directory=output_directory))
        callbacks.append(training_info_logger_callback)

        training_csv_log_path = output_directory.joinpath(
            f"{TRAINING_NAME}-metrics.csv")
        training_csv_logger_callback = scaae.callbacks.TrainingCSVLogger(
            filename=training_csv_log_path, append=True)
        callbacks.append(training_csv_logger_callback)

        if logging_options:
            logging_options = scaae.utilities.check_list(logging_options)
            log_directory = output_directory.joinpath(LOG_DIRECTORY_NAME)
            log_directory.mkdir(parents=True, exist_ok=True)

            if "tensorboard" in logging_options:
                tensorboard_callback = tfk.callbacks.TensorBoard(
                    log_dir=log_directory,
                    write_graph=False,
                    profile_batch=0)
                callbacks.append(tensorboard_callback)

            if "callback_durations" in logging_options:
                callback_duration_log_path = log_directory.joinpath(
                    f"{TRAINING_NAME}-callback_durations.csv")

        if plotting:
            intermediate_results_directory = output_directory.joinpath(
                INTERMEDIATE_ANALYSIS_DIRECTORY_NAME)
            intermediate_results_directory.mkdir(parents=True, exist_ok=True)
            learning_curve_plotter_callback = (
                scaae.callbacks.LearningCurvePlotter(
                    output_directory=intermediate_results_directory,
                    base_name="learning_curves"))
            callbacks.append(learning_curve_plotter_callback)

            if aae.latent_size > 1:
                plot_latent_space_callback = (
                    scaae.callbacks.LatentSpacePlotter(
                        data_set=validation_set_otherwise_training_set,
                        annotation_key_match_patterns=(
                            plot_annotation_key_match_patterns),
                        annotation_key_ignore_patterns=(
                            plot_annotation_key_ignore_patterns),
                        base_name=(
                            f"{validation_otherwise_training}"
                            "-latent_representation"),
                        output_directory=intermediate_results_directory,
                        batch_size=effective_batch_size,
                        verbose=printer.verbose))
                callbacks.append(plot_latent_space_callback)
                plot_true_distribution_parameters_callback = (
                    scaae.callbacks.TrueDistributionParameterPlotter(
                        output_directory=intermediate_results_directory))
                callbacks.append(plot_true_distribution_parameters_callback)

    training_stopwatch_callback = scaae.callbacks.TrainingStopwatch(
        verbose=printer.verbose)
    callbacks.append(training_stopwatch_callback)

    callback_list = scaae.callbacks.AdditionalMetricsCallbackList(
        callbacks=callbacks,
        data_set=validation_set_otherwise_training_set,
        clustering_methods=clustering_methods,
        clustering_resolutions=clustering_resolutions,
        clustering_neighbourhood_sizes=clustering_neighbourhood_sizes,
        clustering_principal_component_counts=(
            clustering_principal_component_counts),
        ground_truth_annotation_key=ground_truth_annotation_key,
        ground_truth_representation_key=ground_truth_representation_key,
        clustering_metric_aggregator=clustering_metric_aggregator,
        batch_size=effective_batch_size,
        callback_duration_log_path=callback_duration_log_path,
        verbose=printer.verbose)

    # Add progress-bar callback explicitly to fix order of output
    progress_bar_callback = tf.keras.callbacks.ProgbarLogger(
        count_mode="steps", stateful_metrics=aae.metrics_names)
    all_callbacks = [progress_bar_callback, callback_list]

    if initial_epoch < epoch_count:
        metric_names = callback_list.additional_metrics_at_epoch_end()
        if metric_names:
            scaae.analyses.prepare_for_clustering_metrics(
                data_set=validation_set_otherwise_training_set,
                representation_key=ground_truth_representation_key,
                metric_names=callback_list.additional_metrics_at_epoch_end(),
                dense_memory_limit_in_gigabytes=(
                    dense_memory_limit_in_gigabytes))
        printer.print("Training model:")
        aae.fit(
            training_set.X,
            validation_data=(
                validation_set.X,) if validation_set is not None else None,
            batch_size=effective_batch_size,
            epochs=epoch_count,
            initial_epoch=initial_epoch,
            callbacks=all_callbacks,
            verbose=printer.keras_models_verbose)
    else:
        printer.print("Model has already been trained.")

    if output_directory:
        if training_csv_log_path.exists():
            learning_curves = scaae.utilities.load_csv(
                training_csv_log_path)
            learning_curve_plot_path = output_directory.joinpath(
                "learning_curves.png")
            scaae.analyses.plot_learning_curves(
                learning_curves,
                metric_groups=aae.metric_groups,
                path=learning_curve_plot_path)
        if callback_duration_log_path and callback_duration_log_path.exists():
            callback_durations = scaae.utilities.load_csv(
                callback_duration_log_path)
            callback_duration_sums_path = callback_duration_log_path.with_name(
                f"{callback_duration_log_path.stem}-sum"
                f"{callback_duration_log_path.suffix}")
            callback_durations.sum(numeric_only=True).to_csv(
                callback_duration_sums_path,
                header=["total_duration_in_seconds"])


def encode(path,
           model_directory,
           output_directory,
           data_set_layer=None,
           gene_mask_annotation_key=None,
           normalise=False,
           scaling_method=None,
           batch_size=64,
           verbose=1):
    printer = scaae.utilities.Printer(verbose=verbose)
    output_directory = scaae.utilities.check_path(output_directory)
    data_set = _encode(
        path=path,
        model_directory=model_directory,
        output_directory=output_directory,
        data_set_layer=data_set_layer,
        gene_mask_annotation_key=gene_mask_annotation_key,
        normalise=normalise,
        scaling_method=scaling_method,
        batch_size=batch_size,
        verbose=printer.verbose)
    latent_representation_path = output_directory.joinpath(
        "latent_representation.h5ad")
    printer.print("Saving latent representation.")
    scaae.analyses.save_latent_representation(
        data_set, path=latent_representation_path)


def analyse(path,
            output_directory,
            latent_representation_path=None,
            latent_annotations_path=None,
            data_set_layer=None,
            gene_mask_annotation_key=None,
            normalise=False,
            scaling_method=None,
            plot_annotation_key_match_patterns=None,
            plot_annotation_key_ignore_patterns=None,
            ground_truth_annotation_key_match_patterns=None,
            ground_truth_annotation_key_ignore_patterns=None,
            decomposition_methods=None,
            clustering_methods=None,
            clustering_resolutions=None,
            clustering_neighbourhood_sizes=None,
            clustering_principal_component_counts=None,
            clustering_metrics=None,
            clustering_sort_keys=None,
            sankey_ground_truth_order=None,
            latent_clustering_plot_limit=None,
            latent_clustering_plot_median=False,
            dense_memory_limit_in_gigabytes=None,
            save_latent_annotations=True,
            latent_annotations_name="scaae_annotations",
            verbose=1):

    printer = scaae.utilities.Printer(verbose=verbose)
    output_directory = scaae.utilities.check_path(output_directory)
    if latent_representation_path:
        latent_representation_path = scaae.utilities.check_path(
            latent_representation_path)
    if latent_annotations_path:
        latent_annotations_path = scaae.utilities.check_path(
            latent_annotations_path)

    printer.print("Loading data set.")
    evaluation_set = scaae.data.read(path, layer=data_set_layer)

    if gene_mask_annotation_key or normalise or scaling_method:
        preprocessing_message = _preprocessing_message(
            gene_mask_annotation_key=gene_mask_annotation_key,
            normalise=normalise,
            scaling_method=scaling_method)
        printer.print(f"Preprocessing data set by {preprocessing_message}.")
        evaluation_set = scaae.data.preprocess(
            evaluation_set,
            gene_mask_annotation_key=gene_mask_annotation_key,
            normalise=normalise,
            scaling_method=scaling_method)

    if (not scaae.data.utilities.has_latent_representation(evaluation_set)
            and latent_representation_path is None):
        raise Exception(
            "Data set does not include a latent representation. "
            "Please specify a path to the latent representation separately.")

    if latent_representation_path:
        if latent_representation_path.samefile(path):
            latent_representation = evaluation_set.copy()
            scaae.data.utilities.remove_annotations_from_data_set(
                latent_representation)
        else:
            latent_string = "latent representation"
            if latent_annotations_path:
                latent_string = f"{latent_string} and annotations"
            printer.print(f"Loading {latent_string}.")
            latent_representation = scaae.data.read_latent_representation(
                latent_representation_path)
        if latent_annotations_path:
            latent_annotations = scaae.data.read_annotations(
                latent_annotations_path)
            scaae.data.utilities.add_observation_annotations_to_data_set(
                latent_representation, latent_annotations)
        scaae.data.utilities.add_latent_representation_to_data_set(
            latent_representation=latent_representation,
            data_set=evaluation_set,
            add_annotations=True)

    _analyse(
        evaluation_set=evaluation_set,
        output_directory=output_directory,
        decomposition_methods=decomposition_methods,
        clustering_methods=clustering_methods,
        clustering_resolutions=clustering_resolutions,
        clustering_neighbourhood_sizes=clustering_neighbourhood_sizes,
        clustering_principal_component_counts=(
            clustering_principal_component_counts),
        clustering_metrics=clustering_metrics,
        clustering_sort_keys=clustering_sort_keys,
        sankey_ground_truth_order=sankey_ground_truth_order,
        latent_clustering_plot_limit=latent_clustering_plot_limit,
        latent_clustering_plot_median=latent_clustering_plot_median,
        plot_annotation_key_match_patterns=plot_annotation_key_match_patterns,
        plot_annotation_key_ignore_patterns=(
            plot_annotation_key_ignore_patterns),
        ground_truth_annotation_key_match_patterns=(
            ground_truth_annotation_key_match_patterns),
        ground_truth_annotation_key_ignore_patterns=(
            ground_truth_annotation_key_ignore_patterns),
        dense_memory_limit_in_gigabytes=dense_memory_limit_in_gigabytes,
        verbose=printer.verbose)

    if clustering_methods and save_latent_annotations:
        additional_latent_annotations_path = output_directory.joinpath(
            f"{latent_representation_path.stem}-{latent_annotations_name}"
            ".h5ad")
        printer.print("Saving latent annotations.")
        scaae.analyses.save_additional_latent_annotations(
            evaluation_set,
            original_latent_data_set=latent_representation,
            path=additional_latent_annotations_path)


def evaluate(path,
             model_directory,
             output_directory,
             data_set_layer=None,
             gene_mask_annotation_key=None,
             normalise=False,
             scaling_method=None,
             plot_annotation_key_match_patterns=None,
             plot_annotation_key_ignore_patterns=None,
             ground_truth_annotation_key_match_patterns=None,
             ground_truth_annotation_key_ignore_patterns=None,
             batch_size=64,
             decomposition_methods=None,
             clustering_methods=None,
             clustering_resolutions=None,
             clustering_neighbourhood_sizes=None,
             clustering_principal_component_counts=None,
             clustering_metrics=None,
             clustering_sort_keys=None,
             sankey_ground_truth_order=None,
             latent_clustering_plot_limit=None,
             latent_clustering_plot_median=False,
             save_latent_representation=True,
             dense_memory_limit_in_gigabytes=None,
             verbose=1):

    printer = scaae.utilities.Printer(verbose=verbose)
    output_directory = scaae.utilities.check_path(output_directory)

    decomposition_methods = decomposition_methods or "pca"

    evaluation_set = _encode(
        path=path,
        model_directory=model_directory,
        output_directory=output_directory,
        data_set_layer=data_set_layer,
        gene_mask_annotation_key=gene_mask_annotation_key,
        normalise=normalise,
        scaling_method=scaling_method,
        batch_size=batch_size,
        evaluate_model=True,
        output_prefix=EVALUATION_NAME,
        verbose=printer.verbose)

    _analyse(
        evaluation_set=evaluation_set,
        output_directory=output_directory,
        decomposition_methods=decomposition_methods,
        plot_annotation_key_match_patterns=plot_annotation_key_match_patterns,
        plot_annotation_key_ignore_patterns=(
            plot_annotation_key_ignore_patterns),
        ground_truth_annotation_key_match_patterns=(
            ground_truth_annotation_key_match_patterns),
        ground_truth_annotation_key_ignore_patterns=(
            ground_truth_annotation_key_ignore_patterns),
        clustering_methods=clustering_methods,
        clustering_resolutions=clustering_resolutions,
        clustering_neighbourhood_sizes=clustering_neighbourhood_sizes,
        clustering_principal_component_counts=(
            clustering_principal_component_counts),
        clustering_metrics=clustering_metrics,
        clustering_sort_keys=clustering_sort_keys,
        sankey_ground_truth_order=sankey_ground_truth_order,
        latent_clustering_plot_limit=latent_clustering_plot_limit,
        latent_clustering_plot_median=latent_clustering_plot_median,
        output_prefix=EVALUATION_NAME,
        dense_memory_limit_in_gigabytes=dense_memory_limit_in_gigabytes,
        verbose=printer.verbose)

    if save_latent_representation:
        latent_representation_path = output_directory.joinpath(
            f"{EVALUATION_NAME}-latent_representation.h5ad")
        printer.print("Saving latent representation.")
        scaae.analyses.save_latent_representation(
            evaluation_set, path=latent_representation_path)


def _encode(path,
            model_directory,
            output_directory,
            data_set_layer=None,
            gene_mask_annotation_key=None,
            normalise=False,
            scaling_method=None,
            batch_size=64,
            evaluate_model=False,
            output_prefix=None,
            verbose=1):

    printer = scaae.utilities.Printer(verbose=verbose)

    model_directory = scaae.utilities.check_path(model_directory)
    output_directory = scaae.utilities.check_path(output_directory)
    output_directory.mkdir(parents=True, exist_ok=True)

    printer.print("Loading data set.")
    data_set = scaae.data.read(path, layer=data_set_layer)

    if gene_mask_annotation_key or normalise or scaling_method:
        preprocessing_message = _preprocessing_message(
            gene_mask_annotation_key=gene_mask_annotation_key,
            normalise=normalise,
            scaling_method=scaling_method)
        printer.print(f"Preprocessing data set by {preprocessing_message}.")
        data_set = scaae.data.preprocess(
            data_set,
            gene_mask_annotation_key=gene_mask_annotation_key,
            normalise=normalise,
            scaling_method=scaling_method)

    feature_size = data_set.shape[1]

    backup_and_restoration_callback = scaae.callbacks.BackUpAndRestore(
        directory=model_directory,
        config_name=CONFIG_NAME,
        weights_name=WEIGHTS_NAME,
        restore_when_evaluating=True)
    model_config = scaae.models.utilities.load_model_config(
        config_or_path=backup_and_restoration_callback.config_path,
        feature_size=feature_size)

    distribution_strategy = _distribution_strategy(
        mode="evaluation", verbose=printer.verbose)
    effective_batch_size = (
        batch_size * distribution_strategy.num_replicas_in_sync)

    printer.print("Setting up model.")
    with distribution_strategy.scope():
        aae = scaae.models.get_adversarial_autoencoder(model_config)
        aae.compile()

    aae.summary(print_fn=printer.verbose_print)

    if evaluate_model:
        callbacks = []
        callbacks.append(backup_and_restoration_callback)

        stop_on_invalid_loss_callback = scaae.callbacks.StopOnInvalidLoss()
        callbacks.append(stop_on_invalid_loss_callback)

        test_csv_log_filename = "metrics.csv"
        if output_prefix:
            test_csv_log_filename = (
                f"{output_prefix}-{test_csv_log_filename}")
        test_csv_log_path = output_directory.joinpath(test_csv_log_filename)
        test_csv_logger_callback = scaae.callbacks.TestCSVLogger(
            path=test_csv_log_path)
        callbacks.append(test_csv_logger_callback)

        printer.print("Evaluating model on data set:")
        aae.evaluate(
            data_set.X,
            batch_size=effective_batch_size,
            callbacks=callbacks,
            verbose=printer.keras_models_verbose)

    printer.print("Encoding data set into latent representation:")
    latent_samples = aae.encoder.predict(
        data_set.X,
        batch_size=effective_batch_size,
        verbose=printer.keras_models_verbose)
    if scaae.models.is_categorical(aae.encoder):
        latent_representation, latent_categories = latent_samples
    else:
        latent_representation = latent_samples
        latent_categories = None
    scaae.data.utilities.add_latent_representation_to_data_set(
        latent_representation=latent_representation,
        data_set=data_set,
        latent_categories=latent_categories)

    return data_set


def _subset_names_for_training(validation=False):
    if validation:
        training_set_name = f"{TRAINING_NAME} set"
        validation_set_name = f"{VALIDATION_NAME} set"
    else:
        training_set_name = "data set"
        validation_set_name = None
    return training_set_name, validation_set_name


def _analyse(evaluation_set,
             output_directory,
             decomposition_methods=None,
             plot_annotation_key_match_patterns=None,
             plot_annotation_key_ignore_patterns=None,
             ground_truth_annotation_key_match_patterns=None,
             ground_truth_annotation_key_ignore_patterns=None,
             clustering_methods=None,
             clustering_resolutions=None,
             clustering_neighbourhood_sizes=None,
             clustering_principal_component_counts=None,
             clustering_metrics=None,
             clustering_sort_keys=None,
             sankey_ground_truth_order=None,
             latent_clustering_plot_limit=None,
             latent_clustering_plot_median=False,
             output_prefix=None,
             dense_memory_limit_in_gigabytes=None,
             verbose=1):

    initial_latent_categorical_annotation_keys = (
        scaae.data.utilities.categorical_annotation_keys(
            evaluation_set.obs, latent_only=True))

    printer = scaae.utilities.Printer(verbose=verbose)
    output_directory = scaae.utilities.check_path(output_directory)
    output_directory.mkdir(parents=True, exist_ok=True)

    clustering_metrics = _check_clustering_metrics(clustering_metrics)

    clustering_methods = scaae.utilities.check_list(clustering_methods)
    clustering_resolutions = scaae.utilities.check_list(
        clustering_resolutions, wrap_none=True)
    clustering_neighbourhood_sizes = scaae.utilities.check_list(
        clustering_neighbourhood_sizes, wrap_none=True)
    clustering_principal_component_counts = scaae.utilities.check_list(
        clustering_principal_component_counts, wrap_none=True)

    if clustering_methods:
        clustering_configs = scaae.analyses.clustering_configs(
            clustering_methods,
            resolutions=clustering_resolutions,
            neighbourhood_sizes=clustering_neighbourhood_sizes,
            principal_component_counts=clustering_principal_component_counts)
        printer.print("Clustering latent representation:")
        scaae.analyses.cluster_latent_representation_with_configs(
            evaluation_set,
            *clustering_configs,
            enable_progress_bar=printer.verbose)

    plottable_annotation_keys = (
        scaae.data.utilities.plottable_annotation_keys(
            evaluation_set.obs,
            match_patterns=plot_annotation_key_match_patterns,
            ignore_patterns=plot_annotation_key_ignore_patterns))

    if clustering_methods or initial_latent_categorical_annotation_keys:
        printer.print("Evaluate latent clusterings:")
        scaae.analyses.prepare_for_clustering_metrics(
            data_set=evaluation_set,
            dense_memory_limit_in_gigabytes=dense_memory_limit_in_gigabytes)
        clustering_metric_sets = scaae.analyses.evaluate_clusterings(
            evaluation_set,
            metric_names=clustering_metrics,
            ground_truth_annotation_key_match_patterns=(
                ground_truth_annotation_key_match_patterns),
            ground_truth_annotation_key_ignore_patterns=(
                ground_truth_annotation_key_ignore_patterns),
            sort_keys=clustering_sort_keys,
            enable_progress_bar=printer.verbose)
        for clustering_metric_set_name, clustering_metric_set in (
                clustering_metric_sets.items()):
            clustering_metric_set_filename = (
                f"{clustering_metric_set_name}_clustering_metrics.csv")
            if output_prefix:
                clustering_metric_set_filename = (
                    f"{output_prefix}-{clustering_metric_set_filename}")
            clustering_metric_set_path = output_directory.joinpath(
                clustering_metric_set_filename)
            clustering_metric_set.to_csv(clustering_metric_set_path)

        if latent_clustering_plot_limit is not None:
            plottable_annotation_keys = (
                scaae.analyses.limit_latent_clustering_annotation_keys(
                    plottable_annotation_keys,
                    limit=latent_clustering_plot_limit,
                    additional_keys=initial_latent_categorical_annotation_keys,
                    clustering_metric_sets=clustering_metric_sets,
                    clustering_sort_keys=clustering_sort_keys,
                    include_median=latent_clustering_plot_median))

    decomposition_methods = _check_decomposition_methods(
        decomposition_methods,
        latent_size=scaae.data.utilities.latent_representation_size(
            evaluation_set))

    for decomposition_method in decomposition_methods:
        printer.print(
            "Plotting latent representation using method "
            f"\"{decomposition_method}\":")
        for plottable_annotation_key in scaae.utilities.ProgressBar(
                plottable_annotation_keys, unit="plot", unit_plural="plots",
                disable=not printer.verbose):
            plot_filename = (
                f"latent_space-{decomposition_method}"
                f"-{plottable_annotation_key}.png")
            if output_prefix:
                plot_filename = (
                    f"{output_prefix}-{plot_filename}")
            plot_path = output_directory.joinpath(plot_filename)
            scaae.analyses.plot_latent_representation(
                evaluation_set, annotation_keys=plottable_annotation_key,
                decomposition_method=decomposition_method, path=plot_path)

    if sankey_ground_truth_order:
        latent_annotation_keys = (
            scaae.data.utilities.categorical_annotation_keys(
                evaluation_set.obs, latent_only=True))
        for latent_annotation_key in latent_annotation_keys:
            clustering_annotation_keys = (
                sankey_ground_truth_order + [latent_annotation_key])
            clustering_annotation_keys_string = (
                scaae.utilities.join_strings(map(
                    lambda s: f"\"{s}\"", clustering_annotation_keys)))
            printer.print(
                "Plotting Sankey diagram for annotations "
                f"{clustering_annotation_keys_string}.")
            sankey_diagram_filename = (
                f"sankey-{latent_annotation_key}.png")
            if output_prefix:
                sankey_diagram_filename = (
                    f"{output_prefix}-{sankey_diagram_filename}")
            sankey_diagram_path = output_directory.joinpath(
                sankey_diagram_filename)
            scaae.analyses.plot_clusterings_in_sankey_diagram(
                evaluation_set,
                clustering_annotation_keys=clustering_annotation_keys,
                path=sankey_diagram_path)


def _preprocessing_message(gene_mask_annotation_key=None, normalise=False,
                           scaling_method=None):
    message_parts = []
    if gene_mask_annotation_key:
        message_parts.append(
            f"keeping genes according to the \"{gene_mask_annotation_key}\" "
            "gene mask annotation")
    if normalise:
        message_parts.append("normalising")
    if scaling_method:
        message_parts.append(f"scaling using the \"{scaling_method}\" method")
    return scaae.utilities.join_strings(message_parts, "and")


def _distribution_strategy(mode, verbose=0):
    printer = scaae.utilities.Printer(verbose=verbose)
    available_gpus = tf.config.list_physical_devices("GPU")
    available_gpu_count = len(available_gpus) if available_gpus else 0
    if available_gpu_count > 1:
        printer.print(
            f"Using {available_gpu_count} GPUs for {mode} in parallel.")
        strategy = tf.distribute.MirroredStrategy()
    elif available_gpu_count == 1:
        printer.print(f"Using GPU for {mode}.")
        strategy = tf.distribute.get_strategy()
    else:
        strategy = tf.distribute.get_strategy()
    return strategy


def _check_rapids_availability(verbose=0):
    printer = scaae.utilities.Printer(verbose=verbose)
    if scaae.analyses.rapids_available():
        printer.print("Using RAPIDS when possible.")


def _default_early_stopping_initial_delay(sample_size):
    sample_size_threshold = DEFAULT_EARLY_STOPPING_INITIAL_DELAY_CONFIG[
        "sample_size_threshold"]
    initial_delay_under_threshold = (
        DEFAULT_EARLY_STOPPING_INITIAL_DELAY_CONFIG["under_threshold"])
    initial_delay_above_threshold = (
        DEFAULT_EARLY_STOPPING_INITIAL_DELAY_CONFIG["above_threshold"])
    return (
        initial_delay_above_threshold
        if sample_size_threshold > sample_size_threshold
        else initial_delay_under_threshold)


def _check_clustering_metrics(clustering_metrics=None):
    if clustering_metrics is None:
        clustering_metrics = scaae.analyses.CLUSTERING_DEFAULTS.get(
            "metric_names")
    elif clustering_metrics == ["all"] or clustering_metrics == "all":
        clustering_metrics = scaae.analyses.CLUSTERING_DEFAULTS.get(
            "all_metric_names")
    return clustering_metrics


def _check_decomposition_methods(decomposition_methods, latent_size):
    decomposition_methods = scaae.utilities.check_list(decomposition_methods)
    if latent_size == 1:
        decomposition_methods = []
    elif latent_size == 2:
        decomposition_methods = [None]
    return decomposition_methods


def _format_clustering_method_and_parameters(method, resolution=None,
                                             neighbourhood_size=None,
                                             principal_component_count=None):
    spec = f"\"{method}\""
    config_parts = []
    if resolution is not None:
        config_parts.append(f"resolution: {resolution}")
    if neighbourhood_size is not None:
        config_parts.append(f"neighbourhood size: {neighbourhood_size}")
    if principal_component_count is not None:
        config_parts.append(
            f"principal_component_count: {principal_component_count}")
    if config_parts:
        config = ", ".join(config_parts)
        spec = f"{spec} ({config})"
    return spec


def _version_string():
    import sys

    if sys.version_info >= (3, 8):
        from importlib import metadata
    else:
        import importlib_metadata as metadata

    name = __package__ or __name__
    if isinstance(name, str):
        name = name.split(".", 1)[0]

    try:
        metadata = metadata.metadata(name)
        name = metadata["name"]
        version = metadata["version"]
        version_string = f"{name} {version}"
    except metadata.PackageNotFoundError:
        version_string = "Please install package first."

    return version_string


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        "--version", "-V",
        action="version",
        version="{version}".format(version=_version_string()))

    subparsers = parser.add_subparsers(title="subcommands", required=True)

    training_subparser = subparsers.add_parser(
        name="train",
        description="Train model on single-cell transcriptomic data.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    training_subparser.set_defaults(func=train)

    encoding_subparser = subparsers.add_parser(
        name="encode",
        description="Encode single-cell transcriptomic data using model.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    encoding_subparser.set_defaults(func=encode)

    analysis_subparser = subparsers.add_parser(
        name="analyse",
        description="Analyse encoded single-cell transcriptomic data.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    analysis_subparser.set_defaults(func=analyse)

    evaluation_subparser = subparsers.add_parser(
        name="evaluate",
        description="Evaluate model on single-cell transcriptomic data.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    evaluation_subparser.set_defaults(func=evaluate)

    for subparser in (training_subparser, encoding_subparser,
                      analysis_subparser, evaluation_subparser):
        subparser.add_argument(
            dest="path",
            type=str,
            help="path to data set")

    for subparser in (encoding_subparser, evaluation_subparser):
        subparser.add_argument(
            "--model-directory", "-m",
            dest="model_directory",
            metavar="path",
            type=str,
            required=True,
            help=(
                "path to model directory, "
                "if output directory does not contain a `model` directory"))

    for subparser in (encoding_subparser, analysis_subparser,
                      evaluation_subparser):
        subparser.add_argument(
            "--output-directory", "-o",
            dest="output_directory",
            metavar="path",
            type=str,
            required=True,
            help="path to output directory")

    training_subparser.add_argument(
        "--output-directory", "-o",
        dest="output_directory",
        metavar="path",
        type=str,
        default=None,
        help=(
            "path to output directory, "
            "if none is provided, model is not saved"))

    for subparser in (training_subparser, encoding_subparser,
                      analysis_subparser, evaluation_subparser):

        subparser.add_argument(
            "--data-set-layer", "-l",
            dest="data_set_layer",
            metavar="layer_name",
            type=str,
            default=None,
            help="layer name to use for data set, if supported")
        subparser.add_argument(
            "--gene-mask-annotation", "--gma",
            dest="gene_mask_annotation_key",
            metavar="annotation_name",
            type=str,
            default=None,
            help="name for annotation containing gene mask for preprocessing")
        subparser.add_argument(
            "--normalise", "-n",
            dest="normalise",
            action="store_true",
            default=False,
            help="normalise data set")
        scaling_group = subparser.add_mutually_exclusive_group()
        scaling_group.add_argument(
            "--scaling-method", "--sm",
            dest="scaling_method",
            metavar="method_name",
            type=str,
            default=None,
            help=(
                "name for method used to scale data set, options: "
                + ", ".join(list(scaae.data.PREPROCESSING_SCALARS))))
        scaling_group.add_argument(
            "--standardise", "-s",
            dest="scaling_method",
            action="store_const",
            const="standardise",
            default=False,
            help="standardise data set")
        scaling_group.add_argument(
            "--min-max-scale", "--mms",
            dest="scaling_method",
            action="store_const",
            const="min_max_scale",
            default=False,
            help="rescale data set (min-max scaling)")

    analysis_subparser.add_argument(
        "--latent-representation-path", "--lrp",
        dest="latent_representation_path",
        metavar="path",
        type=str,
        default=None,
        help="path to latent representation")
    analysis_subparser.add_argument(
        "--latent-annotations-path", "--lap",
        dest="latent_annotations_path",
        metavar="path",
        type=str,
        default=None,
        help="path to (additional) annotations for latent representation")

    for subparser in (training_subparser, encoding_subparser,
                      evaluation_subparser):
        subparser.add_argument(
            "--batch-size", "-B",
            dest="batch_size",
            metavar="integer",
            type=int,
            default=64,
            help="batch size used for training, encoding, or evaluation")

    training_subparser.add_argument(
        "--ground-truth-annotation", "--gta",
        dest="ground_truth_annotation_key",
        metavar="annotation_name",
        type=str,
        default=None,
        help=(
            "name of annotation used as ground truth, "
            "if none is provided, tries to infer one from data set"))
    training_subparser.add_argument(
        "--ground-truth-representation", "--gtr",
        dest="ground_truth_representation_key",
        metavar="representation_name",
        type=str,
        default=None,
        help=(
            "name of representation used as reference "
            "for unsupervised metrics"))
    training_subparser.add_argument(
        "--validation-path", "--vp",
        dest="validation_path",
        metavar="path",
        type=str,
        default=None,
        help="path to validation set")
    training_subparser.add_argument(
        "--model-kind", "--mk",
        dest="model_kind",
        metavar="kind",
        type=str,
        default="base",
        help=(
            "kind of model to use, options: "
            + ", ".join(list(scaae.models.MODELS))
            + " (experimental)"))
    training_subparser.add_argument(
        "--intermediate-sizes", "-I",
        dest="intermediate_sizes",
        metavar="integer",
        type=int,
        nargs="+",
        default=None,
        help=(
            "size(s) of intermediate layer(s), "
            "overrides model default and model configuration value"))
    training_subparser.add_argument(
        "--discriminator-intermediate-sizes", "-D",
        dest="discriminator_intermediate_sizes",
        metavar="integer",
        type=int,
        nargs="+",
        default=None,
        help=(
            "size(s) of discriminator intermediate layer(s), "
            "overrides model default and model configuration value"))
    training_subparser.add_argument(
        "--latent-size", "-L",
        dest="latent_size",
        metavar="integer",
        type=int,
        default=None,
        help=(
            "number of dimensions for latent represenation, "
            "overrides model default and model configuration value"))
    training_subparser.add_argument(
        "--category-count", "-K",
        dest="category_count",
        metavar="integer",
        type=int,
        default=None,
        help=(
            "number of categories for categorical model (experimental), "
            "overrides model default and model configuration value"))
    training_subparser.add_argument(
        "--model-config-path", "-m",
        dest="model_config",
        metavar="path",
        type=str,
        default=None,
        help="path to model configuration")
    training_subparser.add_argument(
        "--optimiser",
        dest="optimiser",
        metavar="optimiser_name",
        type=str,
        default=None,
        help=(
            "name of optimiser for model, "
            "overrides optimiser default and optimiser configuration value"))
    training_subparser.add_argument(
        "--autoencoder-learning-rate", "--alr",
        dest="autoencoder_learning_rate",
        metavar="real_number",
        type=float,
        default=None,
        help=(
            "learning rate for autoencoder, "
            "overrides optimiser default and optimiser configuration value"))
    training_subparser.add_argument(
        "--discriminator-learning-rate", "--dlr",
        dest="discriminator_learning_rate",
        metavar="real_number",
        type=float,
        default=None,
        help=(
            "learning rate for discriminator, "
            "overrides optimiser default and optimiser configuration value"))
    training_subparser.add_argument(
        "--generator-learning-rate", "--glr",
        dest="generator_learning_rate",
        metavar="real_number",
        type=float,
        default=None,
        help=(
            "learning rate for generator, "
            "overrides optimiser default and optimiser configuration value"))
    training_subparser.add_argument(
        "--learning-decay-rate", "--ldr",
        dest="learning_decay_rate",
        metavar="real_number",
        type=float,
        default=None,
        help=(
            "learning rate decay for model, "
            "overrides optimiser default and optimiser configuration value"))
    training_subparser.add_argument(
        "--gradient-clipping-norm", "--gn",
        dest="gradient_clipping_norm",
        metavar="real_number",
        type=float,
        default=None,
        help=(
            "norm to use for gradient clipping, "
            "overrides optimiser default and optimiser configuration value"))
    training_subparser.add_argument(
        "--gradient-clipping-value", "--gv",
        dest="gradient_clipping_value",
        metavar="real_number",
        type=float,
        default=None,
        help=(
            "value to use for gradient clipping, "
            "overrides optimiser default and optimiser configuration value"))
    training_subparser.add_argument(
        "--optimisation-config-path", "--oc",
        dest="optimisation_config",
        metavar="path",
        type=str,
        default=None,
        help="path to optimiser configuration")
    training_subparser.add_argument(
        "--number-of-epochs", "-E",
        dest="epoch_count",
        metavar="integer",
        type=int,
        default=100,
        help="number of epochs for which to train")
    training_subparser.add_argument(
        "--early-stopping-loss", "--es",
        dest="early_stopping_loss",
        metavar="loss_name|metric_name",
        type=str,
        default=None,
        help="name of loss or metric to monitor for early stopping")
    training_subparser.add_argument(
        "--early-stopping-patience", "--esp",
        dest="early_stopping_patience",
        metavar="integer",
        type=int,
        default=25,
        help=(
            "number of epochs for which to continue training, "
            "if loss or metric monitored for early stopping does not improve"))
    training_subparser.add_argument(
        "--early-stopping-initial-delay", "--esid",
        dest="early_stopping_initial_delay",
        metavar="integer",
        type=int,
        default=None,
        help=(
            "number of epochs for which to train initially before "
            "employing early stopping"))
    training_subparser.add_argument(
        "--convergence-stopping-loss-pattern", "--sc",
        dest="convergence_stopping_loss_pattern",
        metavar="pattern",
        type=str,
        default=None,
        help=(
            "regular expression pattern for loss and/or metric names "
            "to monitor for convergence stopping (experimental)"))
    training_subparser.add_argument(
        "--convergence-stopping-threshold", "--cst",
        dest="convergence_stopping_threshold",
        metavar="real_number",
        type=float,
        default=0.0001,
        help=(
            "threshold for determining convergence for "
            "losses and/or metrics monitored for convergence stopping"
            "(experimental)"))
    training_subparser.add_argument(
        "--convergence-stopping-window-size", "--csws",
        dest="convergence_stopping_window_size",
        metavar="integer",
        type=int,
        default=10,
        help=(
            "number of previous epochs to consider when "
            "determining convergence for losses and/or metrics monitored "
            "for convergence stopping (experimental)"))
    training_subparser.add_argument(
        "--plot",
        dest="plotting",
        action="store_true",
        default=False,
        help="plot intermediate analyses if output directory is provided")
    training_subparser.add_argument(
        "--log",
        dest="logging_options",
        metavar="option",
        type=str,
        nargs="+",
        default=None,
        help=(
            "log extra information if output directory is provided, "
            "options: tensorboard, callback_durations"))
    training_subparser.add_argument(
        "--eagerly",
        dest="eagerly",
        action="store_true",
        default=False,
        help="run model using TensorFlow eager execution to help debugging")

    for subparser in (training_subparser, analysis_subparser,
                      evaluation_subparser):
        subparser.add_argument(
            "--clustering-methods", "-c",
            dest="clustering_methods",
            metavar="method_name",
            type=str,
            nargs="+",
            default=None,
            help=(
                "name(s) of method(s) to use for clustering, options: "
                + ", ".join(list(scaae.analyses.LATENT_CLUSTERERS))))
        subparser.add_argument(
            "--clustering-resolutions", "--cr",
            dest="clustering_resolutions",
            metavar="real_number",
            type=float,
            nargs="+",
            default=None,
            help="resolution(s) for clustering method(s)")
        subparser.add_argument(
            "--clustering-neighbourhood-sizes", "--cn",
            dest="clustering_neighbourhood_sizes",
            metavar="integer",
            type=int,
            nargs="+",
            default=None,
            help="neighbourhood size(s) for clustering method(s)")
        subparser.add_argument(
            "--clustering-principal-component-counts", "--cp",
            dest="clustering_principal_component_counts",
            metavar="integer",
            type=int,
            nargs="+",
            default=None,
            help="number of principal component(s) for clustering method(s)")

    training_subparser.add_argument(
        "--clustering-metric-aggregator", "--ca",
        dest="clustering_metric_aggregator",
        metavar="aggregator_name",
        type=str,
        default="optimum",
        help=(
            "name of aggregator for clustering metric(s) evaluated "
            "during training"))

    for subparser in (analysis_subparser, evaluation_subparser):
        subparser.add_argument(
            "--clustering-metrics", "--cm",
            dest="clustering_metrics",
            metavar="metric_name",
            type=str,
            nargs="+",
            default=None,
            help=(
                "name(s) of clustering metric(s) to evaluate, options: "
                + ", ".join(list(scaae.analyses.CLUSTERING_METRICS))))
        subparser.add_argument(
            "--clustering-metric-sort-order", "--cs",
            dest="clustering_sort_keys",
            metavar="metric_name",
            type=str,
            nargs="+",
            default=None,
            help=(
                "order of clustering metric(s) by which to sort metrics, "
                "if none are provided, default sort order is used"))
        subparser.add_argument(
            "--sankey-ground-truth-order", "--sgto",
            dest="sankey_ground_truth_order",
            metavar="annotation_name",
            type=str,
            nargs="+",
            default=None,
            help=(
                "order of ground truth annotation(s) for Sankey diagram, "
                "if provided produces Sankey diagram (experimental)"))
        subparser.add_argument(
            "--decomposition-methods", "-d",
            dest="decomposition_methods",
            metavar="method_name",
            type=str,
            nargs="+",
            default=None,
            help=(
                "name(s) of method(s) used for decomposition when plotting"
                "high-dimensional latent representation, options: "
                + ", ".join(list(scaae.analyses.LATENT_DECOMPOSERS))))
        subparser.add_argument(
            "--latent-clustering-plot-limit", "--lcpl",
            dest="latent_clustering_plot_limit",
            metavar="integer",
            type=int,
            default=None,
            help=(
                "number of latent clusterings to use for plotting, "
                "sorted by clustering metric sort order"
            ))
        subparser.add_argument(
            "--include-latent-clustering-plot-median", "--ilcpm",
            dest="latent_clustering_plot_median",
            action="store_true",
            default=False,
            help=(
                "include median latent clustering when plotting, "
                "according to each clustering metric in sort order"))

    for subparser in (training_subparser, analysis_subparser,
                      evaluation_subparser):
        plot_annotations_group = subparser.add_mutually_exclusive_group()
        plot_annotations_group.add_argument(
            "--plot-annotation-match-patterns", "--pamp",
            dest="plot_annotation_key_match_patterns",
            metavar="pattern",
            type=str,
            nargs="+",
            default=None,
            help=(
                "regular expression pattern(s) for annotation(s) to plot, "
                "if none are provided, all numeric and categorical "
                "annotations are used"))
        plot_annotations_group.add_argument(
            "--plot-annotation-ignore-patterns", "--paip",
            dest="plot_annotation_key_ignore_patterns",
            metavar="pattern",
            type=str,
            nargs="+",
            default=None,
            help=(
                "regular expression pattern(s) for annotation(s) to not plot, "
                "if none are provided, all numeric and categorical "
                "annotations are used"))

    for subparser in (analysis_subparser, evaluation_subparser):
        ground_truth_annotations_group = (
            subparser.add_mutually_exclusive_group())
        ground_truth_annotations_group.add_argument(
            "--ground-truth-annotation-match-patterns", "--gtamp",
            dest="ground_truth_annotation_key_match_patterns",
            metavar="pattern",
            type=str,
            nargs="+",
            default=None,
            help=(
                "regular expression pattern(s) for annotation(s) "
                "to use as ground truth, "
                "if none are provided, all categorical annotations are used"))
        ground_truth_annotations_group.add_argument(
            "--ground-truth-annotation-ignore-patterns", "--gtaip",
            dest="ground_truth_annotation_key_ignore_patterns",
            metavar="pattern",
            type=str,
            nargs="+",
            default=None,
            help=(
                "regular expression pattern(s) for annotation(s) "
                "to not use as ground truth, "
                "if none are provided, all categorical annotations are used"))

    evaluation_subparser.add_argument(
        "--skip-saving-latent-representation", "--sslr",
        dest="save_latent_representation",
        action="store_false",
        default=True,
        help="do not save latent representation")

    for subparser in (training_subparser, analysis_subparser,
                      evaluation_subparser):
        subparser.add_argument(
            "--dense-memory-limit-in-gigabytes", "--dml",
            dest="dense_memory_limit_in_gigabytes",
            metavar="integer",
            type=float,
            default=scaae.utilities.DEFAULT_MEMORY_LIMIT_IN_GIGABYTES,
            help="memory limit (in GB) for caching dense matrices")

    for subparser in (training_subparser, encoding_subparser,
                      analysis_subparser, evaluation_subparser):
        verbosity_group = subparser.add_mutually_exclusive_group()
        verbosity_group.add_argument(
            "--verbose", "-v",
            dest="verbose",
            action="store_const",
            const=2)
        verbosity_group.add_argument(
            "--quiet", "-q",
            dest="verbose",
            action="store_const",
            const=0)
        subparser.set_defaults(verbose=1)

    arguments = parser.parse_args()
    function = arguments.func
    arguments = vars(arguments)
    arguments.pop("func")
    status = function(**arguments)

    return status
