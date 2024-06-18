from black import enable_unstable_feature_callback
from funcnodes import Shelf, NodeDecorator
from exposedfunctionality import controlled_wrapper
from typing import Literal, Optional, Union, Callable
import numpy as np
from sklearn.base import BaseEstimator
from enum import Enum
from sklearn.decomposition import (
    DictionaryLearning,
    FactorAnalysis,
    FastICA,
    IncrementalPCA,
    KernelPCA,
    LatentDirichletAllocation,
    MiniBatchDictionaryLearning,
    MiniBatchSparsePCA,
    NMF,
    MiniBatchNMF,
    PCA,
    SparsePCA,
    SparseCoder,
    TruncatedSVD,
    randomized_svd,
)


class FitAlgorithm(Enum):
    lars = "lars"
    cd = "cd"

    @classmethod
    def default(cls):
        return cls.lars.value


class TransformAlgorithm(Enum):
    lasso_lars = "lasso_lars"
    lasso_cd = "lasso_cd"
    lars = "lars"
    omp = "omp"
    threshold = "threshold"

    @classmethod
    def default(cls):
        return cls.omp.value


@NodeDecorator(
    node_id="sklearn.decomposition.DictionaryLearning",
    name="DictionaryLearning",
)
@controlled_wrapper(DictionaryLearning, wrapper_attribute="__fnwrapped__")
def _dictionary_learning(
    n_components: Optional[int] = None,
    alpha: float = 1.0,
    max_iter: int = 1000,
    tol: float = 1e-8,
    fit_algorithm: FitAlgorithm = "lars",
    transform_algorithm: TransformAlgorithm = "omp",
    transform_n_nonzero_coefs: Optional[int] = None,
    transform_alpha: Optional[float] = None,
    n_jobs: Optional[int] = None,
    code_init: Optional[np.ndarray] = None,
    dict_init: Optional[np.ndarray] = None,
    callback: Optional[Callable] = None,
    verbose: bool = False,
    split_sign: bool = False,
    random_state: Optional[Union[int, np.random.RandomState]] = None,
    positive_code: bool = False,
    positive_dict: bool = False,
    transform_max_iter: int = 1000,
) -> Callable[[], BaseEstimator]:
    def create_dictionary_learning():
        return DictionaryLearning(
            n_components=n_components,
            alpha=alpha,
            max_iter=max_iter,
            tol=tol,
            fit_algorithm=fit_algorithm,
            transform_algorithm=transform_algorithm,
            transform_n_nonzero_coefs=transform_n_nonzero_coefs,
            transform_alpha=transform_alpha,
            n_jobs=n_jobs,
            code_init=code_init,
            dict_init=dict_init,
            callback=callback,
            verbose=verbose,
            split_sign=split_sign,
            random_state=random_state,
            positive_code=positive_code,
            positive_dict=positive_dict,
            transform_max_iter=transform_max_iter,
        )

    return create_dictionary_learning


class SVDMethod(Enum):
    lapack = "lapack"
    randomized = "randomized"

    @classmethod
    def default(cls):
        return cls.randomized.value


class Rotation(Enum):
    varimax = "varimax"
    quartimax = "quartimax"
    NONE = None

    @classmethod
    def default(cls):
        return cls.NONE.value


@NodeDecorator(
    node_id="sklearn.decomposition.FactorAnalysis",
    name="FactorAnalysis",
)
@controlled_wrapper(FactorAnalysis, wrapper_attribute="__fnwrapped__")
def _factor_analysis(
    n_components: Optional[int] = None,
    tol: float = 1e-2,
    copy: bool = True,
    max_iter: int = 1000,
    noise_variance_init: Optional[int] = None,
    svd_method: SVDMethod = "randomized",
    iterated_power: int = 3,
    rotation: Rotation = None,
    random_state: Optional[Union[int, np.random.RandomState]] = 0,
) -> Callable[[], BaseEstimator]:
    if noise_variance_init == "np":
        noise_variance_init = None

    def create_factor_analysis():
        return FactorAnalysis(
            n_components=n_components,
            copy=copy,
            max_iter=max_iter,
            tol=tol,
            noise_variance_init=noise_variance_init,
            svd_method=svd_method,
            iterated_power=iterated_power,
            rotation=rotation,
            random_state=random_state,
        )

    return create_factor_analysis


