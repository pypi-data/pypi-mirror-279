import datetime
import json
import re
import sys
import time
from datetime import timedelta
from functools import singledispatch
from pathlib import Path

import numpy as np
import pandas as pd
from natsort import natsorted
from tqdm import tqdm

DEFAULT_MEMORY_LIMIT_IN_GIGABYTES = 10


class Printer:
    def __init__(self, verbose):
        self._verbose = verbose

    @property
    def verbose(self):
        return self._verbose

    @property
    def keras_verbose(self):
        return min(max(0, self._verbose), 1)

    @property
    def keras_models_verbose(self):
        verbose = self.keras_verbose
        if verbose and not sys.stdout.isatty():
            verbose = 2
        return verbose

    def print(self, *args, **kwargs):
        if self.verbose:
            print(*args, **kwargs)

    def verbose_print(self, *args, **kwargs):
        if self.verbose > 1:
            print(*args, **kwargs)


class Stopwatch:
    def __init__(self):
        self.start_time = self.end_time = None

    def start(self):
        self.start_time = time.perf_counter()

    def stop(self):
        self.end_time = time.perf_counter()

    @property
    def duration(self):
        if self.start_time is None or self.end_time is None:
            duration = None
        else:
            duration = self.end_time - self.start_time
        return duration

    @property
    def formatted_duration(self):
        return format_duration(self.duration)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *exc_info):
        self.stop()


class ProgressBar(tqdm):
    def __init__(self, iterable, *, leave="statistics", unit_plural=None,
                 **kwargs):
        self.leave_statistics = leave == "statistics"
        self.unit_plural = unit_plural
        leave = False if leave == "statistics" else leave
        super().__init__(iterable, leave=leave, **kwargs)
        self.verbose = not self.disable

    def close(self):
        super().close()
        if self.verbose and self.leave_statistics:
            message = self.formatted_statistics(separator=" - ")
            if self.desc:
                message = f"{self.desc}: {message}"
            print(message)
            self.leave_statistics = False

    @property
    def format_dict(self):
        format_dict = super().format_dict
        format_dict.setdefault("unit_plural", self.unit_plural)
        return format_dict

    def formatted_statistics(self, separator=", "):
        formatted_statistics_parts = []

        start_index = self.format_dict.get("initial")
        current_index = self.format_dict.get("n")
        count = self.format_dict.get("total")
        unit = (
            self.format_dict.get("unit") if count == 1
            else self.format_dict.get("unit_plural")
            or self.format_dict.get("unit"))
        formatted_status = f"{current_index}"
        if start_index and start_index != current_index:
            formatted_status = f"{start_index}-{formatted_status}"
        if count:
            formatted_status = f"{formatted_status}/{count}"
        formatted_status = f"{formatted_status} {unit}"
        formatted_statistics_parts.append(formatted_status)

        elapsed_time = self.format_dict.get("elapsed")
        formatted_duration = format_duration(elapsed_time)
        formatted_statistics_parts.append(formatted_duration)

        rate = self.format_dict.get("rate")
        unit = self.format_dict.get("unit")
        if rate:
            frequency = 1 / rate
            formatted_frequency = format_duration(frequency)
            formatted_frequency = f"{formatted_frequency}/{unit}"
            formatted_statistics_parts.append(formatted_frequency)

        return separator.join(formatted_statistics_parts)


def format_duration(duration):
    if not isinstance(duration, timedelta):
        duration = timedelta(seconds=duration)
    total_seconds = duration.total_seconds()
    total_seconds = np.round(
        total_seconds,
        decimals=(
            3 if total_seconds < 1
            else 2 if total_seconds < 10
            else 1 if total_seconds < 60
            else 0))
    duration = timedelta(seconds=total_seconds)
    string_parts = []
    if duration.days > 0:
        string_parts.append(f"{duration.days}d")
    if duration.seconds > 0:
        hours, remainder = divmod(duration.seconds, 60 * 60)
        minutes, seconds = divmod(remainder, 60)
        seconds += duration.microseconds * 1e-6
        if hours > 0 or string_parts:
            string_parts.append(f"{hours}h")
        if minutes > 0 or string_parts:
            string_parts.append(f"{minutes}m")
        if seconds > 0 or string_parts:
            if string_parts:
                second_format = ".0f"
            else:
                second_format = ".3g"
            string_parts.append(f"{seconds:{second_format}}s")
    if not string_parts:
        milliseconds = duration.microseconds * 1e-3
        if milliseconds >= 1:
            string_parts.append(f"{milliseconds:.3g}ms")
    if not string_parts:
        string_parts.append("0ms")
    string_parts = string_parts[:2]
    string = " ".join(string_parts)
    return string


def save_as_json(obj, path, replace=True):
    path = check_path(path)
    if path.exists() and not replace:
        raise FileExistsError(f"{path} already exists.")
    path.write_text(json.dumps(obj, indent="\t", default=to_serializable))


