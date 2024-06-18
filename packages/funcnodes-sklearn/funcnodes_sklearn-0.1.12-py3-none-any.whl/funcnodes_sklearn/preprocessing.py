from funcnodes import Shelf, NodeDecorator
from exposedfunctionality import controlled_wrapper
from typing import Tuple, Literal, Optional, Union, Callable
from enum import Enum
import numpy as np
from numpy.random import RandomState
from sklearn.base import BaseEstimator
from sklearn.preprocessing import (
    Binarizer,
    FunctionTransformer,
    KBinsDiscretizer,
    KernelCenterer,
    LabelBinarizer,
    LabelEncoder,
    MaxAbsScaler,
    MinMaxScaler,
    MultiLabelBinarizer,
    Normalizer,
    OneHotEncoder,
    OrdinalEncoder,
    PolynomialFeatures,
    PowerTransformer,
    QuantileTransformer,
    RobustScaler,
    SplineTransformer,
    StandardScaler,
    TargetEncoder,
)


# @NodeDecorator(
#     node_id="sklearn.preprocessing.Binarizer",
#     name="Binarizer",
# )
# @controlled_wrapper(Binarizer, wrapper_attribute="__fnwrapped__")
# def _binarizer(
#     threshold: float = 0.0,
# ) -> BaseEstimator:
#     def create_binarizer():
#         return Binarizer(threshold=threshold)

#     return create_binarizer


# @NodeDecorator(
#     node_id="sklearn.preprocessing.FunctionTransformer",
#     name="FunctionTransformer",
# )
# @controlled_wrapper(FunctionTransformer, wrapper_attribute="__fnwrapped__")
# def _function_transformer(
#     func: Optional[Callable] = None,
#     inverse_func: Optional[Callable] = None,
#     validate: bool = True,
#     accept_sparse: bool = False,
#     check_inverse: bool = True,
#     feature_names_out: Optional[Union[Callable, Literal["one-to-one"]]] = None,
#     kw_args: Optional[dict] = None,
#     inv_kw_args: Optional[dict] = None
    
# ) -> BaseEstimator:
#     def create_function_transformer():
#         return FunctionTransformer(
#             func=func,
#             inverse_func=inverse_func,
#             validate=validate,
#             accept_sparse=accept_sparse,
#             check_inverse=check_inverse,
#             feature_names_out=feature_names_out,
#             kw_args=kw_args,
#             inv_kw_args=inv_kw_args
#         )

#     return create_function_transformer


# class Encode(Enum):
#     onehot = "onehot"
#     ordinal = "ordinal"
#     onehot_dense = "onehot-dense"
    
#     @classmethod
#     def default(cls):
#         cls.onehot.value
        
        
# class Strategy(Enum):
#     uniform = "uniform"
#     quantile = "quantile"
#     kmeans = "kmeans"
    
#     @classmethod
#     def default(cls):
#         cls.quantile.value
        
# class Dtype(Enum):
#     float32 = np.float32
#     float64 = np.float64
#     NONE = None
    
#     @classmethod
#     def default(cls):
#         cls.NONE.value
# @NodeDecorator(
#     node_id="sklearn.preprocessing.KBinsDiscretizer",
#     name="KBinsDiscretizer",
# )
# @controlled_wrapper(KBinsDiscretizer, wrapper_attribute="__fnwrapped__")
# def _kbins_discretizer(
#     n_bins: int = 5,
#     encode: Encode = Encode.default(),
#     strategy: Strategy = Strategy.default(),
#     dtype: Dtype = np.float64,
#     subsample: Optional[int] = None,
#     random_state: Optional[Union[int, RandomState]] = None,
# ) -> BaseEstimator:
#     def create_kbins_discretizer():
#         return KBinsDiscretizer(
#             n_bins=n_bins,
#             encode=encode,
#             strategy=strategy,
#             dtype=dtype,
#             subsample=subsample,
#             random_state=random_state,
#         )

#     return create_kbins_discretizer    
    
