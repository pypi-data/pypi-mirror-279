from funcnodes import Shelf, NodeDecorator
from typing import Optional, Callable, Union
import numpy as np
from sklearn.base import BaseEstimator
import inspect


@NodeDecorator(
    node_id="sklearn.fit",
    name="fit",
)
def _fit(
    model: Union[BaseEstimator, Callable[[], BaseEstimator]],
    X: np.ndarray,
    y: Optional[np.ndarray] = None,
) -> BaseEstimator:
    if not isinstance(model, BaseEstimator):
        model = model()

    # # Get the signature of the fit method
    # fit_signature = inspect.signature(model.fit)
    # parameter_names = list(fit_signature.parameters.keys())
    # print(parameter_names)

    # if len(parameter_names) == 1:
    #     return model.fit(X)
    # else:
    #     print(y)
    #     return model.fit(X, y)
    if y is not None:
        return model.fit(X, y)
    else:
        return model.fit(X)


# @NodeDecorator(
#     node_id="sklearn.fit_transform",
#     name="fit_transform",
# )
# def _fit_transform(
#     model: Union[BaseEstimator, Callable[[], BaseEstimator]],
#     X: np.ndarray,
#     y: Optional[np.ndarray] = None,
# ) -> np.ndarray:

#     def apply_fit_transform():
#         if not isinstance(model.fit_transform(X, y), np.ndarray):
#             return model.fit_transform(X, y).toarray()
#         else:
#             return model.fit_transform(X, y)

#     return apply_fit_transform


@NodeDecorator(
    node_id="sklearn.inverse_transform",
    name="inverse_transform",
)
def _inverse_transform(
    model: Union[BaseEstimator, Callable[[], BaseEstimator]],
    X: np.ndarray,
) -> np.ndarray:
    if not isinstance(model, BaseEstimator):
        model = model()
    if not isinstance(model.inverse_transform(X), np.ndarray):
        return model.inverse_transform(X).toarray()
    else:
        return model.inverse_transform(X)


@NodeDecorator(
    node_id="sklearn.transform",
    name="transform",
)
def _transform(
    model: Union[BaseEstimator, Callable[[], BaseEstimator]],
    X: np.ndarray,
) -> np.ndarray:
    if not isinstance(model.transform(X), np.ndarray):
        return model.transform(X).toarray()
    else:
        return model.transform(X)


@NodeDecorator(
    node_id="sklearn.predict",
    name="predict",
)
def _predict(
    model: Union[BaseEstimator, Callable[[], BaseEstimator]],
    X: np.ndarray,
) -> np.ndarray:
    if not isinstance(model.predict(X), np.ndarray):
        return model.predict(X).toarray()
    else:
        return model.predict(X)


FIT_NODE_SHELFE = Shelf(
    nodes=[_fit, _inverse_transform, _transform, _predict],
    subshelves=[],
    name="Fit",
    description="Methods for fitting, transforming, and more.",
)
