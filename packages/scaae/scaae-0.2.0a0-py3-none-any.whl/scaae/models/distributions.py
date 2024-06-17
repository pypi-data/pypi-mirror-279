from functools import lru_cache

import numpy as np

import tensorflow as tf
from tensorflow import keras as tfk
from tensorflow.keras import layers as tfkl

from tensorflow_probability import layers as tfpl, distributions as tfd
from tensorflow_probability.python.internal import distribution_util as tfdu

from scaae.utilities import check_dict

DISTRIBUTIONS = {}


class InputDistribution(tfkl.Layer):
    def __init__(self,
                 name,
                 event_shape=(),
                 mixture_component_count=None,
                 distribution_kwargs=None,
                 **kwargs):
        super().__init__(name=name)
        distribution_kwargs = check_dict(distribution_kwargs)
        distribution = IndependentInputDistribution(
            name,
            event_shape=event_shape,
            distribution_kwargs=distribution_kwargs,
            **kwargs)
        parameters_size = distribution.params_size(
            event_shape=event_shape)
        if mixture_component_count and mixture_component_count > 1:
            distribution = MixtureSameFamily(
                num_components=mixture_component_count,
                component_layer=distribution)
            parameters_size = distribution.params_size(
                mixture_component_count, parameters_size)
        self.distribution = distribution
        self.parameters = tfkl.Dense(parameters_size, name="parameters")

    def call(self, inputs):
        parameters = self.parameters(inputs)
        distribution = self.distribution(parameters)
        return distribution


class IndependentInputDistribution(tfpl.DistributionLambda):
    def __init__(self,
                 distribution_name,
                 event_shape=(),
                 convert_to_tensor_fn="sample",
                 validate_args=False,
                 distribution_kwargs=None,
                 **kwargs):
        kwargs.pop("make_distribution_fn", None)
        distribution_kwargs = check_dict(distribution_kwargs)
        distribution_name = _check_distribution_name(distribution_name)
        distribution_specs = DISTRIBUTIONS.get(distribution_name)
        self.parameter_count = distribution_specs.get("parameter_count")
        make_distribution_fn = _make_independent_distribution_function(
            make_distribution_fn=distribution_specs.get("function"),
            parameter_count=self.parameter_count)
        super().__init__(
            lambda parameters: make_distribution_fn(
                parameters,
                event_shape=event_shape,
                validate_args=validate_args,
                name=distribution_name,
                **distribution_kwargs),
            convert_to_tensor_fn=convert_to_tensor_fn,
            **kwargs)

    def params_size(self, event_shape=()):
        return self.parameter_count * tf.math.reduce_prod(event_shape)


def _make_independent_distribution_function(make_distribution_fn,
                                            parameter_count):
    def new(parameters, event_shape=(), validate_args=False, name=None,
            **kwargs):
        with tf.name_scope(name or "Independent"):
            parameters = tf.convert_to_tensor(parameters, name="parameters")
            event_shape = tfdu.expand_to_vector(
                tf.convert_to_tensor(
                    event_shape, name="event_shape", dtype_hint=tf.int32),
                tensor_name="event_shape")
            output_shape = tf.concat([
                tf.shape(parameters)[:-1],
                event_shape,
            ], axis=0)
            parameters = tf.split(parameters, parameter_count, axis=-1)
            parameters = [
                tf.reshape(parameter, output_shape)
                for parameter in parameters]
            return tfd.Independent(
                make_distribution_fn(
                    parameters=parameters,
                    validate_args=validate_args,
                    **kwargs),
                reinterpreted_batch_ndims=tf.size(event_shape),
                validate_args=validate_args)
    return new


def register_distribution(name, parameter_count):
    def decorator(function):
        DISTRIBUTIONS[name] = {
            "function": function,
            "parameter_count": parameter_count
        }
        return function
    return decorator


@register_distribution("bernoulli", parameter_count=1)
def _make_bernoulli(parameters, validate_args=False):
    logits, = parameters
    logits = _clip_for_exponentiating(logits)
    return tfd.Bernoulli(
        logits=logits,
        validate_args=validate_args)


@register_distribution("one_hot_categorical", parameter_count=1)
def _make_one_hot_categorical(parameters,
                              temperature=0.5,
                              validate_args=False):
    logits, = parameters
    logits = _clip_for_exponentiating(logits)
    return tfd.RelaxedOneHotCategorical(
        temperature=temperature,
        logits=logits,
        validate_args=validate_args)