# @NodeDecorator(
#     node_id="sklearn.preprocessing.KernelCenterer",
#     name="KernelCenterer",
# )
# @controlled_wrapper(KernelCenterer, wrapper_attribute="__fnwrapped__")
# def _kbins_centerer(
#     K_fit_rows_: np.ndarray,
#     K_fit_all_: float,
#     n_features_in_: int,
#     feature_names_in_: np.ndarray,
# ) -> BaseEstimator:
#     def create_kbins_centerer():
#         return KernelCenterer(
#             K_fit_rows=K_fit_rows_,
#             K_fit_all=K_fit_all_,
#             n_features_in=n_features_in_,
#             feature_names_in=feature_names_in_,
#         )

#     return create_kbins_centerer    



# PREPROCESSING_NODE_SHELFE = Shelf(
#     nodes=[
#         _binarizer,
#         _function_transformer,
#         _kbins_discretizer,
#         _kbins_centerer,
        
#     ],
#     subshelves=[],
#     name="Preprocessing",
#     description="Methods for scaling, centering, normalization, binarization, and more.",
# )


@NodeDecorator(
    node_id="sklearn.preprocessing.Binarizer",
    name="Binarizer",
)
@controlled_wrapper(Binarizer, wrapper_attribute="__fnwrapped__")
def _binarizer(
    threshold: float = 0.0,
) -> BaseEstimator:
    def create_binarizer():
        return Binarizer(threshold=threshold)

    return create_binarizer


@NodeDecorator(
    node_id="sklearn.preprocessing.FunctionTransformer",
    name="FunctionTransformer",
)
@controlled_wrapper(FunctionTransformer, wrapper_attribute="__fnwrapped__")
def _function_transformer(
    func: Optional[Callable] = None,
    inverse_func: Optional[Callable] = None,
    validate: bool = True,
    accept_sparse: bool = False,
    check_inverse: bool = True,
    feature_names_out: Optional[Union[Callable, Literal["one-to-one"]]] = None,
    kw_args: Optional[dict] = None,
    inv_kw_args: Optional[dict] = None
) -> BaseEstimator:
    def create_function_transformer():
        return FunctionTransformer(
            func=func,
            inverse_func=inverse_func,
            validate=validate,
            accept_sparse=accept_sparse,
            check_inverse=check_inverse,
            feature_names_out=feature_names_out,
            kw_args=kw_args,
            inv_kw_args=inv_kw_args
        )

    return create_function_transformer


class Encode(Enum):
    onehot = "onehot"
    ordinal = "ordinal"
    onehot_dense = "onehot-dense"
    
    @classmethod
    def default(cls):
        cls.onehot.value
        
        
class Strategy(Enum):
    uniform = "uniform"
    quantile = "quantile"
    kmeans = "kmeans"
    
    @classmethod
    def default(cls):
        cls.quantile.value
        
class Dtype(Enum):
    float32 = np.float32
    float64 = np.float64
    NONE = None
    
    @classmethod
    def default(cls):
        cls.NONE.value
        
        
@NodeDecorator(
    node_id="sklearn.preprocessing.KBinsDiscretizer",
    name="KBinsDiscretizer",
)
@controlled_wrapper(KBinsDiscretizer, wrapper_attribute="__fnwrapped__")
def _kbins_discretizer(
    n_bins: int = 5,
    encode: Encode = Encode.default(),
    strategy: Strategy = Strategy.default(),
    dtype: Dtype = np.float64,
    subsample: Optional[int] = None,
    random_state: Optional[Union[int, RandomState]] = None,
) -> BaseEstimator:
    def create_kbins_discretizer():
        return KBinsDiscretizer(
            n_bins=n_bins,
            encode=encode,
            strategy=strategy,
            dtype=dtype,
            subsample=subsample,
            random_state=random_state,
        )

    return create_kbins_discretizer    
    
    