@singledispatch
def to_serializable(value):
    return str(value)


@to_serializable.register(np.float32)
def float32_to_serializable(value):
    return np.float64(str(value))


@to_serializable.register(datetime.datetime)
def datetime_to_serializable(value):
    return value.astimezone().isoformat()


def load_csv(path):
    path = check_path(path)
    data_frame = pd.read_csv(path)
    if "epoch" in data_frame.columns:
        data_frame = data_frame.drop_duplicates(
            subset="epoch", keep="last")
        data_frame = data_frame.set_index("epoch")
    return data_frame


def join_strings(strings, conjunction="and"):
    if not isinstance(strings, (list, tuple)):
        try:
            strings = list(strings)
        except TypeError:
            raise ValueError(
                "`strings` should be a list, tuple, or iterable of strings.")
    conjunction = conjunction.strip()
    string_count = len(strings)
    if string_count == 1:
        enumerated_string = strings[0]
    elif string_count == 2:
        enumerated_string = " {} ".format(conjunction).join(strings)
    elif string_count >= 3:
        enumerated_string = "{}, {} {}".format(
            ", ".join(strings[:-1]),
            conjunction,
            strings[-1])
    else:
        raise ValueError("`strings` does not contain any strings.")
    return enumerated_string


def compose_message(*parts):
    message = " ".join(p for p in parts if p)
    punctuation_pattern = r" ([.,:;!?])"
    message = re.sub(punctuation_pattern, r"\1", message)
    return message


def remove_prefix(text, prefix):
    if prefix and text.startswith(prefix):
        return text[len(prefix):]
    else:
        return text


def remove_suffix(text, suffix):
    if suffix and text.endswith(suffix):
        return text[:-len(suffix)]
    else:
        return text


def ensure_prefix(text, prefix):
    if prefix and not text.startswith(prefix):
        text = f"{prefix}{text}"
    return text


def ensure_suffix(text, suffix):
    if suffix and not text.endswith(suffix):
        text = f"{text}{suffix}"
    return text


def filter_texts(texts, match_patterns=None, ignore_patterns=None):
    if (match_patterns is None and ignore_patterns is None
            or match_patterns and ignore_patterns):
        raise RuntimeError("Either provide match patterns or ignore patterns.")

    elif match_patterns:
        match_patterns = check_list(match_patterns, not_empty=True)
        filtered_texts = set()

        for pattern in match_patterns:
            filtered_texts.update(
                text for text in texts if re.fullmatch(pattern, text))

    elif ignore_patterns:
        ignore_patterns = check_list(ignore_patterns, not_empty=True)
        filtered_texts = set(texts)

        for pattern in ignore_patterns:
            filtered_texts = filtered_texts.difference(
                text for text in texts if re.fullmatch(pattern, text))

    return sorted(filtered_texts)


class AllValuesUniqueError(ValueError):
    pass


def as_categorical_series(values, index=None, check_uniqueness=False):
    if index is None and isinstance(values, pd.Series):
        index = values.index
    categorical = pd.Categorical(values)
    if check_uniqueness and len(categorical.categories) >= len(values):
        raise AllValuesUniqueError
    categorical = categorical.reorder_categories(natsorted(
        categorical.categories))
    return pd.Series(categorical, index=index)


def allow_memory_usage(requested_memory_usage_in_bytes,
                       memory_limit_in_gigabytes=None):
    memory_limit_in_gigabytes = (
        memory_limit_in_gigabytes or DEFAULT_MEMORY_LIMIT_IN_GIGABYTES)
    memory_limit_in_bytes = memory_limit_in_gigabytes * 1e9
    return requested_memory_usage_in_bytes <= memory_limit_in_bytes


def check_path(path):
    return Path(path).expanduser().resolve()


def check_float(value):
    return float(value)


def check_list(value, default=None, wrap_none=False,
               use_dictionary_values=False, not_empty=False):
    if value is None:
        if wrap_none:
            value = [None]
        elif default:
            value = default
        else:
            value = []
    elif isinstance(value, dict) and use_dictionary_values:
        value = list(value.values())
    elif isinstance(value, set):
        value = list(value)
    elif not isinstance(value, (list, tuple)):
        value = [value]
    else:
        value = list(value)
    if not_empty:
        _check_not_empty(value, type_name="list")
    return value


def check_dict(value):
    if value is None:
        value = {}
    elif not isinstance(value, dict):
        raise TypeError("Expected dictionary, got {type(value)}.")
    return value


def check_set(value, not_empty=False):
    if not isinstance(value, set):
        try:
            value = set(value)
        except TypeError:
            value = {value}
    if not_empty:
        _check_not_empty(value, type_name="set")
    return value


def _check_not_empty(value, type_name):
    if len(value) == 0:
        raise ValueError(
            f"Expected non-empty {type_name}; "
            f"empty {type_name} or no input provided.")
