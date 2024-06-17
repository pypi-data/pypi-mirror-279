from tensorflow import keras as tfk
from tensorflow.keras import layers as tfkl

from scaae import utilities

_ACTIVATION_LAYER_CLASSES = {
    "LeakyReLU": tfkl.LeakyReLU}


class Dense(tfkl.Layer):
    def __init__(self, units, activation=None, normalisation=None,
                 dropout_rate=None, name=None, dtype=None):
        super().__init__(name=name, dtype=dtype)

        self.activation_identifier = activation
        self.normalisation_name = normalisation
        self.dropout_rate = dropout_rate

        if name:
            dense_layer_name = "dense"
            normalisation_layer_name = "normalisation"
            activation_layer_name = "activation"
            dropout_layer_name = "dropout"
        else:
            dense_layer_name = None
            normalisation_layer_name = None
            activation_layer_name = None
            dropout_layer_name = None

        self.dense = tfkl.Dense(
            units, activation=None, name=dense_layer_name, dtype=dtype)

        self.normalisation = None
        if self.normalisation_name == "batch":
            self.normalisation = tfkl.BatchNormalization(
                name=normalisation_layer_name, dtype=dtype)
        elif self.normalisation_name == "layer":
            self.normalisation = tfkl.LayerNormalization(
                name=normalisation_layer_name, dtype=dtype)
        elif self.normalisation_name is None:
            pass
        else:
            raise ValueError(
                f"Normalisation method {self.normalisation_name} not found.")

        self.activation = tfkl.Activation(
            _activation_function(self.activation_identifier),
            name=activation_layer_name,
            dtype=dtype)

        if self.dropout_rate is not None:
            self.dropout = tfkl.Dropout(
                self.dropout_rate, name=dropout_layer_name, dtype=dtype)

    def call(self, inputs, training=None):
        outputs = self.dense(inputs)
        if self.normalisation is not None:
            outputs = self.normalisation(outputs, training=training)
        outputs = self.activation(outputs)
        if self.dropout_rate is not None:
            outputs = self.dropout(outputs, training=training)
        return outputs


def _activation_function(identifier):
    if isinstance(identifier, dict):
        class_name = identifier.get("class_name")
        config = identifier.get("config", {})
        cls = _ACTIVATION_LAYER_CLASSES.get(class_name)
        if cls:
            identifier = cls.from_config(config)
    return identifier


class DenseBlock(tfkl.Layer):
    def __init__(self, block_units, activation=None, normalisation=None,
                 dropout_rate=None, name=None, dtype=None):
        super().__init__(name=name, dtype=dtype)
        self.activation = activation
        self.normalisation = normalisation
        self.dropout_rate = dropout_rate
        self.block_units = utilities.check_list(block_units, not_empty=True)
        self.block = []
        for number, units in enumerate(self.block_units):
            dense = Dense(
                units,
                activation=self.activation,
                normalisation=self.normalisation,
                dropout_rate=self.dropout_rate,
                name=f"{number}",
                dtype=dtype)
            self.block.append(dense)

    def call(self, inputs, training=None):
        outputs = inputs
        for dense in self.block:
            outputs = dense(outputs, training=training)
        return outputs


class Model(tfk.Model):
    KIND = None

    def summary(self, input_size, print_fn=None, **kwargs):
        strategy = self.distribute_strategy
        with strategy.scope():
            self.build((None, input_size))
        self.call(tfkl.Input(shape=input_size))
        super().summary(print_fn=print_fn, **kwargs)
        if print_fn is None:
            print_fn = print
        submodel_trainable_variable_names = set()
        for layer in self.layers:
            if isinstance(layer, Model):
                for variable in layer.trainable_variables:
                    submodel_trainable_variable_names.add(variable.name)
        model_trainable_variables = [
            variable for variable in self.trainable_variables
            if variable.name not in submodel_trainable_variable_names]
        if model_trainable_variables:
            print_fn("Trainable parameters:")
        for variable in model_trainable_variables:
            print_fn(f"{variable.name}: {variable.shape}")
        print_fn()

    def get_config(self):
        try:
            config = super().get_config()
        except NotImplementedError:
            config = {}
        config.setdefault("model_kind", self.KIND)
        return config

    @classmethod
    def from_config(cls, config, **kwargs):
        config.pop("model_kind", None)
        try:
            model = cls(**config, **kwargs)
        except TypeError as error:
            raise TypeError(
                f"{error} (specified for {cls} in model configuration "
                "or using keyword arguments)")
        return model


class MeanMetric(tfk.metrics.Mean):

    def __init__(self, metric, name_prefix=None):
        name = None

        if metric in ["accuracy", "crossentropy"]:
            name = metric
            metric = f"binary_{metric}"

        self.metric = tfk.metrics.get(metric)

        if name is None:
            if hasattr(metric, "name"):
                name = self.metric.name
            else:
                name = self.metric.__name__

        if name_prefix and not name.startswith(name_prefix):
            name = f"{name_prefix}_{name}"

        super().__init__(name=name)

    def update_state(self, y_true, y_pred, sample_weight=None):
        metric = self.metric(y_true, y_pred)
        return super().update_state(metric, sample_weight=sample_weight)
