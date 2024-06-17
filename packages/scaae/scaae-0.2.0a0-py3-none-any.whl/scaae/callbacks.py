import functools
import csv
import re
import warnings
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras as tfk

from scaae.models import (
    distributions, utilities as model_utilities, VALIDATION_METRIC_PREFIX)
from scaae.data import utilities as data_utilities
from scaae import analyses, models, statistics, utilities

DEFAULT_EARLY_STOPPING_INITIAL_DELAY = 0


class UpdateHyperparameters(tfk.callbacks.Callback):
    """Updates hyperparameters dependent on the epoch."""

    def on_epoch_begin(self, epoch, logs=None):
        self.model.update_hyperparameters(epoch=epoch)


class BackUpAndRestore(tfk.callbacks.ModelCheckpoint):
    """Backups model config and weights and restores weights."""

    def __init__(self,
                 directory,
                 config_name="config",
                 weights_name="weights",
                 restore_when_training=True,
                 restore_when_evaluating=False,
                 restore_when_predicting=False,
                 verbose=0):

        self.directory = utilities.check_path(directory)
        config_filename = f"{config_name}.json"
        self.config_path = self.directory.joinpath(config_filename)
        weights_basename = weights_name + "-epoch_{epoch}"
        self.weight_basename_prefix = weights_basename.format(epoch="")
        self.restore_when_training = restore_when_training
        self.restore_when_evaluating = restore_when_evaluating
        self.restore_when_predicting = restore_when_predicting

        self.started = False

        super().__init__(
            filepath=self.directory.joinpath(weights_basename),
            monitor="",
            verbose=verbose,
            save_best_only=False,
            save_weights_only=True,
            mode="auto",
            save_freq="epoch",
            options=None)

    def on_train_begin(self, logs=None):
        super().on_train_begin(logs=logs)
        self.directory.mkdir(parents=True, exist_ok=True)
        self._check_or_save_model_config()
        if self.restore_when_training:
            self._load_weights_if_present()

    def on_test_begin(self, logs=None):
        super().on_test_begin(logs=logs)
        self._check_or_save_model_config()
        if self.restore_when_evaluating:
            self._load_weights_if_present()

    def on_predict_begin(self, logs=None):
        super().on_predict_begin(logs=logs)
        self._check_or_save_model_config()
        if self.restore_when_predicting:
            self._load_weights_if_present()

    def on_epoch_end(self, epoch, logs=None):
        if (self.model.stop_training and
                self.model.stopped_early_with_weights_from_epoch is not None):
            epoch = self.model.stopped_early_with_weights_from_epoch
        super().on_epoch_end(epoch=epoch, logs=logs)
        if self.started:
            self._remove_old_checkpoints()
        else:
            self.started = True

    def on_train_end(self, logs=None):
        super().on_train_end(logs=logs)
        self._remove_old_checkpoints()

    def initial_epoch(self):
        weights_path = tf.train.latest_checkpoint(self.directory)
        if weights_path:
            initial_epoch = self._epoch_from_checkpoint_path(weights_path)
        else:
            initial_epoch = 0
        return initial_epoch

    def _check_or_save_model_config(self):
        model_config = self.model.get_config()
        if self.config_path.exists():
            loaded_config = model_utilities.load_model_config(self.config_path)
            if not loaded_config == model_config:
                raise Exception(
                    "The restored model configuration does not match "
                    "the current model configuration.")
        else:
            model_utilities.save_model_config(
                model_config, path=self.config_path)

    def _load_weights_if_present(self):
        weights_path = tf.train.latest_checkpoint(self.directory)
        if weights_path:
            self.model.load_weights(weights_path).expect_partial()

    def _remove_old_checkpoints(self):
        latest_checkpoint_path_prefix = tf.train.latest_checkpoint(
            self.directory)
        if latest_checkpoint_path_prefix:
            all_checkpoint_paths = self.directory.glob(
                f"{self.weight_basename_prefix}*")
            for path in all_checkpoint_paths:
                if not path.match(f"{latest_checkpoint_path_prefix}*"):
                    path.unlink()

    def _epoch_from_checkpoint_path(self, path):
        path_prefix = self.directory.joinpath(self.weight_basename_prefix)
        match = re.match(
            r"(\d+).*", utilities.remove_prefix(str(path), str(path_prefix)))
        epoch = int(match.group(1))
        return epoch


