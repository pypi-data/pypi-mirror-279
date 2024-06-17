import tensorflow as tf
from tensorflow.keras import layers as tfkl
from tensorflow import keras as tfk
from tensorflow.python.keras import backend as K

from scaae.models.base import DenseBlock, Model, MeanMetric
from scaae.models import distributions, noise_models
from scaae.models.utilities import configure_optimiser
from scaae.utilities import check_float, check_list, check_dict

DEFAULT_LOSSES = {
    "autoencoder": "mean_squared_error",
    "discriminator": "binary_crossentropy",
    "generator": "binary_crossentropy",
    "categorical_discriminator": "binary_crossentropy",
    "categorical_generator": "binary_crossentropy"}
DEFAULT_ACTIVATIONS = {
    "binary_crossentropy": "sigmoid"}
ACTIVATION_ALIASES = {
    "leaky_relu": "LeakyReLU"}
DEFAULT_ACTIVATION_CONFIGS = {
    "LeakyReLU": {"alpha": 0.2}}
MODELS = {}


class NegativeLogLikelihood(tf.losses.Loss):
    def call(self, inputs, distribution):
        return - distribution.log_prob(inputs)


class Encoder(Model):
    def __init__(self,
                 latent_size=32,
                 category_count=1,
                 intermediate_sizes=[64, 64],
                 intermediate_activation="relu",
                 intermediate_normalisation=None,
                 intermediate_dropout_rate=None,
                 name="encoder"):
        super().__init__(name=name)
        self.intermediate = DenseBlock(
            intermediate_sizes,
            activation=intermediate_activation,
            normalisation=intermediate_normalisation,
            dropout_rate=intermediate_dropout_rate,
            name="intermediate")
        self.latent_representation = distributions.InputDistribution(
            "normal",
            event_shape=latent_size,
            mixture_component_count=category_count,
            convert_to_tensor_fn="sample")

    def predict_step(self, inputs):
        if isinstance(inputs, tuple):
            inputs = inputs[0]
        distribution = self(inputs, training=False)
        outputs = distribution.mean()
        return outputs

    def call(self, inputs, training=None):
        intermediates = self.intermediate(inputs, training=training)
        latent_representations = self.latent_representation(intermediates)
        return latent_representations


class CategoricalEncoder(Encoder):
    def __init__(self,
                 latent_size=32,
                 intermediate_sizes=[64, 64],
                 intermediate_activation="relu",
                 intermediate_normalisation=None,
                 intermediate_dropout_rate=None,
                 category_count=2,
                 categorical_temperature=None,
                 learn_categorical_temperature=False,
                 name="categorical_encoder"):
        super().__init__(
            latent_size=latent_size,
            intermediate_sizes=intermediate_sizes,
            intermediate_activation=intermediate_activation,
            intermediate_normalisation=intermediate_normalisation,
            intermediate_dropout_rate=intermediate_dropout_rate,
            name=name)

        if not isinstance(category_count, int):
            raise TypeError("`category_count` should be an integer.")
        elif category_count < 2:
            raise TypeError(
                "The number of categories should be more than 1.")

        latent_category_distribution_name = "one_hot_categorical"

        if learn_categorical_temperature:
            if categorical_temperature is None:
                raise RuntimeError(
                    "To learn the temperature for the categorical encoder, "
                    "an initial value must be specified.")
            with tf.name_scope(self.name):
                with tf.name_scope(latent_category_distribution_name):
                    categorical_temperature = tf.Variable(
                        categorical_temperature, trainable=True,
                        name="temperature")
        self.categorical_temperature = categorical_temperature

        distribution_kwargs = {}
        if self.categorical_temperature:
            distribution_kwargs["temperature"] = self.categorical_temperature

        self.latent_category = distributions.InputDistribution(
            latent_category_distribution_name,
            event_shape=category_count,
            distribution_kwargs=distribution_kwargs,
            convert_to_tensor_fn="sample")

    def predict_step(self, inputs):
        if isinstance(inputs, tuple):
            inputs = inputs[0]
        latent_representations, latent_categories = self(
            inputs, training=False)
        latent_representations = latent_representations.mean()
        latent_categories = tf.math.argmax(
            latent_categories.distribution.probs_parameter(), axis=-1)
        return latent_representations, latent_categories

    def call(self, inputs, training=None):
        intermediates = self.intermediate(inputs, training=training)
        latent_representations = self.latent_representation(intermediates)
        latent_categories = self.latent_category(intermediates)
        return latent_representations, latent_categories


class Decoder(Model):
    def __init__(self,
                 feature_size,
                 intermediate_sizes=[64, 64],
                 intermediate_activation="relu",
                 intermediate_normalisation=None,
                 intermediate_dropout_rate=None,
                 reconstruction_distribution=None,
                 reconstruction_activation=None,
                 name="decoder"):
        super().__init__(name=name)
        self.intermediate = DenseBlock(
            intermediate_sizes,
            activation=intermediate_activation,
            normalisation=intermediate_normalisation,
            dropout_rate=intermediate_dropout_rate,
            name="intermediate")
        if reconstruction_distribution:
            self.reconstruction = distributions.InputDistribution(
                reconstruction_distribution,
                event_shape=feature_size,
                convert_to_tensor_fn="mean")
        else:
            self.reconstruction = tfkl.Dense(
                feature_size,
                activation=reconstruction_activation,
                name="reconstruction")

    def call(self, inputs, training=None):
        intermediates = self.intermediate(inputs, training=training)
        reconstructions = self.reconstruction(intermediates)
        return reconstructions


class Discriminator(Model):
    def __init__(self,
                 intermediate_sizes=[64, 64],
                 intermediate_activation="relu",
                 intermediate_normalisation=None,
                 intermediate_dropout_rate=None,
                 verdict_distribution=None,
                 verdict_activation=None,
                 name="discriminator"):
        super().__init__(name=name)
        self.intermediate = DenseBlock(
            intermediate_sizes,
            activation=intermediate_activation,
            normalisation=intermediate_normalisation,
            dropout_rate=intermediate_dropout_rate,
            name="intermediate")
        if verdict_distribution:
            self.verdict = distributions.InputDistribution(
                verdict_distribution,
                event_shape=1,
                convert_to_tensor_fn="mean")
        else:
            self.verdict = tfkl.Dense(
                1, activation=verdict_activation, name="verdict")

    def call(self, inputs, training=None):
        intermediates = self.intermediate(inputs, training=training)
        verdicts = self.verdict(intermediates)
        return verdicts


class CategoricalDiscriminator(Discriminator):
    def __init__(self,
                 intermediate_sizes=[64, 64],
                 intermediate_activation="relu",
                 intermediate_normalisation=None,
                 intermediate_dropout_rate=None,
                 verdict_distribution=None,
                 verdict_activation=None,
                 name="categorical_discriminator"):
        super().__init__(
            intermediate_sizes=intermediate_sizes,
            intermediate_activation=intermediate_activation,
            intermediate_normalisation=intermediate_normalisation,
            intermediate_dropout_rate=intermediate_dropout_rate,
            verdict_distribution=verdict_distribution,
            verdict_activation=verdict_activation,
            name=name)


