# scAAE

Command-line tool for single-cell RNA-sequencing analysis with adversarial autoencoders.

## Installation

scAAE requires Python 3.7--3.10. We recommend installing scAAE in a virtual environment using, for example, [Conda][].

scAAE can be installed using [pip][]:

    $ python3 -m pip install scaae

To accelerate clustering using [supported GPUs][RAPIDS-requirements], install scAAE with [RAPIDS][]:

    $ python3 -m pip install scaae[rapids] --extra-index-url https://pypi.nvidia.com

[Conda]: https://conda.io/
[pip]: https://pip.pypa.io/
[RAPIDS]: https://rapids.ai/
[RAPIDS-requirements]: https://docs.rapids.ai/install#system-req

### Local installation

1. [Clone][] or download the repository.

2. Open the root directory of the repository in a terminal.

3. Install scAAE using pip:

    * Standard installation:

          $ python3 -m pip install -e .

    * With RAPIDS:

          $ python3 -m pip install -e .[rapids] --extra-index-url https://pypi.nvidia.com

[clone]: https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository

## Quick tutorial

### Unsupervised scAAE model

Train an scAAE model on a data set (`training_set.h5ad`) using early stopping with an unsupervised clustering metric (for example, silhouette coefficient) with a validation set (`validation_set.h5ad`):

    $ scaae train training_set.h5ad --vp validation_set.h5ad --es silhouette_coefficient \
    > -o unsupervised_model

The model is saved to a directory named `unsupervised_model`.

Evaluate the model on another data set (`test_set.h5ad`):

    $ scaae evaluate test_set.h5ad -m unsupervised_model -o evaluation-unsupervised

### Semi-supervised scAAE model

Train an scAAE model on a data set (`training_set.h5ad`) using early stopping with a supervised clustering metric (for example, adjusted Rand index) with a validation set (`validation_set.h5ad`):

    $ scaae train training_set.h5ad --vp validation_set.h5ad --es adjusted_rand_index \
    > -o semi_supervised_model

The model is saved to a directory named `semi_supervised_model`.

Evaluate the model on another data set (`test_set.h5ad`):

    $ scaae evaluate test_set.h5ad -m semi_supervised_model -o evaluation-semi_supervised

## Usage

scAAE provides a command-line interface (CLI), which is divided into two main subcommands: `train` and `evaluate`. The latter subcommand can also be accomplished with two other separate subcommands: `encode` and `analyse`.

### Supported data sets

All subcommands follow the same basic structure:

    $ scaae {train,evaluate,encode,analyse} $DATA_SET_PATH

`$DATA_SET_PATH` is the path to input data set. scAAE supports CSV, TSV, [H5AD][] and [Loom][] files among others.[^supported-files] If multiple layers are available in the data set such as for H5AD files, a specific layer can be chosen using the `-l` argument:

    $ scaae train data_set.h5ad -l logcounts

[H5AD]: https://anndata.readthedocs.io/
[Loom]: http://linnarssonlab.org/loompy/