class AdditionalMetrics(tfk.callbacks.Callback):
    """Computes additional metrics."""

    def __init__(self,
                 data_set=None,
                 clustering_methods=None,
                 clustering_resolutions=None,
                 clustering_neighbourhood_sizes=None,
                 clustering_principal_component_counts=None,
                 ground_truth_annotation_key=None,
                 ground_truth_representation_key=None,
                 clustering_metric_aggregator="median",
                 batch_size=64,
                 printer_verbose=0,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_set = data_set
        self.clustering_methods = clustering_methods
        self.clustering_resolutions = clustering_resolutions
        self.clustering_neighbourhood_sizes = clustering_neighbourhood_sizes
        self.clustering_principal_component_counts = (
            clustering_principal_component_counts)
        self.ground_truth_annotation_key = ground_truth_annotation_key
        self.ground_truth_representation_key = ground_truth_representation_key
        self.clustering_metric_aggregator = clustering_metric_aggregator
        self.batch_size = batch_size
        self.printer = utilities.Printer(printer_verbose)

    def set_data_set(self, data_set):
        self.data_set = data_set

    def additional_metrics_at_epoch_end(self, epoch=None, logs=None):
        return set()

    def maybe_compute_additional_metrics(self, epoch, logs=None):
        logs = logs or None
        metric_names = self.additional_metrics_at_epoch_end(
            epoch=epoch, logs=logs)
        clustering_metric_names = analyses.clustering_metric_names(
            metric_names)
        if clustering_metric_names:
            data_set_name = None
            if self.data_set is not None:
                data_set_name = self.data_set.uns.get("name")
            self.printer.print(utilities.compose_message(
                "Computing clustering metrics",
                "for" if data_set_name is not None else None,
                data_set_name, ":"))
            clustering_metrics = _encode_cluster_compare(
                adversarial_autoencoder=self.model,
                data_set=self.data_set,
                clustering_metric_names=clustering_metric_names,
                clustering_methods=self.clustering_methods,
                clustering_resolutions=self.clustering_resolutions,
                clustering_neighbourhood_sizes=(
                    self.clustering_neighbourhood_sizes),
                clustering_principal_component_counts=(
                    self.clustering_principal_component_counts),
                original_grouping_key=self.ground_truth_annotation_key,
                representation_key=self.ground_truth_representation_key,
                clustering_metric_aggregator=self.clustering_metric_aggregator,
                encoding_identifier=f"epoch_{epoch + 1}",
                batch_size=self.batch_size,
                verbose=self.printer.verbose)
            logs.update(clustering_metrics)
        return logs


class AdditionalMetricsCallbackList(AdditionalMetrics):
    """Performs common operations for all callbacks."""

    def __init__(self,
                 callbacks,
                 data_set,
                 clustering_methods=None,
                 clustering_resolutions=None,
                 clustering_neighbourhood_sizes=None,
                 clustering_principal_component_counts=None,
                 ground_truth_annotation_key=None,
                 ground_truth_representation_key=None,
                 clustering_metric_aggregator="median",
                 batch_size=64,
                 callback_duration_log_path=None,
                 verbose=0):
        super().__init__(
            data_set=data_set,
            clustering_methods=clustering_methods,
            clustering_resolutions=clustering_resolutions,
            clustering_neighbourhood_sizes=clustering_neighbourhood_sizes,
            clustering_principal_component_counts=(
                clustering_principal_component_counts),
            ground_truth_annotation_key=ground_truth_annotation_key,
            ground_truth_representation_key=ground_truth_representation_key,
            clustering_metric_aggregator=clustering_metric_aggregator,
            batch_size=batch_size,
            printer_verbose=verbose)
        self.callbacks = callbacks or []
        if callback_duration_log_path:
            self.callback_duration_logger = CallbackDurationLogger(
                callbacks=[self] + self.callbacks,
                path=callback_duration_log_path)
        else:
            self.callback_duration_logger = None

    def set_params(self, params):
        super().set_params(params)
        for callback in self.callbacks:
            callback.set_params(params)

    def set_model(self, model):
        super().set_model(model)
        for callback in self.callbacks:
            callback.set_model(model)

    def additional_metrics_at_epoch_end(self, epoch=None, logs=None):
        additional_metrics = set()
        for callback in self.callbacks:
            if isinstance(callback, AdditionalMetrics):
                additional_metrics_for_callback = (
                    callback.additional_metrics_at_epoch_end(
                        epoch=epoch, logs=logs))
                if additional_metrics_for_callback:
                    additional_metrics_for_callback = utilities.check_set(
                        additional_metrics_for_callback)
                    additional_metrics.update(
                        additional_metrics_for_callback)
        return additional_metrics

    def on_batch_begin(self, batch, logs=None):
        for callback in self.callbacks:
            callback.on_batch_begin(batch, logs=logs)

    def on_batch_end(self, batch, logs=None):
        for callback in self.callbacks:
            callback.on_batch_end(batch, logs=logs)

    def on_epoch_begin(self, epoch, logs=None):
        if self.callback_duration_logger:
            self.callback_duration_logger.reset(epoch=epoch)
        for callback in self.callbacks:
            with utilities.Stopwatch() as stopwatch:
                callback.on_epoch_begin(epoch, logs=logs)
            if self.callback_duration_logger:
                self.callback_duration_logger.add(
                    callback, duration=stopwatch.duration)

    def on_epoch_end(self, epoch, logs=None):
        if self.callback_duration_logger:
            self.callback_duration_logger.check_epoch(epoch=epoch)
        with utilities.Stopwatch() as stopwatch:
            logs = self.maybe_compute_additional_metrics(epoch, logs=logs)
        if self.callback_duration_logger:
            self.callback_duration_logger.add(
                callback=self, duration=stopwatch.duration)
        for callback in self.callbacks:
            with utilities.Stopwatch() as stopwatch:
                callback.on_epoch_end(epoch, logs=logs)
            if self.callback_duration_logger:
                self.callback_duration_logger.add(
                    callback, duration=stopwatch.duration)
        if self.callback_duration_logger:
            self.callback_duration_logger.log(epoch=epoch)

    def on_train_batch_begin(self, batch, logs=None):
        for callback in self.callbacks:
            callback.on_train_batch_begin(batch, logs=logs)

    def on_train_batch_end(self, batch, logs=None):
        for callback in self.callbacks:
            callback.on_train_batch_end(batch, logs=logs)

    def on_test_batch_begin(self, batch, logs=None):
        for callback in self.callbacks:
            callback.on_test_batch_begin(batch, logs=logs)

    def on_test_batch_end(self, batch, logs=None):
        for callback in self.callbacks:
            callback.on_test_batch_end(batch, logs=logs)

    def on_predict_batch_begin(self, batch, logs=None):
        for callback in self.callbacks:
            callback.on_predict_batch_begin(batch, logs=logs)

    def on_predict_batch_end(self, batch, logs=None):
        for callback in self.callbacks:
            callback.on_predict_batch_end(batch, logs=logs)

    def on_train_begin(self, logs=None):
        if self.callback_duration_logger:
            self.callback_duration_logger.reset(epoch="start")
            self.callback_duration_logger.set_up_writer()
        for callback in self.callbacks:
            with utilities.Stopwatch() as stopwatch:
                callback.on_train_begin(logs=logs)
            if self.callback_duration_logger:
                self.callback_duration_logger.add(
                    callback, duration=stopwatch.duration)
        if self.callback_duration_logger:
            self.callback_duration_logger.log()

    def on_train_end(self, logs=None):
        if self.callback_duration_logger:
            self.callback_duration_logger.reset(epoch="end")
        for callback in self.callbacks:
            with utilities.Stopwatch() as stopwatch:
                callback.on_train_end(logs=logs)
            if self.callback_duration_logger:
                self.callback_duration_logger.add(
                    callback, duration=stopwatch.duration)
        if self.callback_duration_logger:
            self.callback_duration_logger.log()
            self.callback_duration_logger.reset_writer()

    def on_test_begin(self, logs=None):
        for callback in self.callbacks:
            callback.on_test_begin(logs=logs)

    def on_test_end(self, logs=None):
        for callback in self.callbacks:
            callback.on_test_end(logs=logs)

    def on_predict_begin(self, logs=None):
        for callback in self.callbacks:
            callback.on_predict_begin(logs=logs)

    def on_predict_end(self, logs=None):
        for callback in self.callbacks:
            callback.on_predict_end(logs=logs)


class CallbackDurationLogger:
    """Logs durations for callbacks during training."""

    def __init__(self, callbacks, path):
        self.durations = {}
        self.epoch = self.epoch_start_time = self.epoch_end_time = None
        self.finalised = False
        self.callback_names = list(map(_class_name, callbacks))
        self.path = utilities.check_path(path)
        self.writer = None

    def reset(self, epoch=None, start_of_epoch=True):
        self.durations = {}
        if epoch is not None:
            self.epoch = epoch
            if start_of_epoch:
                self.epoch_start_time = datetime.now(timezone.utc)
            else:
                self.epoch_start_time = None
        else:
            self.epoch = self.epoch_start_time = None
        self.epoch_end_time = None
        self.finalised = False

    def add(self, callback, duration):
        callback_name = _class_name(callback)
        self.durations.setdefault(callback_name, 0.0)
        self.durations[callback_name] += duration

    def finalise(self, epoch=None):
        self.epoch_end_time = datetime.now(timezone.utc)
        self.finalised = True

    def check_epoch(self, epoch=None):
        if epoch is not None:
            if self.epoch is not None:
                if epoch != self.epoch:
                    warnings.warn(
                        f"Passed epoch ({epoch}) for callback durations "
                        f"does not match recorded epoch ({self.epoch}) "
                        "at last duration reset. Resetting with passed epoch.")
                    self.reset(epoch=epoch, start_of_epoch=False)
            else:
                self.epoch = epoch
                self.epoch_start_time = None

    def log(self, epoch=None):
        self.check_epoch(epoch=epoch)

        if not self.finalised:
            self.finalise()

        if not self.writer:
            self.set_up_writer()

        row = self._build_row()
        self.writer.writerow(row)
        self.file.flush()

    def set_up_writer(self):
        if self.path.exists():
            with self.path.open(mode="r") as f:
                file_empty = not bool(len(f.readline()))
        else:
            file_empty = True
        self.file = self.path.open(mode="a")

        field_names = self._build_row().keys()

        self.writer = csv.DictWriter(self.file, fieldnames=field_names)
        if file_empty:
            self.writer.writeheader()

    def reset_writer(self):
        self.file.close()
        self.writer = None

    def _build_row(self):
        row = {
            "epoch": self.epoch,
            "start_time": self.epoch_start_time,
            "end_time": self.epoch_end_time}
        row.update({
            name: self.durations.get(name) for name in self.callback_names})
        return row


class EarlyStopping(AdditionalMetrics, tfk.callbacks.EarlyStopping):
    """Stops early when a monitored metric have stopped improving."""
    _MODES = {
        analyses.BestDirection.POSITIVE: "max",
        analyses.BestDirection.NEGATIVE: "min"}
    _WORST_VALUE_FOR_DIRECTION = {
        analyses.BestDirection.POSITIVE: "minimum",
        analyses.BestDirection.NEGATIVE: "maximum"}

    def __init__(self,
                 initial_delay=None,
                 evaluate_during_delay=False,
                 data_set=None,
                 clustering_methods=None,
                 clustering_resolutions=None,
                 clustering_neighbourhood_sizes=None,
                 clustering_principal_component_counts=None,
                 ground_truth_annotation_key=None,
                 ground_truth_representation_key=None,
                 clustering_metric_aggregator="median",
                 batch_size=64,
                 verbose=0,
                 **kwargs):
        self.initial_delay = (
            initial_delay if initial_delay is not None
            else DEFAULT_EARLY_STOPPING_INITIAL_DELAY)
        self.evaluate_during_delay = evaluate_during_delay
        mode = kwargs.get("mode")
        if mode and mode == "auto":
            monitor = kwargs.get("monitor")
            if monitor:
                monitor = utilities.remove_prefix(
                    monitor, prefix=VALIDATION_METRIC_PREFIX)
                if monitor in analyses.CLUSTERING_METRICS:
                    best_direction = analyses.clustering_metric_attribute(
                        monitor, "best_direction")
                elif "loss" in monitor:
                    best_direction = analyses.BestDirection.NEGATIVE
                elif "acc" in monitor:
                    best_direction = analyses.BestDirection.POSITIVE
                else:
                    best_direction = None
                if best_direction:
                    mode = self._MODES[best_direction]
                    kwargs["mode"] = mode
        super().__init__(
            data_set=data_set,
            clustering_methods=clustering_methods,
            clustering_resolutions=clustering_resolutions,
            clustering_neighbourhood_sizes=clustering_neighbourhood_sizes,
            clustering_principal_component_counts=(
                clustering_principal_component_counts),
            ground_truth_annotation_key=ground_truth_annotation_key,
            ground_truth_representation_key=ground_truth_representation_key,
            clustering_metric_aggregator=clustering_metric_aggregator,
            batch_size=batch_size,
            printer_verbose=verbose,
            verbose=0,
            **kwargs)
        self.stopped_early_with_weights_from_epoch = None

    def additional_metrics_at_epoch_end(self, epoch=None, logs=None):
        logs = logs or {}
        additional_metrics = set()
        if self.monitor not in logs and (
                epoch is not None and epoch >= self.initial_delay
                or epoch is None or self.evaluate_during_delay):
            base_metric_name = utilities.remove_prefix(
                self.monitor, prefix=VALIDATION_METRIC_PREFIX)
            if base_metric_name in analyses.CLUSTERING_METRICS:
                additional_metrics.add(self.monitor)
        if additional_metrics and self.data_set is None:
            raise ValueError(
                "Please provide data set to stop early using "
                f"\"{self.monitor}\".")
        return additional_metrics

    def on_epoch_end(self, epoch, logs=None):
        if epoch >= self.initial_delay:
            logs = self.maybe_compute_additional_metrics(epoch, logs=logs)
            logs = self._replace_na_monitored_clustering_metric_value(logs)
            super().on_epoch_end(epoch=epoch, logs=logs)
        if self.model.stop_training:
            self.model.add_reason_for_stopping_training("Early stopping.")
            if self.restore_best_weights:
                self.stopped_early_with_weights_from_epoch = (
                    self.stopped_epoch - self.wait)
                self.model.stopped_early_with_weights_from_epoch = (
                    self.stopped_early_with_weights_from_epoch)

    def on_train_end(self, logs=None):
        if self.stopped_epoch > 0:
            self.printer.print(
                f"Stopped at epoch {self.stopped_epoch + 1}, "
                "since monitored value has stopped improving.")
        if self.stopped_early_with_weights_from_epoch:
            self.printer.print(
                "Model weights restored from the best epoch, "
                "which was epoch "
                f"{self.stopped_early_with_weights_from_epoch + 1}.")

    def _replace_na_monitored_clustering_metric_value(self, logs=None):
        logs = logs or {}
        if (self.monitor in logs
                and self.monitor in analyses.CLUSTERING_METRICS):
            monitor_value = logs[self.monitor]
            if np.isnan(monitor_value):
                best_direction = analyses.clustering_metric_attribute(
                    self.monitor, "best_direction")
                value_extrema = analyses.clustering_metric_extrema(
                    self.monitor, dtype="float")
                worst_value = value_extrema[
                    self._WORST_VALUE_FOR_DIRECTION[best_direction]]
                logs[self.monitor] = worst_value
        return logs


class StopAtConvergence(AdditionalMetrics):
    """Stops training when monitored metrics have stopped changing."""

    def __init__(self,
                 monitor_pattern=r".+loss",
                 threshold=1e-6,
                 window_size=10,
                 smoothing_method=None,
                 smoothing_kwargs=None,
                 data_set=None,
                 clustering_methods=None,
                 clustering_resolutions=None,
                 clustering_neighbourhood_sizes=None,
                 clustering_principal_component_counts=None,
                 ground_truth_annotation_key=None,
                 ground_truth_representation_key=None,
                 clustering_metric_aggregator="median",
                 batch_size=64,
                 verbose=0):

        super().__init__(
            data_set=data_set,
            clustering_methods=clustering_methods,
            clustering_resolutions=clustering_resolutions,
            clustering_neighbourhood_sizes=clustering_neighbourhood_sizes,
            clustering_principal_component_counts=(
                clustering_principal_component_counts),
            ground_truth_annotation_key=ground_truth_annotation_key,
            ground_truth_representation_key=ground_truth_representation_key,
            clustering_metric_aggregator=clustering_metric_aggregator,
            batch_size=batch_size,
            printer_verbose=verbose)

        self.monitor_pattern = monitor_pattern
        self.threshold = abs(threshold)
        self.window_size = window_size
        self.smoothing_method = smoothing_method
        self.smoothing_kwargs = utilities.check_dict(smoothing_kwargs)

        self._reset()

        self.smooth = None
        if self.smoothing_method is not None:
            self.smooth = functools.partial(
                statistics.get_smoothing_function(self.smoothing_method),
                **self.smoothing_kwargs)

    def additional_metrics_at_epoch_end(self, epoch, logs=None):
        logs = logs or {}
        base_metric_pattern = utilities.remove_prefix(
            self.monitor_pattern, prefix=VALIDATION_METRIC_PREFIX)
        if self.monitor_pattern.startswith(VALIDATION_METRIC_PREFIX):
            metric_prefix = VALIDATION_METRIC_PREFIX
        else:
            metric_prefix = ""
        additional_metrics = {
            f"{metric_prefix}{metric_name}"
            for metric_name in analyses.CLUSTERING_METRICS
            if re.match(pattern=base_metric_pattern, string=metric_name)
            if metric_name not in logs}
        if additional_metrics and self.data_set is None:
            raise ValueError(
                "Please provide data set to stop at convergence using "
                "metrics mathcing pattern "
                f"\"{self.monitor_pattern}\".")
        return additional_metrics

    def on_train_begin(self, logs=None):
        self._reset()

    def on_epoch_end(self, epoch, logs=None):
        logs = self.maybe_compute_additional_metrics(epoch, logs=logs)
        self._update_history(logs)
        self._update_convergence()
        if all(self.converged.values()):
            self.stopped_epoch = epoch
            self.model.stop_training = True
            self.model.add_reason_for_stopping_training(
                "Monitored values seem to have converged.")

    def on_train_end(self, logs=None):
        if self.stopped_epoch:
            self.printer.print(
                f"Stopped at epoch {self.stopped_epoch + 1}, "
                "since monitored values seem to have converged.")

    def _update_history(self, logs=None):
        logs = logs or {}
        for metric_name, metric_value in logs.items():
            if re.match(pattern=self.monitor_pattern, string=metric_name):
                self.history.setdefault(metric_name, [])
                self.history[metric_name].append(metric_value)

        if len(self.history) == 0:
            available_metrics = ", ".join(list(logs.keys()))
            raise ValueError(
                "No metrics matching monitor pattern "
                f"`{self.monitor_pattern}`. "
                f"Available metrics are: {available_metrics}.")

    def _update_convergence(self):
        for metric_name, metric_history in self.history.items():
            self.converged.setdefault(metric_name, False)
            if len(metric_history) >= self.window_size:
                if self.smooth:
                    metric_history = self.smooth(metric_history)
                recent_metric_history = metric_history[-self.window_size - 2:]
                differences = np.gradient(recent_metric_history, edge_order=2)
                differences = differences[-self.window_size:]
                self.converged[metric_name] = all(
                    np.fabs(differences) < self.threshold)

    def _reset(self):
        self.history = {}
        self.converged = {}
        self.stopped_epoch = None


class History(tfk.callbacks.Callback):
    def __init__(self):
        super().__init__()
        self.history = []

    def on_train_begin(self, logs=None):
        self.history = []

    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}
        record = {"epoch": epoch}
        record.update(logs)
        self.history.append(record)