def _register_adversarial_autoencoder():
    def decorator(cls):
        MODELS[cls.KIND] = cls
        return cls
    return decorator


@_register_adversarial_autoencoder()
class AdversarialAutoEncoder(Model):
    KIND = "base"

    def __init__(self,
                 feature_size,
                 intermediate_sizes=(256, 128),
                 latent_size=32,
                 category_count=None,
                 autoencoder_distribution=None,
                 autoencoder_loss=None,
                 autoencoder_metrics=None,
                 autoencoder_activation=None,
                 discriminator_intermediate_sizes=None,
                 discriminator_distribution=None,
                 discriminator_loss=None,
                 discriminator_weight=1.,
                 discriminator_metrics="accuracy",
                 discriminator_activation=None,
                 discriminator_label_flipping_rate=None,
                 discriminator_label_smoothing_scale=0.1,
                 gaussian_discriminator_sample_noise_scale=None,
                 gaussian_discriminator_sample_noise_decay=None,
                 gaussian_discriminator_label_noise_scale=None,
                 generator_distribution=None,
                 generator_loss=None,
                 generator_weight=1.,
                 generator_metrics=None,
                 intermediate_activation="leaky_relu",
                 intermediate_normalisation="batch",
                 intermediate_dropout_rate=0.1,
                 true_distribution_config=None,
                 name="adversarial_autoencoder"):
        super().__init__(name=name)

        intermediate_sizes = check_list(intermediate_sizes)

        autoencoder_distribution, autoencoder_loss, autoencoder_activation = (
            _check_distribution_loss_and_activation_functions(
                autoencoder_distribution,
                autoencoder_loss,
                autoencoder_activation,
                model_name="autoencoder"))
        autoencoder_activation = _check_activation(autoencoder_activation)

        if discriminator_intermediate_sizes is None:
            discriminator_intermediate_sizes = intermediate_sizes[::-1]
        else:
            discriminator_intermediate_sizes = check_list(
                discriminator_intermediate_sizes)

        (discriminator_distribution,
         discriminator_loss,
         discriminator_activation) = (
            _check_distribution_loss_and_activation_functions(
                discriminator_distribution,
                discriminator_loss,
                discriminator_activation,
                model_name="discriminator"))
        discriminator_activation = _check_activation(discriminator_activation)

        if generator_distribution is None:
            generator_distribution = discriminator_distribution
        if generator_loss is None:
            generator_loss = discriminator_loss
        if generator_metrics is None:
            generator_metrics = discriminator_metrics
        generator_distribution, generator_loss, __ = (
            _check_distribution_loss_and_activation_functions(
                generator_distribution,
                generator_loss,
                model_name="generator"))

        intermediate_activation = _check_activation(intermediate_activation)
        true_distribution_config = check_dict(true_distribution_config)

        self.feature_size = feature_size
        self.intermediate_sizes = intermediate_sizes
        self.latent_size = latent_size
        self.autoencoder_distribution_name = autoencoder_distribution
        self.autoencoder_loss_name = autoencoder_loss
        self.autoencoder_metric_names = check_list(autoencoder_metrics)
        self.autoencoder_activation_name = autoencoder_activation
        self.discriminator_intermediate_sizes = (
            discriminator_intermediate_sizes)
        self.discriminator_distribution_name = discriminator_distribution
        self.discriminator_loss_name = discriminator_loss
        self.discriminator_weight = check_float(discriminator_weight)
        self.discriminator_metric_names = check_list(discriminator_metrics)
        self.discriminator_activation = discriminator_activation
        self.discriminator_label_flipping_rate = (
            discriminator_label_flipping_rate)
        self.discriminator_label_smoothing_scale = (
            discriminator_label_smoothing_scale)
        self.gaussian_discriminator_sample_noise_scale = (
            gaussian_discriminator_sample_noise_scale)
        self.gaussian_discriminator_sample_noise_decay = (
            gaussian_discriminator_sample_noise_decay)
        self.gaussian_discriminator_label_noise_scale = (
            gaussian_discriminator_label_noise_scale)
        self.generator_distribution_name = generator_distribution
        self.generator_loss_name = generator_loss
        self.generator_weight = check_float(generator_weight)
        self.generator_metric_names = check_list(generator_metrics)
        self.intermediate_activation = intermediate_activation
        self.intermediate_normalisation = intermediate_normalisation
        self.intermediate_dropout_rate = intermediate_dropout_rate
        self.category_count = category_count
        self.true_distribution_config = true_distribution_config

        self.encoder = Encoder(
            latent_size=self.latent_size,
            category_count=self.category_count,
            intermediate_sizes=self.intermediate_sizes,
            intermediate_activation=self.intermediate_activation,
            intermediate_normalisation=self.intermediate_normalisation,
            intermediate_dropout_rate=self.intermediate_dropout_rate)
        self.decoder = Decoder(
            feature_size=self.feature_size,
            intermediate_sizes=self.intermediate_sizes[::-1],
            intermediate_activation=self.intermediate_activation,
            intermediate_normalisation=self.intermediate_normalisation,
            intermediate_dropout_rate=self.intermediate_dropout_rate,
            reconstruction_distribution=self.autoencoder_distribution_name,
            reconstruction_activation=self.autoencoder_activation_name)
        self.discriminator = Discriminator(
            intermediate_sizes=self.discriminator_intermediate_sizes,
            intermediate_activation=self.intermediate_activation,
            intermediate_normalisation=self.intermediate_normalisation,
            intermediate_dropout_rate=self.intermediate_dropout_rate,
            verdict_distribution=self.discriminator_distribution_name,
            verdict_activation=self.discriminator_activation)

        if self.category_count:
            self.true_distribution = distributions.NormalMixtureDistribution(
                event_size=self.latent_size,
                component_count=self.category_count,
                **self.true_distribution_config,
                name="true_normal_mixture")
        else:
            self.true_distribution = distributions.UnitNormalDistribution(
                event_shape=self.latent_size, name="true_normal")

        self.autoencoder_optimiser = None
        if self.autoencoder_loss_name is not None:
            self.autoencoder_loss = tfk.losses.get(self.autoencoder_loss_name)
        elif self.autoencoder_distribution_name is not None:
            self.autoencoder_loss = NegativeLogLikelihood()
        self.autoencoder_loss.reduction = tfk.losses.Reduction.NONE
        self.autoencoder_loss_metric = tfk.metrics.Mean(
            name="autoencoder_loss")
        self.autoencoder_metrics = [
            MeanMetric(metric, name_prefix="autoencoder")
            for metric in self.autoencoder_metric_names]

        self.discriminator_optimiser = None
        if self.discriminator_loss_name is not None:
            self.discriminator_loss = tfk.losses.get(
                self.discriminator_loss_name)
        elif self.discriminator_distribution_name is not None:
            self.discriminator_loss = NegativeLogLikelihood()
        self.discriminator_loss.reduction = tfk.losses.Reduction.NONE
        self.discriminator_loss_metric = tfk.metrics.Mean(
            name="discriminator_loss")
        self.discriminator_metrics = [
            MeanMetric(metric, name_prefix="discriminator")
            for metric in self.discriminator_metric_names]

        self.discriminator_noise = _noise_function(
            label_flipping_rate=self.discriminator_label_flipping_rate,
            label_smoothing_scale=self.discriminator_label_smoothing_scale,
            gaussian_sample_noise_scale=(
                self.gaussian_discriminator_sample_noise_scale),
            gaussian_label_noise_scale=(
                self.gaussian_discriminator_label_noise_scale))
        self.gaussian_discriminator_sample_noise_weight = 1.

        self.generator_optimiser = None
        if self.generator_loss_name is not None:
            self.generator_loss = tfk.losses.get(self.generator_loss_name)
        elif self.generator_distribution_name is not None:
            self.generator_loss = NegativeLogLikelihood()
        self.generator_loss.reduction = tfk.losses.Reduction.NONE
        self.generator_loss_metric = tfk.metrics.Mean(name="generator_loss")
        self.generator_metrics = [
            MeanMetric(metric, name_prefix="generator")
            for metric in self.generator_metric_names]

        self.trained_epoch_count = 0
        self.stopping_training_reasons = None
        self.stopped_early_with_weights_from_epoch = None

    def get_config(self):
        config = super().get_config()
        config.update({
            "feature_size": self.feature_size,
            "intermediate_sizes": self.intermediate_sizes,
            "latent_size": self.latent_size,
            "autoencoder_distribution": self.autoencoder_distribution_name,
            "autoencoder_loss": self.autoencoder_loss_name,
            "autoencoder_metrics": self.autoencoder_metric_names,
            "autoencoder_activation": self.autoencoder_activation_name,
            "discriminator_intermediate_sizes": (
                self.discriminator_intermediate_sizes),
            "discriminator_distribution": self.discriminator_distribution_name,
            "discriminator_loss": self.discriminator_loss_name,
            "discriminator_weight": self.discriminator_weight,
            "discriminator_metrics": self.discriminator_metric_names,
            "discriminator_activation": self.discriminator_activation,
            "discriminator_label_flipping_rate": (
                self.discriminator_label_flipping_rate),
            "discriminator_label_smoothing_scale": (
                self.discriminator_label_smoothing_scale),
            "gaussian_discriminator_sample_noise_scale": (
                self.gaussian_discriminator_sample_noise_scale),
            "gaussian_discriminator_sample_noise_decay": (
                self.gaussian_discriminator_sample_noise_decay),
            "gaussian_discriminator_label_noise_scale": (
                self.gaussian_discriminator_label_noise_scale),
            "generator_distribution": self.generator_distribution_name,
            "generator_loss": self.generator_loss_name,
            "generator_weight": self.generator_weight,
            "generator_metrics": self.generator_metric_names,
            "intermediate_activation": self.intermediate_activation,
            "intermediate_normalisation": self.intermediate_normalisation,
            "intermediate_dropout_rate": self.intermediate_dropout_rate,
            "category_count": self.category_count,
            "true_distribution_config": self.true_distribution.get_config(),
            "name": self.name})
        return config

    def compile(self,
                autoencoder_optimiser=None,
                discriminator_optimiser=None,
                generator_optimiser=None,
                default_optimiser_name="adam",
                autoencoder_learning_rate=1e-4,
                discriminator_learning_rate=1e-5,
                generator_learning_rate=1e-5,
                default_decay=1e-6,
                default_gradient_clipping_norm=None,
                default_gradient_clipping_value=None,
                default_distribution_gradient_clipping_norm=3,
                **kwargs):

        super().compile(**kwargs)

        if autoencoder_optimiser is None:
            autoencoder_optimiser = default_optimiser_name
        if discriminator_optimiser is None:
            discriminator_optimiser = default_optimiser_name
        if generator_optimiser is None:
            generator_optimiser = default_optimiser_name

        autoencoder_optimiser = configure_optimiser(
            optimiser=autoencoder_optimiser,
            learning_rate=autoencoder_learning_rate,
            decay=default_decay,
            clipnorm=default_gradient_clipping_norm,
            clipvalue=default_gradient_clipping_value,
            distribution_modelling=(
                self.autoencoder_distribution_name is not None),
            distribution_clipnorm=default_distribution_gradient_clipping_norm)

        discriminator_optimiser = configure_optimiser(
            optimiser=discriminator_optimiser,
            learning_rate=discriminator_learning_rate,
            decay=default_decay,
            clipnorm=default_gradient_clipping_norm,
            clipvalue=default_gradient_clipping_value,
            distribution_modelling=(
                self.discriminator_distribution_name is not None),
            distribution_clipnorm=default_distribution_gradient_clipping_norm)

        generator_optimiser = configure_optimiser(
            optimiser=generator_optimiser,
            learning_rate=generator_learning_rate,
            decay=default_decay,
            clipnorm=default_gradient_clipping_norm,
            clipvalue=default_gradient_clipping_value,
            distribution_modelling=(
                self.generator_distribution_name is not None),
            distribution_clipnorm=default_distribution_gradient_clipping_norm)

        self.autoencoder_optimiser = tfk.optimizers.get(autoencoder_optimiser)
        self.discriminator_optimiser = tfk.optimizers.get(
            discriminator_optimiser)
        self.generator_optimiser = tfk.optimizers.get(generator_optimiser)

    @property
    def optimisers(self):
        optimisers = {
            "autoencoder": self.autoencoder_optimiser,
            "discriminator": self.discriminator_optimiser,
            "generator": self.generator_optimiser}
        return optimisers

    @property
    def metrics(self):
        metrics = []
        if self.autoencoder_loss_metric is not None:
            metrics.append(self.autoencoder_loss_metric)
        if self.discriminator_loss_metric is not None:
            metrics.append(self.discriminator_loss_metric)
        if self.generator_loss_metric is not None:
            metrics.append(self.generator_loss_metric)
        if self.autoencoder_metrics is not None:
            metrics.extend(self.autoencoder_metrics)
        if self.discriminator_metrics is not None:
            metrics.extend(self.discriminator_metrics)
        if self.generator_metrics is not None:
            metrics.extend(self.generator_metrics)
        return metrics

    @property
    def metric_groups(self):
        metric_groups = self._metrics_grouped_by_kind()
        return [group for group in metric_groups.values()]

    def summary(self, **kwargs):
        self.true_distribution.build(())
        super().summary(self.feature_size, **kwargs)
        self.encoder.summary(self.feature_size, **kwargs)
        self.decoder.summary(self._decoder_input_shape, **kwargs)
        self.discriminator.summary(self._discriminator_input_shape, **kwargs)

    def add_reason_for_stopping_training(self, reason):
        if self.stopping_training_reasons is None:
            self.stopping_training_reasons = []
        self.stopping_training_reasons.append(reason)

    def update_hyperparameters(self, epoch):
        if self.gaussian_discriminator_sample_noise_decay:
            self.gaussian_discriminator_sample_noise_weight = (
                tf.math.pow(
                    self.gaussian_discriminator_sample_noise_decay, epoch))

    def call(self, inputs, training=None):
        if isinstance(inputs, tuple):
            inputs = inputs[0]

        samples = self.encoder(inputs, training=training)
        samples_for_decoder = self._prepare_latent_samples_for_decoder(samples)
        reconstructions = self.decoder(samples_for_decoder, training=training)
        samples_for_discriminator = (
            self._prepare_latent_samples_for_discriminator(samples))
        _ = self.discriminator(samples_for_discriminator, training=training)
        return reconstructions

    def train_step(self, inputs):

        # Reconstruction phase

        with tf.GradientTape() as autoencoder_tape:
            autoencoder_loss = self._compute_autoencoder_loss(
                inputs, training=True)

        trainable_autoencoder_variables = (
            self.encoder.trainable_variables
            + self.decoder.trainable_variables)
        autoencoder_gradients = autoencoder_tape.gradient(
            autoencoder_loss, trainable_autoencoder_variables)
        self.autoencoder_optimiser.apply_gradients(
            zip(autoencoder_gradients, trainable_autoencoder_variables))

        # Regularisation phase: Discriminator part

        with tf.GradientTape() as discriminator_tape:
            discriminator_loss = self._compute_discriminator_loss(
                inputs, training=True)
            effective_discriminator_loss = (
                self.discriminator_weight * discriminator_loss)

        discriminator_variables = (
            self.discriminator.trainable_variables
            + self.true_distribution.trainable_variables)

        discriminator_gradients = discriminator_tape.gradient(
            effective_discriminator_loss, discriminator_variables)
        self.discriminator_optimiser.apply_gradients(
            zip(discriminator_gradients, discriminator_variables))

        # Regularisation phase: Generator part

        with tf.GradientTape() as generator_tape:
            generator_loss = self._compute_generator_loss(
                inputs, training=True)
            effective_generator_loss = self.generator_weight * generator_loss

        generator_gradients = generator_tape.gradient(
            effective_generator_loss, self._generator_variables)
        self.generator_optimiser.apply_gradients(
            zip(generator_gradients, self._generator_variables))

        return {m.name: m.result() for m in self.metrics}

    def test_step(self, inputs):
        self._compute_autoencoder_loss(inputs, training=False)
        self._compute_discriminator_loss(inputs, training=False)
        self._compute_generator_loss(inputs, training=False)
        return {m.name: m.result() for m in self.metrics}

    def _compute_autoencoder_loss(self, inputs, training=None):
        if isinstance(inputs, tuple):
            inputs = inputs[0]

        samples = self.encoder(inputs, training=training)
        samples = self._prepare_latent_samples_for_decoder(samples)
        reconstructions = self.decoder(samples, training=training)
        losses = self.autoencoder_loss(
            _ensure_dense_format(inputs), reconstructions)
        loss = tf.nn.compute_average_loss(losses)

        self.autoencoder_loss_metric.update_state(losses)
        for metric in self.autoencoder_metrics:
            metric.update_state(inputs, reconstructions)

        return loss

    def _compute_discriminator_loss(self, inputs, training=None):
        if isinstance(inputs, tuple):
            inputs = inputs[0]

        if training is None:
            training = K.learning_phase()

        batch_size = tf.shape(inputs)[0]

        gaussian_sample_noise_scale_weight = (
            self.gaussian_discriminator_sample_noise_weight)

        generated_samples = self.encoder(inputs, training=training)
        generated_samples = self._prepare_latent_samples_for_discriminator(
            generated_samples)
        true_distribution = self.true_distribution(0.)
        true_samples = true_distribution.sample(
            tf.shape(generated_samples)[0])

        generated_labels = tf.zeros(shape=(batch_size, 1))
        true_labels = tf.ones(shape=(batch_size, 1))

        maybe_noisy_generated_samples = generated_samples
        maybe_noisy_true_samples = true_samples
        maybe_noisy_generated_labels = generated_labels
        maybe_noisy_true_labels = true_labels

        if training:
            maybe_noisy_generated_samples, maybe_noisy_generated_labels = (
                self.discriminator_noise(
                    # TP distribution does not seem to be coerced correctly
                    # when passed to external function, so it is explicitly
                    # converted to a tensor instead
                    tf.convert_to_tensor(generated_samples), generated_labels,
                    gaussian_sample_noise_scale_weight))
            maybe_noisy_true_samples, maybe_noisy_true_labels = (
                self.discriminator_noise(
                    true_samples, true_labels,
                    gaussian_sample_noise_scale_weight))

        generated_predictions = self.discriminator(
            maybe_noisy_generated_samples, training=training)
        generated_losses = self.discriminator_loss(
            maybe_noisy_generated_labels, generated_predictions)
        generated_loss = tf.nn.compute_average_loss(generated_losses)

        true_predictions = self.discriminator(
            maybe_noisy_true_samples, training=training)
        true_losses = self.discriminator_loss(
            maybe_noisy_true_labels, true_predictions)
        true_loss = tf.nn.compute_average_loss(true_losses)

        loss = generated_loss + true_loss

        self.discriminator_loss_metric.update_state(generated_losses)
        self.discriminator_loss_metric.update_state(true_losses)
        for metric in self.discriminator_metrics:
            metric.update_state(generated_labels, generated_predictions)
            metric.update_state(true_labels, true_predictions)

        return loss

    def _compute_generator_loss(self, inputs, training=None):
        if isinstance(inputs, tuple):
            inputs = inputs[0]

        batch_size = tf.shape(inputs)[0]
        labels = tf.ones(shape=(batch_size, 1))

        samples = self.encoder(inputs, training=training)
        samples = self._prepare_latent_samples_for_discriminator(samples)
        predictions = self.discriminator(samples, training=training)
        losses = self.generator_loss(labels, predictions)
        loss = tf.nn.compute_average_loss(losses)

        self.generator_loss_metric.update_state(losses)
        for metric in self.generator_metrics:
            metric.update_state(labels, predictions)

        return loss

    def _metrics_grouped_by_kind(self):
        metric_groups = {}

        _add_loss_to_metric_groups(
            self.autoencoder_loss, self.autoencoder_loss_metric,
            metric_groups)
        _add_loss_to_metric_groups(
            self.discriminator_loss, self.discriminator_loss_metric,
            metric_groups)
        _add_loss_to_metric_groups(
            self.generator_loss, self.generator_loss_metric,
            metric_groups)

        _add_metrics_to_metric_groups(
            self.autoencoder_metrics, metric_groups)
        _add_metrics_to_metric_groups(
            self.discriminator_metrics, metric_groups)
        _add_metrics_to_metric_groups(
            self.generator_metrics, metric_groups)

        return metric_groups

    @property
    def _decoder_input_shape(self):
        return self.latent_size

    @property
    def _discriminator_input_shape(self):
        return self.latent_size

    @staticmethod
    def _prepare_latent_samples_for_decoder(samples):
        return samples

    @staticmethod
    def _prepare_latent_samples_for_discriminator(samples):
        return samples

    @property
    def _generator_variables(self):
        return self.encoder.trainable_variables