[^supported-files]: scAAE uses [Scanpy's `read` function][sacnpy-read] to load the data set with default arguments. So any data set that can be read without setting other arguments is supported.

[sacnpy-read]: https://scanpy.readthedocs.io/en/stable/generated/scanpy.read.html

### Training

Use the subcommand `train` to train scAAE on a data set:

    $ scaae train $DATA_SET_PATH

By default the model is not saved, but an output directory can be specified with the `-o` argument:

    $ scaae train data_set.h5ad -o output

scAAE will be trained on the data set for 100 epochs. This can be changed using `-E` argument. If a validation data set is provided using `--vp` argument,[^validation-layer] early stopping can also be used to stop training the model early to prevent overfitting. This is done by designating a loss with the `--es` argument:

    $ scaae train training_set.h5ad --vp validation_set.h5ad --es autoencoder_loss

[^validation-layer]: The validation set will use the same layer as used for the training set.

Available losses are `autoencoder_loss`, `discriminator_loss`, and `generator_loss`. Clustering metrics can also be used for early stopping (see [Clustering](#clustering)).

To change the default loss functions of scAAE and other aspects of the model configuration, a JSON file can be provided with the `-m` argument:

    $ scaae train training_set.h5ad -m model_config.json

For details, see [Model configuration](#model-configuration).

### Evaluation

Use the subcommand `evaluate` to evaluate a scAAE model on a data set:

    $ scaae evaluate $DATA_SET_PATH -m $MODEL_DIRECTORY -o $OUTPUT_DIRECTORY

The `$MODEL_DIRECTORY` should be a path to a directory with a previously saved model.

`$OUTPUT_DIRECTORY` is the directory where the analyses are saved. scAAE will save the evaluation as well as the latent representation by default. The latent representation can also be plotted with the `-d` argument using one or more dimensionality-reduction methods:

    $ scaae evaluate test_set.h5ad -m model -o output -d pca umap

Available dimensionality-reduction methods: `pca` (PCA, default), `tsne` (*t*-SNE), and `umap` (UMAP).

### Clustering

scAAE supports clustering the latent representation using both the Louvain (`louvain`) and the Leiden (`leiden`) methods. This is done using the `-c` argument:

    $ scaae evaluate test_set.h5ad -m model -o output -c louvain

Parameters for these methods can also be specified: the resolution (`--cr`), the neighbourhood size (`--cn`), and the number of principal components used (`--cp`). Multiple values can be provided for all of these arguments (including the `-c` argument), and all combinations will be used.

For example, the following prompt will perform clustering using the Louvain and the Leiden methods both with resolutions of 0.8 and 1.2:

    $ scaae evaluate test_set.h5ad -m model -o output -c louvain leiden --cr 0.8 1.2

To evaluate the clustering(s), several clustering metrics can be used:

* Unsupervised clustering metrics:
    * `silhouette_coefficient`: silhouette coefficient.
    * `calinski_harabasz_index`: Calinski--Harabasz index.
    * `davies_bouldin_index`: Davies--Bouldin index.
    * `cluster_count`: number of clusters.
* Supervised clustering metrics:
    * `adjusted_rand_index`: adjusted Rand index.
    * `adjusted_mutual_information`: adjusted mutual information.
    * `cluster_accuracy`: how accurate the clusters match the ground truth. Clusters are matched to ground-truth classes using the [Hungarian algorithm][].
    * `cluster_purity`: how pure the clusters are.
    * `f1_score`: F1 score.
    * `cluster_count_excess`: difference between the number of clusters and the number of ground-truth classes.

[Hungarian algorithm]: https://en.wikipedia.org/wiki/Hungarian_algorithm

For evaluation, the silhouette coefficient and the adjusted Rand index are evaluated by default for any clustering. One or more can also be evaluated with the `--cm` argument:

    $ scaae evaluate test_set.h5ad -o output -c louvain \
    > --cm calinski_harabasz_index adjusted_mutual_information

#### Early stopping using clustering metrics

During training, clustering will only be performed, if a clustering metric is used for early stopping. Only one clustering metric can used:

    $ scaae train training_set.h5ad --vp validation_set.h5ad --es silhouette_coefficient

The `train` subcommand supports the same clustering arguments as above:

    $ scaae train training_set.h5ad --vp validation_set.h5ad --es silhouette_coefficient \
    > -c louvain leiden --cr 0.8 1.2

If no clustering options are specified, the validation set will be clustered three times using the Louvain method with resolutions of 0.4, 0.8, and 1.2.

When performing multiple clusterings during training, the computed clustering metric values have to be aggregated to a single value. By default, the optimum for the clustering metric is used, but other statistics such as the mean (`mean`) or the median (`median`) can also be specified with the `--ca` argument:

    $ scaae train training_set.h5ad --vp validation_set.h5ad --es silhouette_coefficient \
    > -c leiden --cn 0.4 0.8 1.2 --ca median

If supervised metric is chosen, scAAE will try to find a cell-type annotation to use as ground truth. If it cannot, the clustering evaluation will fail. A specific cell annotation can be set as the ground truth using the `--gta` argument:

    $ scaae train training_set.h5ad --vp validation_set.h5ad --es adjusted_rand_index \
    > --gta cluster_name

For unsupervised clustering metrics, the validation data set itself or the chosen layer will be used as reference. Another layer can used with the `--gtr` argument. In addition to the layers in the data set, the latent representation (`latent`) is also an option:

    $ scaae train training_set.h5ad --vp validation_set.h5ad --es silhouette_coefficient \
    > --gtr latent

### Model configuration

scAAE models can be configured by passing a JSON file including a single object with string--value pairs representing each configuration option.

A model configuration file could look like this:

```json
{
    "autoencoder_distribution": "negative_binomial",
    "gaussian_discriminator_sample_noise_scale": 0.05,
    "gaussian_discriminator_sample_noise_decay": 0.99,
    "intermediate_activation": {
        "class_name": "LeakyReLU",
        "config": {"alpha": 0.3}
    },
    "intermediate_dropout_rate": null
}
```

Possible options are listed in the following sections.

##### Options for the autoencoder and discriminator architectures

The number of layers and the number of units in each layer can be set with the following configuration options:

* `"latent_size"` (positive integer, CLI: `-L`): The number of dimensions of the latent representation (default: 32).
* `"intermediate_sizes"` (array of positive integers, CLI: `-I`): The size(s) of the intermediate (hidden) layer(s) of the encoder (default: `[256, 128]`). The default would make two layers with 256 units in first one and 128 units in the second one. The intermediate layers of the decoder reverses the order: 128 units in the first one and 256 units in the second one.
* `"discriminator_intermediate_sizes"` (array of positive integers or null, CLI: `-D`): The size(s) of intermediate layer(s) of the discriminator (default: `null`, which duplicates the intermediate architecture for the decoder).

These options can also be set directly from the command line by using the CLI arguments listed above. These will override any corresponding option in the model configuration file.

##### Options for loss functions and probability distributions

A loss function or a probability distribution (but not both) can be set for each of the networks (autoencoder, discriminator, and generator) of scAAE with the following configuration options:

* `"autoencoder_loss"` (string, object, or null): loss function for the autoencoder (default: `"mean_squared_error"`).
* `"autoencoder_distribution"` (string or null): probability distribution for the autoencoder (default: `null`).
* `"discriminator_loss"` (string, object, or null): loss function for the discriminator (default: `"binary_crossentropy"`).
* `"discriminator_distribution"` (string or null): probability distribution for the discriminator (default: `null`).
* `"generator_loss"` (string, object, or null): loss function for the generator (default: `null`, which duplicates the loss function for the discriminator).
* `"generator_distribution"` (string or null): probability distribution for the generator (default: `null`, which duplicates the probability distribution for the discriminator).

Loss functions can be any [loss function in TensorFlow][tf.losses.get]. Changing the loss function for a network might also require changing the activation function for that network with the following configuration options:

* `"autoencoder_activation"` (string, object, or null): activation function for the autoencoder (default: `null`).
* `"discriminator_activation"` (string, object, or null): activation function for the discriminator (default: `"sigmoid"` if `discriminator_loss` equals `"binary_crossentropy"`, else null).

Activity functions can be any [activity function in TensorFlow][tf.keras.activations.get].

[tf.losses.get]: https://www.tensorflow.org/api_docs/python/tf/keras/losses/get
[tf.keras.activations.get]: https://www.tensorflow.org/api_docs/python/tf/keras/activations/get

As for probability distributions, the following are supported:

* `"poisson"`: Poisson distribution, use only with raw transcript count values.
* `"zero_inflated_poisson"`: Zero-inflated Poisson distribution, use only with raw transcript count values.
* `"negative_binomial"`: Negative binomial, use only with raw transcript count values.
* `"zero_inflated_negative_binomial"`: Zero-inflated negative binomial, use only with raw transcript count values.
* `"normal"`: Normal (Gaussian) distribution, which is equivalent to using mean squared error as a loss function.
* `"bernoulli"`: Bernoulli distribution, which is equivalent to using binary cross-entropy as a loss function.

##### Discriminator noise options

Noise can be added to the discriminator during training to prevent it overfitting. The following configuration options are used if not null:

* `"discriminator_label_flipping_rate"` (real number between 0 and 1 or null): Share of  labels that are flipped (or switched) to add noise to the discriminator during training (default: `null`).
* `"discriminator_label_smoothing_scale"` (positive real number or null): Maximum for uniform noise used to smooth labels (default: `null`).
* `"gaussian_discriminator_sample_noise_scale"` (positive real number or null): Scale (standard deviation) for Gaussian noise added to samples (default: `null`).
* `"gaussian_discriminator_sample_noise_decay"` (real number between 0 and 1 or null): Decay rate of the scale (standard deviation) for Gaussian noise added to samples (default: `null`).
* `"gaussian_discriminator_label_noise_scale"` (positive real number or null): Scale (standard deviation) for Gaussian noise added to labels (default: `null`).

Samples refer to samples drawn from either the desired latent probability distribution or the probability distribution generated by the encoder. Labels refer to whether a sample is from the former or the latter.

##### Options for intermediate layers

The following configuration options for the intermediate layers can be set:

* `"intermediate_activation"` (string, object, or null): activation function for the intermediate layers (default: `"leaky_relu"`).
* `"intermediate_normalisation"` (string or null): normalisation of the intermediate layers (default: `"batch"`). either batch normalisation (`"batch"`), layer normalisation (`"layer"`), or no normalisation (`null`).
* `"intermediate_dropout_rate"` (real number between 0 and 1 or null): rate of dropout regularisation (default: `0.1`).

## Advanced usage

The command-line interface includes several more arguments. Some are explained below, and the rest can be explored using the `-h` argument:

    $ scaae [train|evaluate|encode|analyse] -h

### Separate encoding and analysis

Evaluation of a model can also be performed in two steps: encoding and analysis.

To only encode and save the latent representation, use the subcommand `encode`:

    $ scaae encode $DATA_SET_PATH -m $MODEL_DIRECTORY -o $OUTPUT_DIRECTORY

The latent representation can later be analysed using the subcommand `analyse`:

    $ scaae analyse $DATA_SET_PATH --lrp $LATENT_REPRESENTION_PATH

`$LATENT_REPRESENTION_PATH` is the path to the latent representation. Other  representations of the data (for example, from other methods) can also be used, but they are assumed to be a latent representation. If cell annotations for the latent representation exists in separate CSV/TSV file, they can loaded using the `--lap` argument:

    $ scaae analyse $DATA_SET_PATH --lrp $LATENT_REPRESENTION_PATH \
    > --lap $LATENT_ANNOTATIONS_PATH

### Plotting and ground-truth cell annotations

When plotting the latent representation during training, evaluation, or analysis, a plot will be created for each numeric or categorical[^categorical-annotation] cell annotation. To change which cell annotations are used, use either of the following arguments:

* `--pamp`: space-separated list of regular expressions to match cell annotations used for plotting.
* `--paip`: space-separated list of regular expressions to match cell annotations ignored for plotting.

[^categorical-annotation]: Annotations are assumed to be categorical if they contain strings that do not have the same value for all cells or a different value for each cell. If the annotation name is "category", "clusters", "class", "group", or plurals thereof, they are also assumed to be categorical.

Similarly, when evaluating the supervised clustering metrics, each of the categorical cell annotations will be used as ground truth. To change which cell annotations are used, use either of the following arguments:

* `--gtamp`: space-separated list of regular expressions to match cell annotations used as ground truth.
* `--gtaip`: space-separated list of regular expressions to match cell annotations to not use as ground truth.

### Advanced training

The batch size is by default 64, but can be changed using the `-B` argument.

#### Early stopping

When and for how long early stopping is performed can be set using the following arguments:

* `--esp`: early-stopping patience, which is for how many epochs to continue training, if the validation metric does not improve (default: ´25´).
* `--esid`: initial early-stopping delay, which is for how many epochs to train initially before employing early stopping (default: `None`). If `None`, scAAE will use `10` for data sets with 10000 cells or fewer, and otherwise `1`.

#### Optimisation

How each of the networks (autoencoder, discriminator, and generator) is optimised can be customised using the following arguments:

* `--optimiser`: optimisation method used for each network (default: `adam`). Optimisation method can be any [named optimisation method in TensorFlow][tf.keras.optimizers].
* `--autoencoder-learning-rate`: learning rate for the autoencoder (default: `1e-4`).
* `--discriminator-learning-rate`: learning rate for the discriminator (default: `1e-5`).
* `--generator-learning-rate`: learning rate for the generator (default: `1e-5`).
* `--learning-decay-rate`: learning decay rate for each network (default: `1e-6`).

[tf.keras.optimizers]: https://www.tensorflow.org/api_docs/python/tf/keras/optimizers

Alternatively, an optimisation configuration can be provided as a JSON file using the `--oc` argument. The JSON file must contain a single object with one to three string--value pairs. Each string must be one of `"autoencoder_optimiser"`, `"discriminator_optimiser"`, or `"generator_optimiser"` and the value must be an [optimisation method in TensorFlow][tf.keras.optimizers.get] for the corresponding network.

[tf.keras.optimizers.get]: https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/get

An optimisation configuration file could look like this:

```json
{
    "autoencoder_optimser": "adamax",
    "discriminator_optimiser": {
        "class_name": "Adam",
        "config": {
            "amsgrad": true
        }
    },
    "generator_optimiser": {
        "class_name": "Adam",
        "config": {
            "amsgrad": true
        }
    }
}
```