@NodeDecorator(
    node_id="sklearn.preprocessing.KernelCenterer",
    name="KernelCenterer",
)
@controlled_wrapper(KernelCenterer, wrapper_attribute="__fnwrapped__")
def _kbins_centerer(
) -> BaseEstimator:
    def create_kbins_centerer():
        return KernelCenterer(
        )

    return create_kbins_centerer    
    

@NodeDecorator(
    node_id="sklearn.preprocessing.LabelBinarizer",
    name="LabelBinarizer",
)
@controlled_wrapper(LabelBinarizer, wrapper_attribute="__fnwrapped__")
def _label_binarizer(
    neg_label: int = 0,
    pos_label: int = 1,
    sparse_output: bool = False
) -> BaseEstimator:
    def create_label_binarizer():
        return LabelBinarizer(
            neg_label=neg_label,
            pos_label=pos_label,
            sparse_output=sparse_output,
        )

    return create_label_binarizer
    
    
@NodeDecorator(
    node_id="sklearn.preprocessing.LabelEncoder",
    name="LabelEncoder",
)
@controlled_wrapper(LabelEncoder, wrapper_attribute="__fnwrapped__")
def _label_encoder() -> BaseEstimator:
    def create_label_encoder():
        return LabelEncoder()

    return create_label_encoder
    

@NodeDecorator(
    node_id="sklearn.preprocessing.MaxAbsScaler",
    name="MaxAbsScaler",
)
@controlled_wrapper(MaxAbsScaler, wrapper_attribute="__fnwrapped__")
def _max_abs_scaler() -> BaseEstimator:
    def create_max_abs_scaler():
        return MaxAbsScaler()

    return create_max_abs_scaler
    

@NodeDecorator(
    node_id="sklearn.preprocessing.MinMaxScaler",
    name="MinMaxScaler",
)
@controlled_wrapper(MinMaxScaler, wrapper_attribute="__fnwrapped__")
def _min_max_scaler(
    min: float = 0.0,
    max: float = 1.0,
    clip: bool = False
) -> BaseEstimator:
    feature_range = (min, max)
    def create_min_max_scaler():
        return MinMaxScaler(
            feature_range=feature_range,
            clip=clip,
        )

    return create_min_max_scaler
    
@NodeDecorator(
    node_id="sklearn.preprocessing.MultiLabelBinarizer",
    name="MultiLabelBinarizer",
)
@controlled_wrapper(MultiLabelBinarizer, wrapper_attribute="__fnwrapped__")
def _multi_label_binarizer(
    classes: Optional[np.ndarray] = None,
    sparse_output: bool = False,
) -> BaseEstimator:
    def creat_multi_label_binarizer():
        return MultiLabelBinarizer(
            classes=classes,
            sparse_output=sparse_output,
        )

    return creat_multi_label_binarizer

class Norm(Enum):
    l1 = "l1"
    l2 = "l2"
    max = "max"
    
    @classmethod
    def default(cls):
        cls.l2.value
@NodeDecorator(
    node_id="sklearn.preprocessing.Normalizer",
    name="Normalizer",
)
@controlled_wrapper(Normalizer, wrapper_attribute="__fnwrapped__")
def _normalizer(
    norm: Norm = Norm.default()
) -> BaseEstimator:
    def create_normalizer():
        return Normalizer(
            norm=norm,
        )

    return create_normalizer
    
    
class HandleUnknown1(Enum):
    error = "error"
    ignore = "ignore"
    infrequent_if_exist = "infrequent_if_exist"
    
    @classmethod
    def default(cls):
        cls.ignore.value