class LearningCurvePlotter(History):
    """Plots learning curves of a model."""

    def __init__(self, output_directory, base_name="learning_curves"):
        super().__init__()
        self.output_directory = utilities.check_path(output_directory)
        self.base_name = base_name
        self.path = None

    def on_epoch_end(self, epoch, logs=None):
        super().on_epoch_end(epoch=epoch, logs=logs)
        if self.path is None:
            base_name = f"{self.base_name}-initial_epoch_{epoch + 1}"
            self.path = self.output_directory.joinpath(f"{base_name}.png")
        history = pd.DataFrame(self.history).set_index("epoch").sort_index()
        analyses.plot_learning_curves(
            history,
            metric_groups=self.model.metric_groups,
            path=self.path)


class ScheduledCallback(tfk.callbacks.Callback):
    def __init__(self, function, schedule=None):
        super().__init__()
        self.function = function
        if schedule is None:
            schedule = self._default_schedule
        self.schedule = schedule

    def on_epoch_end(self, epoch, logs=None):
        if self.schedule(epoch):
            self.function(epoch=epoch, logs=logs)

    @staticmethod
    def _default_schedule(epoch):
        return (
            epoch < 10
            or epoch < 200 and (epoch + 1) % 10 == 0
            or epoch < 1000 and (epoch + 1) % 50 == 0
            or epoch > 1000 and (epoch + 1) % 100 == 0)