@register_distribution("normal", parameter_count=2)
def _make_normal(parameters, validate_args=False):
    location, scale = parameters
    scale = tf.math.softplus(_clip_for_exponentiating(scale))
    return tfd.Normal(
        loc=location,
        scale=scale,
        validate_args=validate_args)


@register_distribution("poisson", parameter_count=1)
def _make_poisson(parameters, validate_args=False):
    log_rate, = parameters
    log_rate = _clip_for_exponentiating(log_rate)
    return tfd.Poisson(
        log_rate=log_rate,
        validate_args=validate_args)


@register_distribution("zero_inflated_poisson", parameter_count=2)
def _make_zero_inflated_poisson(parameters, validate_args=False):
    log_rate, excess_zeros_logits = parameters
    log_rate = _clip_for_exponentiating(log_rate)
    excess_zeros_logits = _clip_for_exponentiating(excess_zeros_logits)
    excess_zeros_logits = tf.stack([
        excess_zeros_logits, tf.zeros(tf.shape(excess_zeros_logits))],
        axis=-1)
    return tfd.Mixture(
        cat=tfd.Categorical(
            logits=excess_zeros_logits,
            validate_args=validate_args),
        components=[
            tfd.Deterministic(loc=tf.zeros(tf.shape(log_rate))),
            tfd.Poisson(
                log_rate=log_rate,
                validate_args=validate_args)],
        validate_args=validate_args)


@register_distribution("negative_binomial", parameter_count=2)
def _make_negative_binomial(parameters, validate_args=False):
    total_count, logits = parameters
    total_count = tf.math.ceil(tf.math.softplus(_clip_for_exponentiating(
        total_count)))
    logits = _clip_for_exponentiating(logits)
    return tfd.NegativeBinomial(
        total_count=total_count,
        logits=logits,
        validate_args=validate_args)


@register_distribution("zero_inflated_negative_binomial", parameter_count=3)
def _make_zero_inflated_negative_binomial(parameters, validate_args=False):
    total_count, success_logits, excess_zeros_logits = parameters
    total_count = tf.math.ceil(tf.math.softplus(_clip_for_exponentiating(
        total_count)))
    success_logits = _clip_for_exponentiating(success_logits)
    excess_zeros_logits = _clip_for_exponentiating(excess_zeros_logits)
    excess_zeros_logits = tf.stack([
        excess_zeros_logits, tf.zeros(tf.shape(excess_zeros_logits))],
        axis=-1)
    return tfd.Mixture(
        cat=tfd.Categorical(
            logits=excess_zeros_logits,
            validate_args=validate_args),
        components=[
            tfd.Deterministic(loc=tf.zeros(tf.shape(total_count))),
            tfd.NegativeBinomial(
                total_count=total_count,
                logits=success_logits,
                validate_args=validate_args)],
        validate_args=validate_args)


class MixtureSameFamily(tfpl.MixtureSameFamily):
    def __init__(self,
                 num_components,
                 component_layer,
                 convert_to_tensor_fn=tfd.Distribution.sample,
                 validate_args=False,
                 **kwargs):
        super().__init__(
            num_components=num_components,
            component_layer=component_layer,
            convert_to_tensor_fn=convert_to_tensor_fn,
            validate_args=validate_args,
            **kwargs)

    @staticmethod
    def new(params, num_components, component_layer,
            validate_args=False, name=None):
        with tf.name_scope(name or "MixtureSameFamily"):
            params = tf.convert_to_tensor(params, name="params")
            num_components = tf.convert_to_tensor(
                num_components, name="num_components", dtype_hint=tf.int32)

            components_dist = component_layer(
                tf.reshape(
                    params[..., num_components:],
                    tf.concat([tf.shape(params)[:-1], [num_components, -1]],
                              axis=0)))
            mixture_dist = tfd.Categorical(
                logits=_clip_for_exponentiating(params[..., :num_components]))
            return tfd.MixtureSameFamily(
                mixture_dist,
                components_dist,
                validate_args=validate_args)


class UnitNormalDistribution(tfkl.Layer):
    def __init__(self, event_shape=(), name="normal"):
        super().__init__(name=name)
        location = tf.zeros(shape=tf.expand_dims(event_shape, axis=0))
        self.distribution = tfpl.DistributionLambda(
            lambda _: tfd.Independent(
                tfd.Normal(loc=location, scale=1.),
                reinterpreted_batch_ndims=1))

    def call(self, inputs):
        distribution = self.distribution(inputs)
        return distribution

    def get_config(self):
        return {}