class Algorithm(Enum):
    parallel = "parallel"
    deflation = "deflation"

    @classmethod
    def default(cls):
        return cls.parallel.value


class Fun(Enum):
    logcosh = "logcosh"
    exp = "exp"
    cube = "cube"

    @classmethod
    def default(cls):
        return cls.logcosh.value


class WhitenSolver(Enum):
    eigh = "eigh"
    svd = "svd"

    @classmethod
    def default(cls):
        return cls.svd.value


@NodeDecorator(
    node_id="sklearn.decomposition.FastICA",
    name="FastICA",
)
@controlled_wrapper(FastICA, wrapper_attribute="__fnwrapped__")
def _fast_ica(
    n_components: Optional[int] = None,
    algorithm: Algorithm = "parallel",
    fun: Optional[Union[Fun, Callable]] = "logcosh",
    fun_args: Optional[dict] = None,
    max_iter: int = 200,
    tol: float = 1e-4,
    w_init: Optional[np.ndarray] = None,
    whiten_solver: WhitenSolver = "svd",
    random_state: Optional[Union[int, np.random.RandomState]] = None,
) -> Callable[[], BaseEstimator]:
    def create_fast_ica():
        return FastICA(
            n_components=n_components,
            algorithm=algorithm,
            max_iter=max_iter,
            tol=tol,
            fun=fun,
            fun_args=fun_args,
            w_init=w_init,
            whiten_solver=whiten_solver,
            random_state=random_state,
        )

    return create_fast_ica


@NodeDecorator(
    node_id="sklearn.decomposition.IncrementalPCA",
    name="IncrementalPCA",
)
@controlled_wrapper(IncrementalPCA, wrapper_attribute="__fnwrapped__")
def _incrementa_lpca(
    n_components: Optional[int] = None,
    whiten: bool = False,
    copy: bool = True,
    batch_size: Optional[int] = None,
) -> Callable[[], BaseEstimator]:
    def create_incrementa_lpca():
        return IncrementalPCA(
            n_components=n_components,
            whiten=whiten,
            batch_size=batch_size,
            copy=copy,
        )

    return create_incrementa_lpca


class Kernel(Enum):
    linear = "linear"
    poly = "poly"
    rbf = "rbf"
    sigmoid = "sigmoid"
    cosine = "cosine"
    precomputed = "precomputed"

    @classmethod
    def default(cls):
        return cls.linear.value


class EigenSolvers(Enum):
    auto = "auto"
    dense = "dense"
    arpack = "arpack"
    randomized = "randomized"

    @classmethod
    def default(cls):
        return cls.auto.value


@NodeDecorator(
    node_id="sklearn.decomposition.KernelPCA",
    name="KernelPCA",
)
@controlled_wrapper(KernelPCA, wrapper_attribute="__fnwrapped__")
def _kernel_lpca(
    n_components: Optional[int] = None,
    kernel: Optional[Union[Kernel, Callable]] = "linear",
    gamma: Optional[float] = None,
    degree: int = 3,
    coef0: float = 1,
    kernel_params: Optional[dict] = None,
    alpha: float = 1.0,
    fit_inverse_transform: bool = False,
    eigen_solver: EigenSolvers = "auto",
    tol: float = 0.0,
    max_iter: Optional[int] = None,
    iterated_power: Optional[Union[int, Literal["auto"]]] = "auto",
    remove_zero_eig: bool = False,
    random_state: Optional[Union[int, np.random.RandomState]] = None,
    copy_X: bool = True,
    n_jobs: Optional[int] = None,
) -> Callable[[], BaseEstimator]:
    def create_kernel_lpca():
        return KernelPCA(
            n_components=n_components,
            kernel=kernel,
            max_iter=max_iter,
            tol=tol,
            degree=degree,
            gamma=gamma,
            coef0=coef0,
            kernel_params=kernel_params,
            alpha=alpha,
            fit_inverse_transform=fit_inverse_transform,
            eigen_solver=eigen_solver,
            iterated_power=iterated_power,
            remove_zero_eig=remove_zero_eig,
            copy_X=copy_X,
            n_jobs=n_jobs,
            random_state=random_state,
        )

    return create_kernel_lpca


