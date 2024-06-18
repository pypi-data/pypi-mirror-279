from funcnodes import Shelf, NodeDecorator
from exposedfunctionality import controlled_wrapper
from typing import Optional, Callable
import numpy as np
from sklearn.base import BaseEstimator
from enum import Enum
from sklearn.discriminant_analysis import (
    LinearDiscriminantAnalysis,
    QuadraticDiscriminantAnalysis,
)


class Solver(Enum):
    svd = "svd"
    lsqr = "lsqr"
    eigen = "eigen"

    @classmethod
    def default(cls):
        return cls.svd.value



@NodeDecorator(
    node_id="sklearn.discriminant_analysis.LinearDiscriminantAnalysis",
    name="LinearDiscriminantAnalysis",
)
@controlled_wrapper(LinearDiscriminantAnalysis, wrapper_attribute="__fnwrapped__")
def _lda(
    solver: Solver = "svd",
    shrinkage: Optional[str] = None,
    priors: Optional[np.ndarray] = None,
    n_components: Optional[int] = None,
    store_covariance: bool = False,
    tol: float = 1e-4,
    covariance_estimator: Optional[BaseEstimator] = None,
) -> Callable[[], BaseEstimator]:
    if shrinkage is not None:
        if isinstance(shrinkage, float):
            shrinkage = float(shrinkage)
        elif shrinkage == "auto":
            shrinkage = "auto"
        else:
            raise ValueError(
                f"Invalid value for shrinkage: {shrinkage}. shrinkage : int, float or 'auto'"
            )

    def create_lda():
        return LinearDiscriminantAnalysis(
            n_components=n_components,
            solver=solver,
            priors=priors,
            tol=tol,
            store_covariance=store_covariance,
            covariance_estimator=covariance_estimator,
        )

    return create_lda


@NodeDecorator(
    node_id="sklearn.discriminant_analysis.QuadraticDiscriminantAnalysis",
    name="QuadraticDiscriminantAnalysis",
)
@controlled_wrapper(QuadraticDiscriminantAnalysis, wrapper_attribute="__fnwrapped__")
def _qda(
    priors: Optional[np.ndarray] = None,
    reg_param: float = 0.0,
    store_covariance: bool = False,
    tol: float = 1e-4,
) -> Callable[[], BaseEstimator]:
    def create_qda():
        return QuadraticDiscriminantAnalysis(
            reg_param=reg_param,
            priors=priors,
            tol=tol,
            store_covariance=store_covariance,
        )

    return create_qda


DISCRIMINANTANALYSIS_NODE_SHELFE = Shelf(
    nodes=[_lda, _qda],
    subshelves=[],
    name="Discriminant Analysis",
    description="Linear Discriminant Analysis (LinearDiscriminantAnalysis) and Quadratic Discriminant Analysis (QuadraticDiscriminantAnalysis) are two classic classifiers, with, as their names suggest, a linear and a quadratic decision surface, respectively.",
)
