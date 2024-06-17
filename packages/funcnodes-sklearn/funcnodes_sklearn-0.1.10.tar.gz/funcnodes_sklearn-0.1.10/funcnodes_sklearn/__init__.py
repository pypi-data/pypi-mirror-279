import funcnodes_pandas
import funcnodes_numpy
import funcnodes as fn
from .covariance import COVARIANCE_NODE_SHELFE
from .calibration import CALIBRATION_NODE_SHELFE
from .cluster import CLUSTER_NODE_SHELFE
from .cross_decomposition import CROSS_DECOMPOSITION_NODE_SHELFE
from .datasets import DATASET_NODE_SHELF
from .decomposition import DECOMPOSITION_NODE_SHELFE
from .discriminant_analysis import DISCRIMINANTANALYSIS_NODE_SHELFE
from .metrics import METRICS_NODE_SHELFE
from .preprocessing import PREPROCESSING_NODE_SHELFE
from .fit import FIT_NODE_SHELFE

__version__ = "0.1.10"

NODE_SHELF = fn.Shelf(
    name="sklearn",
    description="scikit-learn for funcnodes",
    nodes=[],
    subshelves=[
        CALIBRATION_NODE_SHELFE,
        CLUSTER_NODE_SHELFE,
        COVARIANCE_NODE_SHELFE,
        CROSS_DECOMPOSITION_NODE_SHELFE,
        DATASET_NODE_SHELF,
        DECOMPOSITION_NODE_SHELFE,
        DISCRIMINANTANALYSIS_NODE_SHELFE,
        METRICS_NODE_SHELFE,
        PREPROCESSING_NODE_SHELFE,
        FIT_NODE_SHELFE
    ],
)
