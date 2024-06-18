from funcnodes import Shelf, NodeDecorator
from typing import Optional, Callable, Union
import numpy as np
from enum import Enum
from matplotlib.figure import Figure
from sklearn.metrics import (
    # model selection interface
    check_scoring,
    get_scorer,
    get_scorer_names,
    make_scorer,
    # classification metrics
    accuracy_score,
    auc,
    average_precision_score,
    balanced_accuracy_score,
    brier_score_loss,
    class_likelihood_ratios,
    classification_report,
    cohen_kappa_score,
    confusion_matrix,
    # d2_log_loss_score,
    dcg_score,
    det_curve,
    f1_score,
    fbeta_score,
    hamming_loss,
    hinge_loss,
    jaccard_score,
    log_loss,
    matthews_corrcoef,
    multilabel_confusion_matrix,
    ndcg_score,
    precision_recall_curve,
    precision_recall_fscore_support,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
    top_k_accuracy_score,
    zero_one_loss,
    # regresiion metrics
    d2_absolute_error_score,
    d2_pinball_score,
    d2_tweedie_score,
    explained_variance_score,
    max_error,
    mean_absolute_error,
    mean_absolute_percentage_error,
    mean_gamma_deviance,
    mean_pinball_loss,
    mean_poisson_deviance,
    mean_squared_error,
    mean_squared_log_error,
    mean_tweedie_deviance,
    median_absolute_error,
    r2_score,
    # root_mean_squared_error,
    # root_mean_squared_log_error,
    # multilabel ranking metrics
    coverage_error,
    label_ranking_average_precision_score,
    label_ranking_loss,
    # clustering metrics
    adjusted_mutual_info_score,
    adjusted_rand_score,
    calinski_harabasz_score,
    # cluster.contingency_matrix,
    # cluster.pair_confusion_matrix,
    completeness_score,
    davies_bouldin_score,
    fowlkes_mallows_score,
    homogeneity_completeness_v_measure,
    homogeneity_score,
    mutual_info_score,
    normalized_mutual_info_score,
    rand_score,
    silhouette_samples,
    silhouette_score,
    # y_measure_score,
    # biclustering metrics
    consensus_score,
    DistanceMetric,
    # TODO:
    # plotting
    ConfusionMatrixDisplay,
    DetCurveDisplay,
    PrecisionRecallDisplay,
    PredictionErrorDisplay,
    RocCurveDisplay,
)


class Normalize(Enum):
    true = "true"
    pred = "pred"
    all = "all"
    NONE = None

    @classmethod
    def default(cls):
        return cls.NONE.value


@NodeDecorator(
    node_id="sklearn.metrics.confusion_matrix",
    name="confusion_matrix",
)
def _confusion_matrix(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    labels: Optional[np.ndarray] = None,
    sample_weight: Optional[np.ndarray] = None,
    normalize: Normalize = Normalize.default(),
) -> np.ndarray:
    return confusion_matrix(
        y_true=y_true,
        y_pred=y_pred,
        labels=labels,
        sample_weight=sample_weight,
        normalize=normalize,
    )

@NodeDecorator(
    node_id="sklearn.metrics.ConfusionMatrixDisplay",
    name="ConfusionMatrixDisplay",
)
def _confusion_matrix_display(
    confusion_matrix: np.ndarray,
    display_labels: Optional[np.ndarray] = None,
) -> Figure:
    return ConfusionMatrixDisplay(
        confusion_matrix=confusion_matrix,
        display_labels=display_labels,
    ).plot()
    
    
CLASSIFICATION_NODE_SHELFE = Shelf(
    nodes=[_confusion_matrix],
    subshelves=[],
    name="Classification metrics",
    description="The sklearn.metrics module implements several loss, score, and utility functions to measure classification performance. Some metrics might require probability estimates of the positive class, confidence values, or binary decisions values. Most implementations allow each sample to provide a weighted contribution to the overall score, through the sample_weight parameter.",
)

PLOTTING_NODE_SHELFE = Shelf(
    nodes=[_confusion_matrix_display],
    subshelves=[],
    name="Plotting",
    description="User guide. See the sklearn_visualizations section for further details.",
)

METRICS_NODE_SHELFE = Shelf(
    nodes=[],
    subshelves=[CLASSIFICATION_NODE_SHELFE, PLOTTING_NODE_SHELFE],
    name="Metrics",
    description="Score functions, performance metrics, pairwise metrics and distance computations.",
)