class LatentSpacePlotter(ScheduledCallback):
    """Plots latent space of a latent-variable model."""

    def __init__(self,
                 data_set,
                 output_directory,
                 annotation_key_match_patterns=None,
                 annotation_key_ignore_patterns=None,
                 base_name="latent_space",
                 schedule=None,
                 batch_size=64,
                 verbose=0):
        super().__init__(function=self._plot, schedule=schedule)
        self.data_set = data_set
        self.output_directory = utilities.check_path(output_directory)
        self.annotation_key_match_patterns = annotation_key_match_patterns
        self.annotation_key_ignore_patterns = annotation_key_ignore_patterns
        self.base_name = base_name
        self.batch_size = batch_size
        self.printer = utilities.Printer(verbose)

    def _plot(self, epoch=None, logs=None):
        identifier = _epoch_identifier(epoch)
        data_set_name = None
        if self.data_set is not None:
            data_set_name = self.data_set.uns.get("name")
        self.printer.print(utilities.compose_message(
            "Plotting latent representation",
            "of" if data_set_name is not None else None, data_set_name,
            "at end of training" if epoch == "end" else "", ":"))
        _encode(
            adversarial_autoencoder=self.model,
            data_set=self.data_set,
            identifier=identifier,
            batch_size=self.batch_size,
            verbose=self.printer.verbose)
        decomposition_method = self._decomposition_method()
        plottable_annotation_keys = data_utilities.plottable_annotation_keys(
            self.data_set.obs,
            match_patterns=self.annotation_key_match_patterns,
            ignore_patterns=self.annotation_key_ignore_patterns)
        path = self.output_directory.joinpath(
            f"{self.base_name}-{identifier}.png")
        analyses.plot_latent_representation(
            self.data_set, annotation_keys=plottable_annotation_keys,
            decomposition_method=decomposition_method, path=path)

    def _decomposition_method(self):
        latent_size = self.model.latent_size
        if latent_size == 1:
            raise ValueError("Cannot plot 1-d latent representation.")
        elif latent_size == 2:
            decomposition_method = None
        else:
            decomposition_method = "pca"
        return decomposition_method