@NodeDecorator(
    node_id="sklearn.preprocessing.OneHotEncoder",
    name="OneHotEncoder",
)
@controlled_wrapper(OneHotEncoder, wrapper_attribute="__fnwrapped__")
def _one_hot_encoder(
    categories: Union[list,Literal["auto"]] = "auto",
    drop: Optional[Union[Literal["first", "if_binary"], np.ndarray]] = None,
    sparse_output: bool = True,
    dtype: Dtype = np.float64,
    handle_unknown: HandleUnknown1 = "ignore",
    min_frequency: Optional[float] = None,
    max_categories: Optional[int] = None,
    feature_name_combiner: Optional[Union[Callable, Literal["concat"]]] = "concat",
) -> BaseEstimator:
    def create_one_hot_encoder():
        return OneHotEncoder(
            categories=categories,
            drop=drop,
            sparse_output=sparse_output,
            dtype=dtype,
            handle_unknown=handle_unknown,
            min_frequency=min_frequency,
            max_categories=max_categories,
            feature_name_combiner=feature_name_combiner,
        )

    return create_one_hot_encoder
    
class HandleUnknown2(Enum):
    error = "error"
    use_encoded_value = "use_encoded_value"
    
    @classmethod
    def default(cls):
        cls.error.value
@NodeDecorator(
    node_id="sklearn.preprocessing.OrdinalEncoder",
    name="OrdinalEncoder",
)
@controlled_wrapper(OrdinalEncoder, wrapper_attribute="__fnwrapped__")
def _ordinal_encoder(
    categories: Optional[Union[list, Literal["auto"]]] = "auto",
    dtype: Dtype = np.float64,
    handle_unknown: HandleUnknown2 = HandleUnknown2.default(),
    unknown_value: Optional[int] = None,
    encoded_missing_value: Optional[int] = None,
    min_frequency: Optional[float] = None,
    max_categories: Optional[int] = None,
    
) -> BaseEstimator:
    def create_ordinal_encoder():
        return OrdinalEncoder(
            categories=categories,
            dtype=dtype,
            handle_unknown=handle_unknown,
            unknown_value=unknown_value,
            encoded_missing_value=encoded_missing_value,
            min_frequency=min_frequency,
            max_categories=max_categories,
        )

    return create_ordinal_encoder
    
class Order(Enum):
    C = "C"
    F = "F"
    
    @classmethod
    def default(cls):
        cls.C.value

@NodeDecorator(
    node_id="sklearn.preprocessing.PolynomialFeatures",
    name="PolynomialFeatures",
)
@controlled_wrapper(PolynomialFeatures, wrapper_attribute="__fnwrapped__")
def _polynomial_features(
    degree: int = 2,
    interaction_only: bool = False,
    include_bias: bool = True,
    order: Order = Order.default(),
) -> BaseEstimator:
    def create_polynomial_features():
        return PolynomialFeatures(
            degree=degree,
            interaction_only=interaction_only,
            include_bias=include_bias,
            order=order,
        )

    return create_polynomial_features
    
class PowerMethod(Enum):
    yeo_johnson = "yeo-johnson"
    box_cox = "box-cox"
    
    @classmethod
    def default(cls):
        cls.yeo_johnson.value
@NodeDecorator(
    node_id="sklearn.preprocessing.PowerTransformer",
    name="PowerTransformer",
)
@controlled_wrapper(PowerTransformer, wrapper_attribute="__fnwrapped__")
def _power_transformer(
    method: PowerMethod = PowerMethod.default(),
    standardize: bool = True,
) -> BaseEstimator:
    def create_power_transformer():
        return PowerTransformer(
            method=method,
            standardize=standardize,
        )

    return create_power_transformer
    
class OutputDistribution(Enum):
    uniform = "uniform"
    normal = "normal"
    
    @classmethod
    def default(cls):
        cls.uniform.value
@NodeDecorator(
    node_id="sklearn.preprocessing.QuantileTransformer",
    name="QuantileTransformer",
)
@controlled_wrapper(QuantileTransformer, wrapper_attribute="__fnwrapped__")
def _quantile_transformer(
    n_quantiles: int = 1000,
    output_distribution: OutputDistribution = OutputDistribution.default(),
    ignore_implicit_zeros: bool = False,
    subsample: int = 1e5,
    random_state: Optional[Union[int, RandomState]] = None,
) -> BaseEstimator:
    def create_quantile_transformer():
        return QuantileTransformer(
            n_quantiles=n_quantiles,
            output_distribution=output_distribution,
            ignore_implicit_zeros=ignore_implicit_zeros,
            subsample=subsample,
            random_state=random_state,
        )

    return create_quantile_transformer
    