@_register_adversarial_autoencoder()
class CategoricalAdversarialAutoEncoder(AdversarialAutoEncoder):
    KIND = "categorical"

    def __init__(self,
                 feature_size,
                 intermediate_sizes=(256, 128),
                 latent_size=32,
                 category_count=2,
                 autoencoder_distribution=None,
                 autoencoder_loss=None,
                 autoencoder_metrics=None,
                 autoencoder_activation=None,
                 discriminator_intermediate_sizes=None,
                 discriminator_distribution=None,
                 discriminator_loss=None,
                 discriminator_weight=1.,
                 discriminator_metrics="accuracy",
                 discriminator_activation=None,
                 discriminator_label_flipping_rate=None,
                 discriminator_label_smoothing_scale=0.1,
                 gaussian_discriminator_sample_noise_scale=None,
                 gaussian_discriminator_sample_noise_decay=None,
                 gaussian_discriminator_label_noise_scale=None,
                 generator_distribution=None,
                 generator_loss=None,
                 generator_weight=1.,
                 generator_metrics=None,
                 categorical_discriminator_distribution=None,
                 categorical_discriminator_loss=None,
                 categorical_discriminator_weight=1.,
                 categorical_discriminator_metrics=None,
                 categorical_discriminator_activation=None,
                 categorical_discriminator_label_flipping_rate=None,
                 categorical_discriminator_label_smoothing_scale=None,
                 gaussian_categorical_discriminator_sample_noise_scale=None,
                 gaussian_categorical_discriminator_sample_noise_decay=None,
                 gaussian_categorical_discriminator_label_noise_scale=None,
                 categorical_generator_distribution=None,
                 categorical_generator_loss=None,
                 categorical_generator_weight=1.,
                 categorical_generator_metrics=None,
                 categorical_encoder_temperature=None,
                 learn_categorical_encoder_temperature=False,
                 learn_true_categorical_probabilities=False,
                 true_categorical_temperature=None,
                 learn_true_categorical_temperature=False,
                 intermediate_activation="leaky_relu",
                 intermediate_normalisation="batch",
                 intermediate_dropout_rate=0.1,
                 name="categorical_adversarial_autoencoder"):
        super().__init__(
            feature_size=feature_size,
            intermediate_sizes=intermediate_sizes,
            latent_size=latent_size,
            category_count=None,
            autoencoder_distribution=autoencoder_distribution,
            autoencoder_loss=autoencoder_loss,
            autoencoder_metrics=autoencoder_metrics,
            autoencoder_activation=autoencoder_activation,
            discriminator_intermediate_sizes=discriminator_intermediate_sizes,
            discriminator_distribution=discriminator_distribution,
            discriminator_loss=discriminator_loss,
            discriminator_weight=discriminator_weight,
            generator_weight=generator_weight,
            discriminator_metrics=discriminator_metrics,
            discriminator_activation=discriminator_activation,
            discriminator_label_flipping_rate=(
                discriminator_label_flipping_rate),
            discriminator_label_smoothing_scale=(
                discriminator_label_smoothing_scale),
            gaussian_discriminator_sample_noise_scale=(
                gaussian_discriminator_sample_noise_scale),
            gaussian_discriminator_sample_noise_decay=(
                gaussian_discriminator_sample_noise_decay),
            gaussian_discriminator_label_noise_scale=(
                gaussian_discriminator_label_noise_scale),
            generator_distribution=generator_distribution,
            generator_loss=generator_loss,
            generator_metrics=generator_metrics,
            intermediate_activation=intermediate_activation,
            intermediate_normalisation=intermediate_normalisation,
            intermediate_dropout_rate=intermediate_dropout_rate,
            name=name)

        categorical_discriminator_distribution = (
            categorical_discriminator_distribution
            or discriminator_distribution)
        categorical_discriminator_loss = (
            categorical_discriminator_loss or discriminator_loss)
        categorical_discriminator_metrics = (
            categorical_discriminator_metrics or discriminator_metrics)
        (categorical_discriminator_distribution,
         categorical_discriminator_loss,
         categorical_discriminator_activation) = (
            _check_distribution_loss_and_activation_functions(
                categorical_discriminator_distribution,
                categorical_discriminator_loss,
                categorical_discriminator_activation,
                model_name="categorical_discriminator"))
        categorical_discriminator_activation = _check_activation(
            categorical_discriminator_activation)

        categorical_generator_distribution = (
            categorical_generator_distribution
            or categorical_discriminator_distribution)
        categorical_generator_loss = (
            categorical_generator_loss or categorical_discriminator_loss)
        categorical_generator_metrics = (
            categorical_generator_metrics or categorical_discriminator_metrics)
        categorical_generator_distribution, categorical_generator_loss, __ = (
            _check_distribution_loss_and_activation_functions(
                categorical_generator_distribution,
                categorical_generator_loss,
                model_name="categorical_generator"))

        categorical_discriminator_label_flipping_rate = (
            categorical_discriminator_label_flipping_rate
            or discriminator_label_flipping_rate)
        categorical_discriminator_label_smoothing_scale = (
            categorical_discriminator_label_smoothing_scale
            or discriminator_label_smoothing_scale)
        gaussian_categorical_discriminator_sample_noise_scale = (
            gaussian_categorical_discriminator_sample_noise_scale
            or gaussian_discriminator_sample_noise_scale)
        gaussian_categorical_discriminator_sample_noise_decay = (
            gaussian_categorical_discriminator_sample_noise_decay
            or gaussian_discriminator_sample_noise_decay)
        gaussian_categorical_discriminator_label_noise_scale = (
            gaussian_categorical_discriminator_label_noise_scale
            or gaussian_discriminator_label_noise_scale)

        self.category_count = category_count
        self.categorical_discriminator_distribution_name = (
            categorical_discriminator_distribution)
        self.categorical_discriminator_loss_name = (
            categorical_discriminator_loss)
        self.categorical_discriminator_weight = check_float(
            categorical_discriminator_weight)
        self.categorical_discriminator_metric_names = check_list(
            categorical_discriminator_metrics)
        self.categorical_discriminator_activation = (
            categorical_discriminator_activation)
        self.categorical_discriminator_label_flipping_rate = (
            categorical_discriminator_label_flipping_rate)
        self.categorical_discriminator_label_smoothing_scale = (
            categorical_discriminator_label_smoothing_scale)
        self.gaussian_categorical_discriminator_sample_noise_scale = (
            gaussian_categorical_discriminator_sample_noise_scale)
        self.gaussian_categorical_discriminator_sample_noise_decay = (
            gaussian_categorical_discriminator_sample_noise_decay)
        self.gaussian_categorical_discriminator_label_noise_scale = (
            gaussian_categorical_discriminator_label_noise_scale)
        self.categorical_generator_distribution_name = (
            categorical_generator_distribution)
        self.categorical_generator_loss_name = categorical_generator_loss
        self.categorical_generator_weight = check_float(
            categorical_generator_weight)
        self.categorical_generator_metric_names = check_list(
            categorical_generator_metrics)
        self.categorical_encoder_temperature = categorical_encoder_temperature
        self.learn_categorical_encoder_temperature = (
            learn_categorical_encoder_temperature)
        self.learn_true_categorical_probabilities = (
            learn_true_categorical_probabilities)
        self.true_categorical_temperature = (
            true_categorical_temperature)
        self.learn_true_categorical_temperature = (
            learn_true_categorical_temperature)

        self.encoder = CategoricalEncoder(
            latent_size=self.latent_size,
            intermediate_sizes=self.intermediate_sizes,
            intermediate_activation=self.intermediate_activation,
            intermediate_normalisation=self.intermediate_normalisation,
            intermediate_dropout_rate=self.intermediate_dropout_rate,
            category_count=self.category_count,
            categorical_temperature=self.categorical_encoder_temperature,
            learn_categorical_temperature=(
                self.learn_categorical_encoder_temperature))
        self.categorical_discriminator = CategoricalDiscriminator(
            intermediate_sizes=self.discriminator_intermediate_sizes,
            intermediate_activation=self.intermediate_activation,
            intermediate_normalisation=self.intermediate_normalisation,
            intermediate_dropout_rate=self.intermediate_dropout_rate,
            verdict_distribution=(
                self.categorical_discriminator_distribution_name),
            verdict_activation=self.categorical_discriminator_activation)
        self.true_categorical_distribution = (
            distributions.CategoricalDistribution(
                category_count=self.category_count,
                learn_probabilities=self.learn_true_categorical_probabilities,
                temperature=self.true_categorical_temperature,
                learn_temperature=self.learn_true_categorical_temperature,
                name="true_categorical"))

        self.categorical_discriminator_optimiser = None
        if self.categorical_discriminator_loss_name is not None:
            self.categorical_discriminator_loss = tfk.losses.get(
                self.categorical_discriminator_loss_name)
        elif self.categorical_discriminator_distribution_name is not None:
            self.categorical_discriminator_loss = NegativeLogLikelihood()
        self.categorical_discriminator_loss.reduction = (
            tfk.losses.Reduction.NONE)
        self.categorical_discriminator_loss_metric = tfk.metrics.Mean(
            name="categorical_discriminator_loss")
        self.categorical_discriminator_metrics = [
            MeanMetric(metric, name_prefix="categorical_discriminator")
            for metric in self.categorical_discriminator_metric_names]

        self.categorical_discriminator_noise = _noise_function(
            label_flipping_rate=(
                self.categorical_discriminator_label_flipping_rate),
            label_smoothing_scale=(
                self.categorical_discriminator_label_smoothing_scale),
            gaussian_sample_noise_scale=(
                self.gaussian_categorical_discriminator_sample_noise_scale),
            gaussian_label_noise_scale=(
                self.gaussian_categorical_discriminator_label_noise_scale))
        self.gaussian_categorical_discriminator_sample_noise_weight = 1.

        self.categorical_generator_optimiser = None
        if self.categorical_generator_loss_name is not None:
            self.categorical_generator_loss = tfk.losses.get(
                self.categorical_generator_loss_name)
        elif self.categorical_generator_distribution_name is not None:
            self.categorical_generator_loss = NegativeLogLikelihood()
        self.categorical_generator_loss.reduction = tfk.losses.Reduction.NONE
        self.categorical_generator_loss_metric = tfk.metrics.Mean(
            name="categorical_generator_loss")
        self.categorical_generator_metrics = [
            MeanMetric(metric, name_prefix="categorical_generator")
            for metric in self.categorical_generator_metric_names]

    def get_config(self):
        config = super().get_config()
        config.update({
            "category_count": self.category_count,
            "categorical_discriminator_distribution": (
                self.categorical_discriminator_distribution_name),
            "categorical_discriminator_loss": (
                self.categorical_discriminator_loss_name),
            "categorical_discriminator_weight": (
                self.categorical_discriminator_weight),
            "categorical_discriminator_metrics": (
                self.categorical_discriminator_metric_names),
            "categorical_discriminator_activation": (
                self.categorical_discriminator_activation),
            "categorical_discriminator_label_flipping_rate": (
                self.categorical_discriminator_label_flipping_rate),
            "categorical_discriminator_label_smoothing_scale": (
                self.categorical_discriminator_label_smoothing_scale),
            "gaussian_categorical_discriminator_sample_noise_scale": (
                self.gaussian_categorical_discriminator_sample_noise_scale),
            "gaussian_categorical_discriminator_sample_noise_decay": (
                self.gaussian_categorical_discriminator_sample_noise_decay),
            "gaussian_categorical_discriminator_label_noise_scale": (
                self.gaussian_categorical_discriminator_label_noise_scale),
            "categorical_generator_distribution": (
                self.categorical_generator_distribution_name),
            "categorical_generator_loss": (
                self.categorical_generator_loss_name),
            "categorical_generator_weight": self.categorical_generator_weight,
            "categorical_generator_metrics": (
                self.categorical_generator_metric_names),
            "categorical_encoder_temperature": (
                self.categorical_encoder_temperature),
            "learn_categorical_encoder_temperature": (
                self.learn_categorical_encoder_temperature),
            "learn_true_categorical_probabilities": (
                self.learn_true_categorical_probabilities),
            "true_categorical_temperature": (
                self.true_categorical_temperature),
            "learn_true_categorical_temperature": (
                self.learn_true_categorical_temperature)})
        return config

    def compile(self,
                autoencoder_optimiser=None,
                discriminator_optimiser=None,
                generator_optimiser=None,
                categorical_discriminator_optimiser=None,
                categorical_generator_optimiser=None,
                default_optimiser_name="adam",
                autoencoder_learning_rate=1e-4,
                discriminator_learning_rate=1e-5,
                generator_learning_rate=1e-5,
                categorical_discriminator_learning_rate=None,
                categorical_generator_learning_rate=None,
                default_decay=1e-6,
                default_gradient_clipping_norm=None,
                default_gradient_clipping_value=None,
                default_distribution_gradient_clipping_norm=3,
                **kwargs):

        super().compile(
            autoencoder_optimiser=autoencoder_optimiser,
            discriminator_optimiser=discriminator_optimiser,
            generator_optimiser=generator_optimiser,
            default_optimiser_name=default_optimiser_name,
            autoencoder_learning_rate=autoencoder_learning_rate,
            discriminator_learning_rate=(
                discriminator_learning_rate),
            generator_learning_rate=generator_learning_rate,
            default_decay=default_decay,
            default_gradient_clipping_norm=default_gradient_clipping_norm,
            default_gradient_clipping_value=default_gradient_clipping_value,
            default_distribution_gradient_clipping_norm=(
                default_distribution_gradient_clipping_norm),
            **kwargs)

        # IDEA: Use corresponding continuous optimiser, if specified.
        categorical_discriminator_optimiser = (
            categorical_discriminator_optimiser or default_optimiser_name)
        categorical_generator_optimiser = (
            categorical_generator_optimiser or default_optimiser_name)

        categorical_discriminator_learning_rate = (
            categorical_discriminator_learning_rate
            or discriminator_learning_rate)
        categorical_generator_learning_rate = (
            categorical_generator_learning_rate
            or generator_learning_rate)

        categorical_discriminator_optimiser = configure_optimiser(
            optimiser=categorical_discriminator_optimiser,
            learning_rate=categorical_discriminator_learning_rate,
            decay=default_decay,
            clipnorm=default_gradient_clipping_norm,
            clipvalue=default_gradient_clipping_value,
            distribution_modelling=(
                self.categorical_discriminator_distribution_name is not None),
            distribution_clipnorm=default_distribution_gradient_clipping_norm)

        categorical_generator_optimiser = configure_optimiser(
            optimiser=categorical_generator_optimiser,
            learning_rate=categorical_generator_learning_rate,
            decay=default_decay,
            clipnorm=default_gradient_clipping_norm,
            clipvalue=default_gradient_clipping_value,
            distribution_modelling=(
                self.categorical_generator_distribution_name is not None),
            distribution_clipnorm=default_distribution_gradient_clipping_norm)

        self.categorical_discriminator_optimiser = tfk.optimizers.get(
            categorical_discriminator_optimiser)
        self.categorical_generator_optimiser = tfk.optimizers.get(
            categorical_generator_optimiser)

    @property
    def optimisers(self):
        optimisers = super().optimisers
        optimisers.update({
            "categorical_discriminator": (
                self.categorical_discriminator_optimiser),
            "categorical_generator": self.categorical_generator_optimiser})
        return optimisers

    @property
    def metrics(self):
        metrics = super().metrics
        if self.categorical_discriminator_loss_metric is not None:
            metrics.append(self.categorical_discriminator_loss_metric)
        if self.categorical_generator_loss_metric is not None:
            metrics.append(self.categorical_generator_loss_metric)
        if self.categorical_discriminator_metrics is not None:
            metrics.extend(self.categorical_discriminator_metrics)
        if self.categorical_generator_metrics is not None:
            metrics.extend(self.categorical_generator_metrics)
        return metrics

    def summary(self, **kwargs):
        self.true_categorical_distribution.build(())
        super().summary(**kwargs)
        self.categorical_discriminator.summary(
            self._categorical_discriminator_input_shape, **kwargs)

    def update_hyperparameters(self, epoch):
        super().update_hyperparameters(epoch=epoch)
        if self.gaussian_categorical_discriminator_sample_noise_decay:
            self.gaussian_categorical_discriminator_sample_noise_weight = (
                tf.math.pow(
                    self.gaussian_categorical_discriminator_sample_noise_decay,
                    epoch))

    def call(self, inputs, training=None):
        if isinstance(inputs, tuple):
            inputs = inputs[0]

        samples = self.encoder(inputs, training=training)
        samples_for_categorical_discriminator = (
            self._prepare_latent_samples_for_categorical_discriminator(
                samples))
        _ = self.categorical_discriminator(
            samples_for_categorical_discriminator, training=training)

        reconstructions = super().call(inputs=inputs, training=training)
        return reconstructions

    def train_step(self, inputs):
        super().train_step(inputs=inputs)

        # Regularisation phase: Categorical discriminator part

        with tf.GradientTape() as categorical_discriminator_tape:
            categorical_discriminator_loss = (
                self._compute_categorical_discriminator_loss(
                    inputs, training=True))
            effective_categorical_discriminator_loss = (
                self.categorical_discriminator_weight
                * categorical_discriminator_loss)

        categorical_discriminator_variables = (
            self.categorical_discriminator.trainable_variables
            + self.true_categorical_distribution.trainable_variables)

        categorical_discriminator_gradients = (
            categorical_discriminator_tape.gradient(
                effective_categorical_discriminator_loss,
                categorical_discriminator_variables))
        self.categorical_discriminator_optimiser.apply_gradients(
            zip(categorical_discriminator_gradients,
                categorical_discriminator_variables))

        # Regularisation phase: Categorical generator part

        with tf.GradientTape() as categorical_generator_tape:
            categorical_generator_loss = (
                self._compute_categorical_generator_loss(
                    inputs, training=True))
            effective_categorical_generator_loss = (
                self.categorical_generator_weight * categorical_generator_loss)

        categorical_generator_gradients = categorical_generator_tape.gradient(
            effective_categorical_generator_loss,
            self._categorical_generator_variables)
        self.categorical_generator_optimiser.apply_gradients(zip(
            categorical_generator_gradients,
            self._categorical_generator_variables))

        return {m.name: m.result() for m in self.metrics}

    def test_step(self, inputs):
        super().test_step(inputs=inputs)
        self._compute_categorical_discriminator_loss(inputs, training=False)
        self._compute_categorical_generator_loss(inputs, training=False)
        return {m.name: m.result() for m in self.metrics}

    def _compute_categorical_discriminator_loss(self, inputs, training=None):
        if isinstance(inputs, tuple):
            inputs = inputs[0]

        if training is None:
            training = K.learning_phase()

        batch_size = tf.shape(inputs)[0]

        gaussian_sample_noise_scale_weight = (
            self.gaussian_categorical_discriminator_sample_noise_weight)

        generated_samples = self.encoder(inputs, training=training)
        generated_samples = (
            self._prepare_latent_samples_for_categorical_discriminator(
                generated_samples))
        categorical_distribution = (
            self.true_categorical_distribution.distribution)
        true_samples = categorical_distribution.sample(
            tf.shape(generated_samples)[0])

        generated_labels = tf.zeros(shape=(batch_size, 1))
        true_labels = tf.ones(shape=(batch_size, 1))

        maybe_noisy_generated_samples = generated_samples
        maybe_noisy_true_samples = true_samples
        maybe_noisy_generated_labels = generated_labels
        maybe_noisy_true_labels = true_labels

        if training:
            maybe_noisy_generated_samples, maybe_noisy_generated_labels = (
                self.categorical_discriminator_noise(
                    # TP distribution does not seem to be coerced correctly
                    # when passed to external function, so it is explicitly
                    # converted to a tensor instead
                    tf.convert_to_tensor(generated_samples), generated_labels,
                    gaussian_sample_noise_scale_weight))
            maybe_noisy_true_samples, maybe_noisy_true_labels = (
                self.categorical_discriminator_noise(
                    true_samples, true_labels,
                    gaussian_sample_noise_scale_weight))

        generated_predictions = self.categorical_discriminator(
            maybe_noisy_generated_samples, training=training)
        generated_losses = self.categorical_discriminator_loss(
            maybe_noisy_generated_labels, generated_predictions)
        generated_loss = tf.nn.compute_average_loss(generated_losses)

        true_predictions = self.categorical_discriminator(
            maybe_noisy_true_samples, training=training)
        true_losses = self.categorical_discriminator_loss(
            maybe_noisy_true_labels, true_predictions)
        true_loss = tf.nn.compute_average_loss(true_losses)

        loss = generated_loss + true_loss

        self.categorical_discriminator_loss_metric.update_state(
            generated_losses)
        self.categorical_discriminator_loss_metric.update_state(true_losses)
        for metric in self.categorical_discriminator_metrics:
            metric.update_state(generated_labels, generated_predictions)
            metric.update_state(true_labels, true_predictions)

        return loss

    def _compute_categorical_generator_loss(self, inputs, training=None):
        if isinstance(inputs, tuple):
            inputs = inputs[0]

        batch_size = tf.shape(inputs)[0]
        labels = tf.ones(shape=(batch_size, 1))

        samples = self.encoder(inputs, training=training)
        samples = self._prepare_latent_samples_for_categorical_discriminator(
            samples)
        predictions = self.categorical_discriminator(
            samples, training=training)
        losses = self.categorical_generator_loss(labels, predictions)
        loss = tf.nn.compute_average_loss(losses)

        self.categorical_generator_loss_metric.update_state(losses)
        for metric in self.categorical_generator_metrics:
            metric.update_state(labels, predictions)

        return loss

    def _metrics_grouped_by_kind(self):
        metric_groups = super()._metrics_grouped_by_kind()

        _add_loss_to_metric_groups(
            self.categorical_discriminator_loss,
            self.categorical_discriminator_loss_metric,
            metric_groups)
        _add_loss_to_metric_groups(
            self.categorical_generator_loss,
            self.categorical_generator_loss_metric,
            metric_groups)

        _add_metrics_to_metric_groups(
            self.categorical_discriminator_metrics, metric_groups)
        _add_metrics_to_metric_groups(
            self.categorical_generator_metrics, metric_groups)

        return metric_groups

    @property
    def _decoder_input_shape(self):
        return self.latent_size + self.category_count

    @property
    def _discriminator_input_shape(self):
        return self.latent_size

    @property
    def _categorical_discriminator_input_shape(self):
        return self.category_count

    @staticmethod
    def _prepare_latent_samples_for_decoder(samples):
        latent_representation_samples, latent_category_samples = samples
        latent_category_samples = tf.cast(
            latent_category_samples, dtype=latent_representation_samples.dtype)
        samples = tf.concat(
            [latent_representation_samples, latent_category_samples],
            axis=-1)
        return samples

    @staticmethod
    def _prepare_latent_samples_for_discriminator(samples):
        latent_representation_samples, __ = samples
        return latent_representation_samples

    @staticmethod
    def _prepare_latent_samples_for_categorical_discriminator(samples):
        __, latent_category_samples = samples
        return latent_category_samples

    @property
    def _generator_variables(self):
        return self._generator_variables_from_distribution_name(
            self.encoder.latent_representation.name)

    @property
    def _categorical_generator_variables(self):
        return self._generator_variables_from_distribution_name(
            self.encoder.latent_category.name)

    def _generator_variables_from_distribution_name(self, distribution_name):
        encoder_variables = self.encoder.trainable_variables
        return [
            v for v in encoder_variables
            if "intermediate" in v.name or distribution_name in v.name]