class TrueDistributionParameterPlotter(ScheduledCallback):
    """Plots the parameters of the the true distribution."""

    def __init__(self, output_directory, base_name="true_distribution",
                 schedule=None):
        super().__init__(function=self._plot, schedule=schedule)
        self.output_directory = utilities.check_path(output_directory)
        self.base_name = base_name

    def _plot(self, epoch=None, logs=None):
        identifier = _epoch_identifier(epoch)
        true_distribution = self.model.true_distribution
        if isinstance(
                true_distribution, distributions.NormalMixtureDistribution):
            path = self.output_directory.joinpath(
                f"{self.base_name}-{identifier}.png")
            analyses.plot_normal_mixture_components(
                coefficients=true_distribution.coefficients(),
                means=true_distribution.means(),
                covariances=true_distribution.covariances(),
                path=path)


def _epoch_identifier(epoch):
    if isinstance(epoch, int):
        identifier = f"epoch_{epoch + 1}"
    elif isinstance(epoch, str):
        identifier = f"epoch_{epoch}"
    else:
        raise TypeError(f"Cannot parse epoch of type `{type(epoch)}`.")
    return identifier


class StopOnInvalidLoss(tfk.callbacks.Callback):
    """Stops when an invalid loss or metric is encountered."""

    def __init__(self, verbose=0):
        super().__init__()
        self.verbose = verbose

    def on_train_batch_end(self, batch, logs=None):
        self._check_batch_logs(mode="train", batch=batch, logs=logs)

    def on_test_batch_end(self, batch, logs=None):
        self._check_batch_logs(mode="test", batch=batch, logs=logs)

    def on_predict_batch_end(self, batch, logs=None):
        self._check_batch_logs(mode="predict", batch=batch, logs=logs)

    def _check_batch_logs(self, mode, batch, logs=None):
        modes = ["train", "test", "predict"]
        if mode not in modes:
            raise ValueError(f"`mode` shoud be {'/'.join(modes)}.")
        for loss_name, loss in logs.items():
            if np.isnan(loss) or np.isinf(loss):
                self.model.stop_training = True
                reason = (
                    f"Stopping {mode}ing; invalid losses and/or metrics for "
                    f"batch {batch}: {logs}.")
                self.model.add_reason_for_stopping_training(reason)
                if self.verbose > 0:
                    print(reason)