@NodeDecorator(
    node_id="sklearn.preprocessing.RobustScaler",
    name="RobustScaler",
)
@controlled_wrapper(RobustScaler, wrapper_attribute="__fnwrapped__")
def _robust_scaler(
    with_centering: bool = True,
    with_scaling: bool = True,
    q_min: float = 25.0,
    q_max: float = 75.0,
    unit_variance: bool = False
) -> BaseEstimator:
    quantile_range = (q_min, q_max)
    def create_robust_scaler():
        return RobustScaler(
            with_centering=with_centering,
            with_scaling=with_scaling,
            quantile_range=quantile_range,
            unit_variance=unit_variance,
        )

    return create_robust_scaler
    
    
class Extrapolation(Enum):
    error = "error"
    constant = "constant"
    linear = "linear"
    contineu = "continue"
    periodic = "periodic"
    
    @classmethod
    def default(cls):
        cls.constant.value

@NodeDecorator(
    node_id="sklearn.preprocessing.SplineTransformer",
    name="SplineTransformer",
)
@controlled_wrapper(SplineTransformer, wrapper_attribute="__fnwrapped__")
def _spline_transformer(
    n_knots: int = 5,
    degree: int = 3,
    knots: Optional[Union[Literal["quantile", "uniform"], np.ndarray]] = "uniform",
    extrapolation: Extrapolation = Extrapolation.default(),
    include_bias: bool = True,
    order: Order = Order.default(),
    sparse_output: bool = False
    
) -> BaseEstimator:
    def create_spline_transformer():
        return SplineTransformer(
            n_knots=n_knots,
            degree=degree,
            knots=knots,
            extrapolation=extrapolation,
            include_bias=include_bias,
            order=order,
            sparse_output=sparse_output,
        )

    return create_spline_transformer

@NodeDecorator(
    node_id="sklearn.preprocessing.StandardScaler",
    name="StandardScaler",
)
@controlled_wrapper(StandardScaler, wrapper_attribute="__fnwrapped__")
def _standard_scaler(
    with_mean: bool = True,
    with_std: bool = True
) -> BaseEstimator:
    def create_standard_scaler():
        return StandardScaler(
            with_mean=with_mean,
            with_std=with_std,
        )

    return create_standard_scaler
    
    
class TargetType(Enum):
    auto = "auto"
    binary = "binary"
    multi_class = "multiclass"
    continuous = "continuous"
    
    @classmethod
    def default(cls):
        cls.auto.value

@NodeDecorator(
    node_id="sklearn.preprocessing.TargetEncoder",
    name="TargetEncoder",
)
@controlled_wrapper(TargetEncoder, wrapper_attribute="__fnwrapped__")
def _target_encoder(
    category: Union[list, Literal["auto"]] = "auto",
    target_type: TargetType = TargetType.default(),
) -> BaseEstimator:
    def create_target_encoder():
        return TargetEncoder(
            category=category,
            target_type=target_type,
        )

    return create_target_encoder


PREPROCESSING_NODE_SHELFE = Shelf(
    nodes=[
        _binarizer,
        _function_transformer,
        _kbins_discretizer,
        _kbins_centerer,
        _label_binarizer,
        _label_encoder,
        _max_abs_scaler,
        _min_max_scaler,
        _multi_label_binarizer,
        _normalizer,
        _one_hot_encoder,
        _ordinal_encoder,
        _polynomial_features,
        _power_transformer,
        _quantile_transformer,
        _robust_scaler,
        _standard_scaler,
        _target_encoder
    ],
    subshelves=[],
    name="Preprocessing",
    description="Methods for scaling, centering, normalization, binarization, and more.",
)