class LearningMethod(Enum):
    batch = "batch"
    online = "online"

    @classmethod
    def default(cls):
        return cls.batch.value


@NodeDecorator(
    node_id="sklearn.decomposition.LatentDirichletAllocation",
    name="LatentDirichletAllocation",
)
@controlled_wrapper(LatentDirichletAllocation, wrapper_attribute="__fnwrapped__")
def _latent_dirichlet_allocation(
    n_components: int = 10,
    doc_topic_prior: Optional[float] = None,
    topic_word_prior: Optional[float] = None,
    learning_method: LearningMethod = "batch",
    learning_decay: float = 0.7,
    learning_offset: float = 10.0,
    max_iter: int = 10,
    batch_size: int = 128,
    evaluate_every: int = -1,
    total_samples: int = 1e6,
    perp_tol: float = 1e-1,
    mean_change_tol: float = 1e-3,
    max_doc_update_iter: int = 100,
    n_jobs: Optional[int] = None,
    verbose: int = 0,
    random_state: Optional[Union[int, np.random.RandomState]] = None,
) -> Callable[[], BaseEstimator]:
    if doc_topic_prior == "1 / n_components":
        doc_topic_prior = None
    if topic_word_prior == "1 / n_components":
        topic_word_prior = None

    def create_latent_dirichlet_allocation():
        return LatentDirichletAllocation(
            n_components=n_components,
            doc_topic_prior=doc_topic_prior,
            max_iter=max_iter,
            topic_word_prior=topic_word_prior,
            learning_method=learning_method,
            learning_decay=learning_decay,
            learning_offset=learning_offset,
            batch_size=batch_size,
            evaluate_every=evaluate_every,
            total_samples=total_samples,
            perp_tol=perp_tol,
            mean_change_tol=mean_change_tol,
            max_doc_update_iter=max_doc_update_iter,
            verbose=verbose,
            n_jobs=n_jobs,
            random_state=random_state,
        )

    return create_latent_dirichlet_allocation


@NodeDecorator(
    node_id="sklearn.decomposition.MiniBatchDictionaryLearning",
    name="MiniBatchDictionaryLearning",
)
@controlled_wrapper(MiniBatchDictionaryLearning, wrapper_attribute="__fnwrapped__")
def _mini_batch_dictionary_learning(
    n_components: Optional[int] = None,
    alpha: float = 1.0,
    max_iter: int = 1000,
    fit_algorithm: FitAlgorithm = "lars",
    n_jobs: Optional[int] = None,
    batch_size: int = 256,
    shuffle: bool = True,
    dict_init: Optional[np.ndarray] = None,
    transform_algorithm: TransformAlgorithm = "omp",
    transform_n_nonzero_coefs: Optional[int] = None,
    transform_alpha: Optional[float] = None,
    verbose: Union[bool, int] = False,
    split_sign: bool = False,
    random_state: Optional[Union[int, np.random.RandomState]] = None,
    positive_code: bool = False,
    positive_dict: bool = False,
    transform_max_iter: int = 1000,
    callback: Optional[Callable] = None,
    tol: float = 1e-3,
    max_no_improvement: int = 10,
) -> Callable[[], BaseEstimator]:
    def create_mini_batch_dictionary_learning():
        return MiniBatchDictionaryLearning(
            n_components=n_components,
            max_iter=max_iter,
            alpha=alpha,
            fit_algorithm=fit_algorithm,
            shuffle=shuffle,
            batch_size=batch_size,
            transform_algorithm=transform_algorithm,
            dict_init=dict_init,
            transform_n_nonzero_coefs=transform_n_nonzero_coefs,
            transform_alpha=transform_alpha,
            split_sign=split_sign,
            verbose=verbose,
            n_jobs=n_jobs,
            random_state=random_state,
            positive_code=positive_code,
            positive_dict=positive_dict,
            transform_max_iter=transform_max_iter,
            callback=callback,
            tol=tol,
            max_no_improvement=max_no_improvement,
        )

    return create_mini_batch_dictionary_learning