class TrainingInfoLogger(tfk.callbacks.Callback):
    """Logs training configuration and status for model."""

    def __init__(self, batch_size, total_epoch_count,
                 early_stopping_loss, early_stopping_patience,
                 early_stopping_initial_delay,
                 convergence_stopping_loss_pattern,
                 convergence_stopping_threshold,
                 convergence_stopping_window_size,
                 clustering_methods,
                 clustering_resolutions,
                 clustering_neighbourhood_sizes,
                 clustering_principal_component_counts,
                 ground_truth_annotation_key,
                 ground_truth_representation_key,
                 clustering_metric_aggregator,
                 output_directory, base_name="training_config"):
        self.batch_size = batch_size
        self.total_epoch_count = total_epoch_count
        self.early_stopping_loss = early_stopping_loss
        self.early_stopping_patience = early_stopping_patience
        self.early_stopping_initial_delay = early_stopping_initial_delay
        self.convergence_stopping_loss_pattern = (
            convergence_stopping_loss_pattern)
        self.convergence_stopping_threshold = convergence_stopping_threshold
        self.convergence_stopping_window_size = (
            convergence_stopping_window_size)
        self.clustering_methods = clustering_methods
        self.clustering_resolutions = clustering_resolutions
        self.clustering_neighbourhood_sizes = clustering_neighbourhood_sizes
        self.clustering_principal_component_counts = (
            clustering_principal_component_counts)
        self.ground_truth_annotation_key = ground_truth_annotation_key
        self.ground_truth_representation_key = ground_truth_representation_key
        self.clustering_metric_aggregator = clustering_metric_aggregator
        self.output_directory = utilities.check_path(output_directory)
        self.base_name = base_name

        self.initial_epoch = None
        self.latest_epoch = None
        self.start_timestamp = None
        self.latest_timestamp = None
        self.end_timestamp = None

    def on_train_begin(self, logs=None):
        self.start_timestamp = datetime.now(timezone.utc)

    def on_epoch_end(self, epoch, logs=None):
        if self.initial_epoch is None:
            self.initial_epoch = epoch
        self.latest_epoch = epoch
        self.latest_timestamp = datetime.now(timezone.utc)
        self._log_training_configuration()

    def on_train_end(self, logs=None):
        self.end_timestamp = datetime.now()
        self._log_training_configuration()

    def _log_training_configuration(self):
        distribution_replica_count = (
            self.model.distribute_strategy.num_replicas_in_sync)

        optimisation_config = {
            name: optimiser.get_config()
            for name, optimiser in self.model.optimisers.items()}

        epoch_info = {
            "initial_epoch": self.initial_epoch + 1,
            "latest_epoch": self.latest_epoch + 1,
            "total_epoch_count": self.total_epoch_count}

        timestamps = {"start": self.start_timestamp}
        if self.end_timestamp is not None:
            timestamps["end"] = self.end_timestamp
        else:
            timestamps["latest"] = self.latest_timestamp

        stopping_info = {
            "early_stopping_loss": self.early_stopping_loss,
            "early_stopping_patience": self.early_stopping_patience,
            "early_stopping_initial_delay": self.early_stopping_initial_delay,
            "convergence_stopping_loss_pattern": (
                self.convergence_stopping_loss_pattern),
            "convergence_stopping_threshold": (
                self.convergence_stopping_threshold),
            "convergence_stopping_window_size": (
                self.convergence_stopping_window_size),
            "clustering_methods": self.clustering_methods,
            "clustering_resolutions": self.clustering_resolutions,
            "clustering_neighbourhood_sizes": (
                self.clustering_neighbourhood_sizes),
            "clustering_principal_component_counts": (
                self.clustering_principal_component_counts),
            "ground_truth_annotation_key": self.ground_truth_annotation_key,
            "ground_truth_representation_key": (
                self.ground_truth_representation_key),
            "clustering_metric_aggregator": self.clustering_metric_aggregator}
        if self.model.stopping_training_reasons is not None:
            stopping_info["stopping_training_reasons"] = (
                self.model.stopping_training_reasons)
        if self.model.stopped_early_with_weights_from_epoch is not None:
            stopping_info["stopped_early_with_weights_from_epoch"] = (
                self.model.stopped_early_with_weights_from_epoch + 1)

        config = {
            "batch_size": self.batch_size,
            "distribution_replica_count": distribution_replica_count,
            "epoch_info": epoch_info,
            "timestamps": timestamps,
            "stopping_info": stopping_info,
            "optimisation_config": optimisation_config}

        base_name = self.base_name
        if self.initial_epoch is not None:
            base_name = f"{base_name}-initial_epoch_{self.initial_epoch + 1}"
        path = self.output_directory.joinpath(f"{base_name}.json")
        utilities.save_as_json(config, path=path)