def get_adversarial_autoencoder(config=None):
    kind = config.pop("model_kind", None)
    cls = MODELS.get(kind)
    if cls is None:
        raise ValueError(f"Model of kind `{kind}` not found.")
    config = check_dict(config)
    return cls.from_config(config)


def is_categorical(model):
    return isinstance(
        model, (CategoricalAdversarialAutoEncoder, CategoricalEncoder))


def _noise_function(label_flipping_rate=None,
                    label_smoothing_scale=None,
                    gaussian_sample_noise_scale=None,
                    gaussian_label_noise_scale=None):
    @tf.function
    def _maybe_make_noisy(samples, labels,
                          gaussian_sample_noise_scale_weight=1.):
        if label_flipping_rate:
            labels = noise_models.flip_binary_labels(
                labels, rate=label_flipping_rate)
        if label_smoothing_scale:
            labels = noise_models.smooth_binary_labels(
                labels, scale=label_smoothing_scale)
        if gaussian_sample_noise_scale:
            effective_gaussian_sample_noise_scale = (
                gaussian_sample_noise_scale_weight *
                gaussian_sample_noise_scale)
            samples = noise_models.add_gaussian_noise(
                samples, scale=effective_gaussian_sample_noise_scale)
        if gaussian_label_noise_scale:
            labels = noise_models.add_gaussian_noise(
                labels, scale=gaussian_label_noise_scale)
        return samples, labels
    return _maybe_make_noisy


