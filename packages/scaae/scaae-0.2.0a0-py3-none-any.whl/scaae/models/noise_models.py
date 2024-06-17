import tensorflow as tf


def add_gaussian_noise(inputs, scale=0.05):
    noise = tf.random.normal(shape=tf.shape(inputs), stddev=scale)
    return inputs + noise


def smooth_binary_labels(labels, scale=0.1):
    noise = tf.random.uniform(
        shape=tf.shape(labels), minval=0, maxval=scale)
    noise = tf.where(tf.cast(labels, dtype="bool"), -noise, noise)
    return labels + noise


def flip_binary_labels(labels, rate=0.1):
    noise = tf.random.uniform(shape=tf.shape(labels), minval=0, maxval=1)
    outputs = tf.cast(labels, dtype="bool")
    outputs = tf.where(
        noise >= rate, outputs, tf.math.logical_not(outputs))
    return tf.cast(outputs, dtype=labels.dtype)
