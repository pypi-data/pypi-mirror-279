import scanpy

SCALERS = {}


def preprocess(data_set, gene_mask_annotation_key=None, normalise=False,
               scaling_method=None):
    if gene_mask_annotation_key:
        data_set = _keep_genes(
            data_set, gene_mask_annotation_key=gene_mask_annotation_key)
    if normalise:
        _normalise(data_set)
    if scaling_method:
        scaler = SCALERS.get(scaling_method)
        if scaler is None:
            available_scalers = ", ".join(list(SCALERS.keys()))
            raise ValueError(
                f"Scaling method `{scaling_method}` not found."
                f"Available methods are: {available_scalers}.")
        scaler(data_set)
    return data_set


def _keep_genes(data_set, gene_mask_annotation_key=None):
    if not isinstance(gene_mask_annotation_key, str):
        raise TypeError(
            "Gene mask annotation name should be a string, "
            f"not \"{type(gene_mask_annotation_key)}\".")
    available_gene_mask_annotation_keys = ", ".join(
        data_set.var.dtypes.index[data_set.var.dtypes == "bool"].to_list())
    if gene_mask_annotation_key not in available_gene_mask_annotation_keys:
        raise ValueError(
            "Gene mask annotation should be a boolean annotation."
            f"Available annotations are: {available_gene_mask_annotation_keys}"
        )
    gene_mask_annotation = data_set.var[gene_mask_annotation_key]
    if all(gene_mask_annotation):
        raise ValueError(
            "Chosen gene mask annotation does not remove any genes.")
    return data_set[:, gene_mask_annotation]


def _normalise(data_set):
    scanpy.pp.normalize_total(data_set)
    data_set.uns["data_interval"] = "unit"


def _register_scaler(name):
    def decorator(function):
        SCALERS[name] = function
        return function
    return decorator


@_register_scaler("standardise")
def _standardise(data_set):
    scanpy.pp.scale(data_set)
    data_set.uns["data_interval"] = "real"


@_register_scaler("min_max_scale")
def _min_max_scale(data_set):
    minimum = data_set.uns.get("minimum")
    if minimum is None:
        minimum = data_set.X.min()
    maximum = data_set.uns.get("maximum")
    if maximum is None:
        maximum = data_set.X.max()

    data_set.X = (data_set.X - minimum) / (maximum - minimum)
    data_set.uns["data_interval"] = "unit"