@NodeDecorator(
    node_id="sklearn.decomposition.MiniBatchSparsePCA",
    name="MiniBatchSparsePCA",
)
@controlled_wrapper(MiniBatchSparsePCA, wrapper_attribute="__fnwrapped__")
def _mini_batch_sparse_pca(
    n_components: Optional[int] = None,
    alpha: float = 1.0,
    ridge_alpha: float = 0.01,
    max_iter: int = 1000,
    callback: Optional[Callable] = None,
    batch_size: int = 3,
    verbose: Union[bool, int] = False,
    shuffle: bool = True,
    n_jobs: Optional[int] = None,
    method: FitAlgorithm = "lars",
    random_state: Optional[Union[int, np.random.RandomState]] = None,
    tol: float = 1e-3,
    max_no_improvement: int = 10,
) -> Callable[[], BaseEstimator]:
    def create_mini_batch_sparse_pca():
        return MiniBatchSparsePCA(
            n_components=n_components,
            max_iter=max_iter,
            alpha=alpha,
            shuffle=shuffle,
            batch_size=batch_size,
            verbose=verbose,
            n_jobs=n_jobs,
            random_state=random_state,
            method=method,
            callback=callback,
            tol=tol,
            max_no_improvement=max_no_improvement,
        )

    return create_mini_batch_sparse_pca


class Init(Enum):
    random = "random"
    nndsvd = "nndsvd"
    nndsvda = "nndsvda"
    nndsvdar = "nndsvdar"
    custom = "custom"
    NONE = None

    @classmethod
    def default(cls):
        return cls.NONE.value


class Solver(Enum):
    cd = "cd"
    mu = "mu"

    @classmethod
    def default(cls):
        return cls.cd.value


class BetaLoss(Enum):
    frobenius = "frobenius"
    kullback_leibler = "kullback-leibler"
    itakura_saito = "itakura-saito"

    @classmethod
    def default(cls):
        return cls.frobenius.value


@NodeDecorator(
    node_id="sklearn.decomposition.NMF",
    name="NMF",
)
@controlled_wrapper(NMF, wrapper_attribute="__fnwrapped__")
def _nmf(
    n_components: Optional[Union[int, Literal["auto"]]] = None,
    init: Init = "frobenius",
    solver: Solver = Solver.default(),
    beta_loss: Union[BetaLoss, float] = BetaLoss.default(),
    tol: float = 1e-4,
    max_iter: int = 200,
    random_state: Optional[Union[int, np.random.RandomState]] = None,
    alpha_W: float = 0.0,
    alpha_H: float = 0.0,
    l1_ratio: float = 0.0,
    verbose: int = 0,
    shuffle: bool = False,
) -> Callable[[], BaseEstimator]:
    def create_nmf():
        return NMF(
            n_components=n_components,
            max_iter=max_iter,
            init=init,
            shuffle=shuffle,
            solver=solver,
            verbose=verbose,
            beta_loss=beta_loss,
            random_state=random_state,
            alpha_W=alpha_W,
            alpha_H=alpha_H,
            tol=tol,
            l1_ratio=l1_ratio,
        )

    return create_nmf


