import pandas as pd

_SMOOTHING_FUNCTIONS = {}


def get_smoothing_function(name):
    smoother = _SMOOTHING_FUNCTIONS.get(name, None)
    if not smoother:
        possible_smoothing_functions = ", ".join(list(
            _SMOOTHING_FUNCTIONS.keys()))
        raise ValueError(
            f"Smoothing method `{name}` not found. "
            "Possible smoothing functions are: "
            f"{possible_smoothing_functions}.")
    return smoother


def _register_smoothing_function(name):
    def decorator(function):
        _SMOOTHING_FUNCTIONS[name] = function
        return function
    return decorator


@_register_smoothing_function("simple_moving_average")
def simple_moving_average(series, window_size=5):
    s = pd.Series(series)
    sma = s.rolling(window=window_size, min_periods=0).mean()
    return sma.values


@_register_smoothing_function("exponential_moving_average")
def exponential_moving_average(series, decay=0.6):
    s = pd.Series(series)
    ema = s.ewm(alpha=decay, min_periods=0).mean()
    return ema.values