class TrainingStopwatch(tfk.callbacks.Callback):
    """Measures how long it takes to train model."""

    def __init__(self, verbose=0):
        super().__init__()
        self.verbose = verbose
        self.stopwatch = utilities.Stopwatch()

    def on_train_begin(self, logs=None):
        self.stopwatch.start()

    def on_train_end(self, logs=None):
        self.stopwatch.stop()
        if self.verbose:
            print(f"Total training time: {self.stopwatch.formatted_duration}.")


class TrainingCSVLogger(tfk.callbacks.CSVLogger):
    """Logs training results to a CSV file."""

    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}
        if self.keys and self.keys != sorted(logs.keys()):
            super().on_train_end()
            csv_log = pd.read_csv(self.filename, sep=self.sep, index_col=0)
            for key in logs.keys():
                if key not in csv_log:
                    csv_log[key] = np.nan
            csv_log.to_csv(self.filename, sep=self.sep)
            self.keys = csv_log.columns.to_list()
            append = self.append
            self.append = True
            self.on_train_begin(logs=logs)
            self.append = append
        super().on_epoch_end(epoch=epoch, logs=logs)


class TestCSVLogger(tfk.callbacks.Callback):
    """Logs test results to a CSV file."""

    def __init__(self, path, delimiter=","):
        super().__init__()
        self.path = utilities.check_path(path)
        self.delimiter = delimiter

    def on_test_end(self, logs=None):
        with self.path.open(mode="w") as f:
            csv_writer = csv.writer(f, delimiter=self.delimiter)
            csv_writer.writerow(logs.keys())
            csv_writer.writerow([
                f"{metric}" for metric in logs.values()])


def _encode(adversarial_autoencoder, data_set, data_set_name=None,
            identifier=None, batch_size=64, verbose=0):
    data_set_name = data_set_name or data_set.uns.get("name")
    printer = utilities.Printer(verbose=verbose)
    previous_identifer = data_set.uns.get("latent_representation_identifier")
    if identifier and identifier == previous_identifer:
        printer.print(utilities.compose_message(
            "Using already encoded latent representation",
            "of" if data_set_name else None, data_set_name, "."))
    else:
        printer.print(utilities.compose_message(
            "Encoding", data_set_name, "into latent representation:"))
        latent_samples = adversarial_autoencoder.encoder.predict(
            data_set.X, batch_size=batch_size,
            verbose=printer.keras_models_verbose)
        if models.is_categorical(adversarial_autoencoder.encoder):
            latent_representation, latent_categories = latent_samples
        else:
            latent_representation = latent_samples
            latent_categories = None
        data_utilities.add_latent_representation_to_data_set(
            latent_representation=latent_representation,
            data_set=data_set,
            latent_categories=latent_categories)
        if identifier:
            data_set.uns["latent_representation_identifier"] = identifier