@NodeDecorator(
    node_id="sklearn.decomposition.MiniBatchNMF",
    name="MiniBatchNMF",
)
@controlled_wrapper(MiniBatchNMF, wrapper_attribute="__fnwrapped__")
def _mini_batch_nmf(
    n_components: Optional[Union[int, Literal["auto"]]] = None,
    init: Init = "frobenius",
    batch_size: int = 1024,
    beta_loss: Union[BetaLoss, float] = BetaLoss.default(),
    tol: float = 1e-4,
    max_no_improvement: int = 10,
    max_iter: int = 200,
    alpha_W: float = 0.0,
    alpha_H: float = 0.0,
    l1_ratio: float = 0.0,
    forget_factor: float = 0.7,
    fresh_restarts: bool = False,
    fresh_restarts_max_iter: int = 30,
    transform_max_iter: Optional[int] = None,
    random_state: Optional[Union[int, np.random.RandomState]] = None,
    verbose: bool = False,
) -> Callable[[], BaseEstimator]:
    if transform_max_iter == "max_iter":
        transform_max_iter = None
    def create_mini_batch_nmf():
        return MiniBatchNMF(
            n_components=n_components,
            max_iter=max_iter,
            init=init,
            batch_size=batch_size,
            max_no_improvement=max_no_improvement,
            verbose=verbose,
            beta_loss=beta_loss,
            random_state=random_state,
            alpha_W=alpha_W,
            alpha_H=alpha_H,
            tol=tol,
            l1_ratio=l1_ratio,
            forget_factor=forget_factor,
            fresh_restarts=fresh_restarts,
            fresh_restarts_max_iter=fresh_restarts_max_iter,
            transform_max_iter=transform_max_iter,
        )

    return create_mini_batch_nmf

class SVDSolver(Enum):
    auto = "auto"
    full = "full"
    randomized = "randomized"
    arpack = "arpack"
    
    @classmethod
    def default(cls):
        return cls.auto.value

class PowerIterationNormalizer(Enum):
    auto = "auto"
    QR = "QR"
    LU = "LU"
    NONE = None
    
    @classmethod
    def default(cls):
        return cls.auto.value
@NodeDecorator(
    node_id="sklearn.decomposition.PCA",
    name="PCA",
)
@controlled_wrapper(PCA, wrapper_attribute="__fnwrapped__")
def _pca(
    n_components: Optional[str] = None,
    copy: bool = True,
    whiten: bool = False,
    svd_solver: SVDSolver = "auto",
    tol: float = 0.0,
    iterated_power: Union[int, Literal["auto"]] = "auto",
    n_oversamples:int=10,
    power_iteration_normalizer: PowerIterationNormalizer="auto",
    random_state: Optional[Union[int, np.random.RandomState]] = None,
) -> Callable[[], BaseEstimator]:
    if n_components is not None:
        if isinstance(int(n_components), int):
            n_components = int(n_components)
        elif isinstance(n_components, float):
            n_components = float(n_components)
        elif n_components == "mle":
            n_components = "mle"
        else:
            raise ValueError(f"Invalid value for n_components: {n_components}. n_components : int, float or 'mle'")

    def create_pca():
        return PCA(
            n_components=n_components,
            copy=copy,
            whiten=whiten,
            svd_solver=svd_solver,
            iterated_power=iterated_power,
            n_oversamples=n_oversamples,
            power_iteration_normalizer=power_iteration_normalizer,
            random_state=random_state,
            tol=tol,
        )

    return create_pca