def _add_loss_to_metric_groups(loss, loss_metric, metric_groups):
    if loss is not None and loss_metric is not None:
        metric_groups.setdefault(loss, []).append(loss_metric.name)


def _add_metrics_to_metric_groups(metrics, metric_groups):
    if metrics is not None:
        for metric in metrics:
            metric_groups.setdefault(metric.metric, []).append(
                metric.name)


def _check_distribution_loss_and_activation_functions(distribution_name=None,
                                                      loss_name=None,
                                                      activation_name=None,
                                                      model_name=None):
    if distribution_name is not None and (
            loss_name is not None or activation_name is not None):
        error_message_parts = []
        if model_name is not None:
            error_message_parts.append(f"for the {model_name},")
        error_message_parts.append(
            f"a distribution (`{distribution_name}`) cannot be specified "
            "together with")
        loss_and_or_activation_parts = []
        if loss_name is not None:
            loss_and_or_activation_parts.append(
                f"a loss function (`{loss_name}`)")
        if activation_name is not None:
            loss_and_or_activation_parts.append(
                f"an activation function (`{activation_name}`)")
        loss_and_or_activation = " or ".join(loss_and_or_activation_parts)
        error_message_parts.append(loss_and_or_activation)
        error_message = " ".join(error_message_parts).capitalize()
        error_message += "."
        raise ValueError(error_message)
    if distribution_name is None and loss_name is None:
        if model_name is not None:
            loss_name = DEFAULT_LOSSES.get(model_name)
            if loss_name is None:
                raise ValueError(
                    f"Default loss function for model `{model_name}` "
                    "not found.")
        else:
            raise ValueError(
                "Cannot get default loss function without specifying model "
                "name.")
    if loss_name is not None and activation_name is None:
        activation_name = DEFAULT_ACTIVATIONS.get(loss_name)
    return distribution_name, loss_name, activation_name


def _check_activation(identifier):
    if not isinstance(identifier, dict):
        identifier = ACTIVATION_ALIASES.get(identifier, identifier)
        identifier = {"class_name": identifier, "config": {}}
    class_name = identifier.get("class_name")
    config = identifier.get("config", {})
    default_config = DEFAULT_ACTIVATION_CONFIGS.get(class_name, {})
    for default_config_name, default_config_value in default_config.items():
        config.setdefault(default_config_name, default_config_value)
    if not config:
        identifier = class_name
    return identifier


def _ensure_dense_format(inputs):
    if isinstance(inputs, tf.SparseTensor):
        inputs = tf.sparse.to_dense(inputs)
    return inputs