class NormalMixtureDistribution(tfkl.Layer):
    def __init__(self,
                 event_size=1,
                 component_count=2,
                 learn_parameters=True,
                 logits_initializer="zeros",
                 locations_initializer="zeros",
                 scales_initializer="inverse-softplus-unit",
                 name="normal_mixture"):
        super().__init__(name=name)
        self.learn_parameters = learn_parameters
        self.logits_initializer = logits_initializer
        self.locations_initializer = locations_initializer
        self.scales_initializer = scales_initializer

        with tf.name_scope(name):
            normal_specs = DISTRIBUTIONS.get("normal")
            normal_parameter_count = (
                normal_specs.get("parameter_count"))
            normal_parameter_size = (
                normal_parameter_count * event_size)
            make_normal_function = normal_specs.get("function")
            make_distribution_function = (
                _make_independent_distribution_function(
                    make_normal_function, normal_parameter_count))
            normal = tfpl.DistributionLambda(
                lambda t: make_distribution_function(t, event_size))
            with tf.name_scope("parameters"):
                initializer = self._parameter_initializer(
                    component_count=component_count,
                    event_size=event_size,
                    logits_initializer=self.logits_initializer,
                    locations_initializer=self.locations_initializer,
                    scales_initializer=self.scales_initializer)
                self.parameters = tfpl.VariableLayer(
                    shape=[
                        MixtureSameFamily.params_size(
                            component_count,
                            normal_parameter_size)],
                    initializer=initializer,
                    trainable=self.learn_parameters)
            self.distribution = MixtureSameFamily(
                num_components=component_count,
                component_layer=normal)

    def call(self, inputs):
        parameters = self.parameters(inputs)
        distribution = self.distribution(parameters)
        return distribution

    def coefficients(self):
        distribution = self(0.)
        return distribution.mixture_distribution.probs_parameter()

    def means(self):
        distribution = self(0.)
        return distribution.components_distribution.mean()

    def variances(self):
        distribution = self(0.)
        return distribution.components_distribution.variance()

    def covariances(self):
        return tf.linalg.diag(self.variances())

    def get_config(self):
        return {
            "learn_parameters": self.learn_parameters,
            "logits_initializer": self.logits_initializer,
            "locations_initializer": self.locations_initializer,
            "scales_initializer": self.scales_initializer}

    @staticmethod
    def _parameter_initializer(component_count, event_size,
                               logits_initializer="zeros",
                               locations_initializer="zeros",
                               scales_initializer="inverse-softplus-unit"):

        if scales_initializer == "inverse-softplus-unit":
            scales_initializer = tfk.initializers.Constant(
                np.log(np.expm1(1.)))

        component_initializer = [locations_initializer, scales_initializer]
        component_sizes = [event_size, event_size]

        initializers = (
            [logits_initializer] + component_count * component_initializer)
        sizes = [component_count] + component_count * component_sizes

        initializer = tfpl.BlockwiseInitializer(
            initializers=initializers, sizes=sizes)

        return initializer


class CategoricalDistribution(tfkl.Layer):
    DEFAULT_TEMPERATURE = 0.5

    def __init__(self,
                 category_count=2,
                 learn_probabilities=False,
                 temperature=None,
                 learn_temperature=False,
                 name="categorical"):
        super().__init__(name=name)
        with tf.name_scope(name):
            self.category_count = category_count
            self.logits = tf.zeros(self.category_count)

            if learn_probabilities:
                self.logits = tf.Variable(
                    self.logits, trainable=True, name="logits")

                if temperature is None:
                    temperature = self.DEFAULT_TEMPERATURE
                if learn_temperature:
                    temperature = tf.Variable(
                        temperature, trainable=True, name="temperature")
                self.temperature = temperature

                distribution = tfd.RelaxedOneHotCategorical(
                    temperature=temperature, logits=self.logits)

            else:
                distribution = tfd.OneHotCategorical(logits=self.logits)

            self.distribution = distribution


def _check_distribution_name(name):
    if name not in DISTRIBUTIONS:
        raise ValueError(f"Distribution `{name}` not found.")
    return name


def _clip_for_exponentiating(x):
    minimum_value, maximum_value = _compute_numerical_limits_for_exponentation(
        x.dtype.as_numpy_dtype())
    return tf.clip_by_value(x, minimum_value, maximum_value)


@lru_cache
def _compute_numerical_limits_for_exponentation(dtype):
    limits = np.finfo(dtype)
    minimum_value = np.log(limits.tiny) / 2
    maximum_value = np.log(limits.max) / 2
    return minimum_value, maximum_value