@NodeDecorator(
    node_id="sklearn.decomposition.SparsePCA",
    name="SparsePCA",
)
@controlled_wrapper(SparsePCA, wrapper_attribute="__fnwrapped__")
def _sparse_pca(
    n_components: Optional[int] = None,
    alpha: float = 1.0,
    ridge_alpha: float = 0.01,
    max_iter: int = 1000,
    tol: float = 1e-8,
    method: FitAlgorithm = "lars",
    n_jobs: Optional[int] = None,
    U_init: Optional[np.ndarray] = None,
    V_init: Optional[np.ndarray] = None,
    verbose: Union[bool, int] = False,
    random_state: Optional[Union[int, np.random.RandomState]] = None,
) -> Callable[[], BaseEstimator]:

    def create_sparse_pca():
        return SparsePCA(
            n_components=n_components,
            alpha=alpha,
            ridge_alpha=ridge_alpha,
            max_iter=max_iter,
            method=method,
            n_jobs=n_jobs,
            U_init=U_init,
            V_init=V_init,
            verbose=verbose,
            random_state=random_state,
            tol=tol,
        )

    return create_sparse_pca

@NodeDecorator(
    node_id="sklearn.decomposition.SparseCoder",
    name="SparseCoder",
)
@controlled_wrapper(SparseCoder, wrapper_attribute="__fnwrapped__")
def _sparse_coder(
    dictionary:np.ndarray,
    transform_algorithm: TransformAlgorithm = TransformAlgorithm.lasso_lars,
    transform_n_nonzero_coefs: Optional[int] = None,
    transform_alpha:  Optional[float] = None,
    split_sign: bool = False,
    n_jobs: Optional[int] = None,
    positive_code: bool = False,
    transform_max_iter: int= 1000,
) -> Callable[[], BaseEstimator]:

    def create_sparse_coder():
        return SparseCoder(
            dictionary=dictionary,
            transform_algorithm=transform_algorithm,
            transform_n_nonzero_coefs=transform_n_nonzero_coefs,
            transform_alpha=transform_alpha,
            split_sign=split_sign,
            n_jobs=n_jobs,
            positive_code=positive_code,
            transform_max_iter=transform_max_iter,
        )

    return create_sparse_coder

class TSVDAlgorithm(Enum):
    arpack = "arpack"
    randomized = "randomized"
    
    @classmethod
    def default(cls):
        return cls.randomized.value
@NodeDecorator(
    node_id="sklearn.decomposition.TruncatedSVD",
    name="TruncatedSVD",
)
@controlled_wrapper(TruncatedSVD, wrapper_attribute="__fnwrapped__")
def _truncated_svd(
    n_components: int = 2,
    algorithm: TSVDAlgorithm = "randomized",
    n_iter: int = 5,
    n_oversamples:int=10,
    power_iteration_normalizer: PowerIterationNormalizer="auto",
    random_state: Optional[Union[int, np.random.RandomState]] = None,
    tol: float = 0.0,
) -> Callable[[], BaseEstimator]:

    def create_truncated_svd():
        return TruncatedSVD(
            n_components=n_components,
            algorithm=algorithm,
            n_iter=n_iter,
            n_oversamples=n_oversamples,
            power_iteration_normalizer=power_iteration_normalizer,
            random_state=random_state,
            tol=tol,
        )

    return create_truncated_svd

DECOMPOSITION_NODE_SHELFE = Shelf(
    nodes=[
        _dictionary_learning,
        _factor_analysis,
        _fast_ica,
        _incrementa_lpca,
        _kernel_lpca,
        _latent_dirichlet_allocation,
        _mini_batch_dictionary_learning,
        _mini_batch_sparse_pca,
        _nmf,
        _mini_batch_nmf,
        _pca,
        _sparse_pca,
        _sparse_coder,
        _truncated_svd
        
    ],
    subshelves=[],
    name="Matrix Decomposition",
    description="The sklearn.decomposition module includes matrix decomposition algorithms, including among others PCA, NMF or ICA. Most of the algorithms of this module can be regarded as dimensionality reduction techniques.",
)