def _encode_cluster_compare(adversarial_autoencoder,
                            data_set,
                            clustering_metric_names,
                            clustering_methods=None,
                            clustering_resolutions=None,
                            clustering_neighbourhood_sizes=None,
                            clustering_principal_component_counts=None,
                            original_grouping_key=None,
                            representation_key=None,
                            distance_metric="euclidean",
                            clustering_metric_aggregator="optimum",
                            encoding_identifier=None,
                            batch_size=64,
                            verbose=0):
    printer = utilities.Printer(verbose=verbose)

    def _base_metric_name(metric_name):
        return utilities.remove_prefix(
            metric_name, prefix=VALIDATION_METRIC_PREFIX)

    clustering_metric_names = utilities.check_set(
        clustering_metric_names, not_empty=True)
    supervised_clustering_metric_names = {
        metric_name for metric_name in clustering_metric_names
        if _base_metric_name(metric_name) in analyses.clustering_metric_names(
            supervised=True)}
    unsupervised_clustering_metric_names = {
        metric_name for metric_name in clustering_metric_names
        if _base_metric_name(metric_name) in analyses.clustering_metric_names(
            supervised=False)}

    if (not supervised_clustering_metric_names and
            not unsupervised_clustering_metric_names):
        raise RuntimeError("No matching clustering metrics found.")

    if clustering_methods is None:
        raise ValueError(
            "No clustering method specified for clustering latent space.")

    _encode(
        adversarial_autoencoder=adversarial_autoencoder,
        data_set=data_set,
        identifier=encoding_identifier,
        batch_size=batch_size,
        verbose=printer.verbose)

    previous_latent_annotation_keys = data_utilities.latent_keys(
        data_set.obs.keys())

    clustering_configs = analyses.clustering_configs(
        clustering_methods,
        resolutions=clustering_resolutions,
        neighbourhood_sizes=clustering_neighbourhood_sizes,
        principal_component_counts=clustering_principal_component_counts)
    printer.print("Clustering latent representation:")
    analyses.cluster_latent_representation_with_configs(
        data_set,
        *clustering_configs,
        enable_progress_bar=printer.verbose)

    latent_grouping_keys = [
        name for name in data_utilities.latent_keys(data_set.obs.keys())
        if name not in previous_latent_annotation_keys]

    comparison_text_parts = []

    if supervised_clustering_metric_names:
        original_grouping = _original_grouping(original_grouping_key, data_set)
        original_grouping_text = f"`{original_grouping.name}` annotation"
        comparison_text_parts.append(original_grouping_text)

    if unsupervised_clustering_metric_names:
        representation, distance_metric = (
            analyses.pairwise_distances_otherwise_representation(
                data_set,
                representation_key=representation_key,
                distance_metric=distance_metric))
        if representation_key:
            representation_text = f"`{representation_key}` representation"
            comparison_text_parts.append(representation_text)

    clustering_inflection = "s" if len(clustering_configs) > 1 else ""
    comparison_text = (
        " using " + " and ".join(comparison_text_parts)
    ) if comparison_text_parts else ""
    printer.print(
        f"Evaluating clustering{clustering_inflection} "
        f"of latent representation{comparison_text}:")

    clustering_metrics = {}
    for metric_name in clustering_metric_names:
        aggregate_clustering_metrics = _aggregator(
            clustering_metric_aggregator,
            metric_name=_base_metric_name(metric_name))
        metric_values = []
        latent_grouping_keys_progress_bar = utilities.ProgressBar(
            latent_grouping_keys, desc=metric_name,
            unit="clustering", unit_plural="clusterings",
            leave=False, disable=not printer.verbose)
        for latent_grouping_name in latent_grouping_keys_progress_bar:
            latent_grouping = data_set.obs[latent_grouping_name]
            if metric_name in supervised_clustering_metric_names:
                metric_value = analyses.compare_groupings(
                    original_grouping=original_grouping,
                    other_grouping=latent_grouping,
                    metric=_base_metric_name(metric_name))
            elif metric_name in unsupervised_clustering_metric_names:
                metric_value = analyses.evaluate_grouping_on_representation(
                    representation=representation,
                    grouping=latent_grouping,
                    metric=_base_metric_name(metric_name),
                    distance_metric=distance_metric)
            metric_values.append(metric_value)
        aggregated_metric = aggregate_clustering_metrics(metric_values)
        printer.print(
            f"{metric_name}: {aggregated_metric:.4f} "
            f"({latent_grouping_keys_progress_bar.formatted_statistics()})")
        clustering_metrics[metric_name] = aggregated_metric

    return clustering_metrics


def _original_grouping(key, data_set):
    if not key:
        keys = data_utilities.categorical_annotation_keys(data_set.obs)
        for guessing_pattern in (
                analyses.ORIGINAL_MAIN_GROUPING_GUESSING_PATTERNS):
            for possible_key in keys:
                if re.fullmatch(
                        guessing_pattern,
                        possible_key.lower()):
                    key = possible_key
                    break
            if key:
                break
    if not key:
        raise ValueError(
            "An appropriate grouping annotation for the original data "
            "could not be found. Please specify one manually.")
    return data_set.obs[key]


def _aggregator(identifier, metric_name=None):
    _AGGREGATORS_FOR_DIRECTION = {
        analyses.BestDirection.POSITIVE: np.max,
        analyses.BestDirection.NEGATIVE: np.min}
    if callable(identifier):
        aggregator = identifier
    elif identifier == "mean":
        aggregator = np.mean
    elif identifier == "median":
        aggregator = np.median
    elif identifier == "optimum":
        best_direction = analyses.clustering_metric_attribute(
            metric_name, "best_direction")
        aggregator = _AGGREGATORS_FOR_DIRECTION[best_direction]
    else:
        raise ValueError(f"Cannot find aggregator `{identifier}`.")
    return aggregator


def _representation(key, data_set):
    if key:
        obsm_key = utilities.ensure_prefix(key, prefix="X_")
        if key in data_set.layers:
            representation = data_set.layers[key]
        elif obsm_key in data_set.obsm:
            representation = data_set.obsm[obsm_key]
        else:
            raise ValueError(
                f"Representation `{key}` not found.")
    else:
        representation = data_set.X
    return representation


def _class_name(instance):
    return type(instance).__name__
