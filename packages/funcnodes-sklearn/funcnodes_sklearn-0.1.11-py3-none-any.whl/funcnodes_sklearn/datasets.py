from funcnodes import Shelf, NodeDecorator
from exposedfunctionality import controlled_wrapper
from pandas.core.frame import DataFrame
from pandas import Series
from scipy.sparse import spmatrix
import numpy as np
import os
from enum import Enum

# import warnings
from numpy.random import RandomState
from typing import List, Optional, Union, Tuple
from sklearn.datasets import (
    fetch_20newsgroups,
    fetch_20newsgroups_vectorized,
    fetch_california_housing,
    fetch_covtype,
    fetch_kddcup99,
    fetch_lfw_pairs,
    fetch_lfw_people,
    fetch_olivetti_faces,
    # fetch_openml,
    fetch_rcv1,
    # fetch_species_distributions,
    load_breast_cancer,
    load_diabetes,
    load_digits,
    # load_files,
    load_iris,
    load_linnerud,
    load_sample_image,
    # load_svmlight_file,
    load_wine,
    make_biclusters,
    make_blobs,
    make_checkerboard,
    make_circles,
    make_classification,
    make_friedman1,
    make_friedman2,
    make_friedman3,
    make_gaussian_quantiles,
    make_hastie_10_2,
    make_low_rank_matrix,
    make_moons,
    make_multilabel_classification,
    make_regression,
    make_s_curve,
    make_sparse_coded_signal,
    make_sparse_spd_matrix,
    make_sparse_uncorrelated,
    make_spd_matrix,
    make_swiss_roll,
)


class Subset(Enum):
    train = "train"
    test = "test"
    all = "all"

    @classmethod
    def default(cls):
        return cls.train.value


@NodeDecorator(
    node_id="sklearn.datasets.fetch_20newsgroups",
    name="fetch_20newsgroups",
    outputs=[
        {"name": "data"},
        {"name": "target"},
        {"name": "filenames"},
        {"name": "DESCR"},
        {"name": "target_names"},
    ],
)
def _20newsgroups(
    subset: Subset = "train",
    categories: Optional[List[str]] = None,
    shuffle: bool = True,
    random_state: Optional[Union[int, RandomState]] = None,
    remove_headers: bool = False,
    remove_footers: bool = False,
    remove_quotes: bool = False,
    download_if_missing: bool = True,
) -> Tuple[list, np.ndarray, List[os.PathLike], str, List[str]]:
    """Load the filenames and data from the 20 newsgroups dataset (classification).

    Download it if necessary.

    =================   ==========
    Classes                     20
    Samples total            18846
    Dimensionality               1
    Features                  text
    =================   ==========

    Read more in the :ref:`User Guide <20newsgroups_dataset>`.

    Parameters
    ----------
    data_home : str or path-like, default=None
        Specify a download and cache folder for the datasets. If None,
        all scikit-learn data is stored in '~/scikit_learn_data' subfolders.

    subset : {'train', 'test', 'all'}, default='train'
        Select the dataset to load: 'train' for the training set, 'test'
        for the test set, 'all' for both, with shuffled ordering.

    categories : array-like, dtype=str, default=None
        If None (default), load all the categories.
        If not None, list of category names to load (other categories
        ignored).

    shuffle : bool, default=True
        Whether or not to shuffle the data: might be important for models that
        make the assumption that the samples are independent and identically
        distributed (i.i.d.), such as stochastic gradient descent.

    random_state : int, RandomState instance or None, default=42
        Determines random number generation for dataset shuffling. Pass an int
        for reproducible output across multiple function calls.
        See :term:`Glossary <random_state>`.

    remove : tuple, default=()
        May contain any subset of ('headers', 'footers', 'quotes'). Each of
        these are kinds of text that will be detected and removed from the
        newsgroup posts, preventing classifiers from overfitting on
        metadata.

        'headers' removes newsgroup headers, 'footers' removes blocks at the
        ends of posts that look like signatures, and 'quotes' removes lines
        that appear to be quoting another post.

        'headers' follows an exact standard; the other filters are not always
        correct.

    download_if_missing : bool, default=True
        If False, raise an OSError if the data is not locally available
        instead of trying to download the data from the source site.

    return_X_y : bool, default=False
        If True, returns `(data.data, data.target)` instead of a Bunch
        object.

        .. versionadded:: 0.22

    Returns
    -------
    data : list of shape (n_samples,)
        The data list to learn.
    target: ndarray of shape (n_samples,)
        The target labels.
    filenames: list of shape (n_samples,)
        The path to the location of the data.
    DESCR: str
        The full description of the dataset.
    target_names: list of shape (n_classes,)
        The names of target classes.


    """
    remove_list = []
    if remove_headers:
        remove_list.append("headers")
    if remove_footers:
        remove_list.append("footers")
    if remove_quotes:
        remove_list.append("quotes")

    remove = (
        Tuple(remove_list) if remove_headers or remove_footers or remove_quotes else ()
    )
    out = fetch_20newsgroups(
        subset=subset,
        categories=categories,
        shuffle=shuffle,
        random_state=random_state,
        remove=remove,
        download_if_missing=download_if_missing,
    )
    data = out["data"]
    target = out["target"]
    filenames = out["filenames"]
    DESCR = out["DESCR"]
    target_names = out["target_names"]

    return data, target, filenames, DESCR, target_names


@NodeDecorator(
    node_id="sklearn.datasets.fetch_20newsgroups_vectorized",
    name="fetch_20newsgroups_vectorized",
    outputs=[
        {"name": "data"},
        {"name": "target"},
        {"name": "target_names"},
        {"name": "DESCR"},
    ],
)
def _20newsgroups_vectorized(
    subset: Subset = "train",
    remove_headers: bool = False,
    remove_footers: bool = False,
    remove_quotes: bool = False,
    download_if_missing: bool = True,
    normalize: bool = True,
) -> Tuple[spmatrix, np.ndarray, list, str]:
    """Load and vectorize the 20 newsgroups dataset (classification).

    Download it if necessary.

    This is a convenience function; the transformation is done using the
    default settings for
    :class:`~sklearn.feature_extraction.text.CountVectorizer`. For more
    advanced usage (stopword filtering, n-gram extraction, etc.), combine
    fetch_20newsgroups with a custom
    :class:`~sklearn.feature_extraction.text.CountVectorizer`,
    :class:`~sklearn.feature_extraction.text.HashingVectorizer`,
    :class:`~sklearn.feature_extraction.text.TfidfTransformer` or
    :class:`~sklearn.feature_extraction.text.TfidfVectorizer`.

    The resulting counts are normalized using
    :func:`sklearn.preprocessing.normalize` unless normalize is set to False.

    =================   ==========
    Classes                     20
    Samples total            18846
    Dimensionality          130107
    Features                  real
    =================   ==========

    Read more in the :ref:`User Guide <20newsgroups_dataset>`.

    Parameters
    ----------
    subset : {'train', 'test', 'all'}, default='train'
        Select the dataset to load: 'train' for the training set, 'test'
        for the test set, 'all' for both, with shuffled ordering.

    remove : tuple, default=()
        May contain any subset of ('headers', 'footers', 'quotes'). Each of
        these are kinds of text that will be detected and removed from the
        newsgroup posts, preventing classifiers from overfitting on
        metadata.

        'headers' removes newsgroup headers, 'footers' removes blocks at the
        ends of posts that look like signatures, and 'quotes' removes lines
        that appear to be quoting another post.

    data_home : str or path-like, default=None
        Specify an download and cache folder for the datasets. If None,
        all scikit-learn data is stored in '~/scikit_learn_data' subfolders.

    download_if_missing : bool, default=True
        If False, raise an OSError if the data is not locally available
        instead of trying to download the data from the source site.

    return_X_y : bool, default=False
        If True, returns ``(data.data, data.target)`` instead of a Bunch
        object.

        .. versionadded:: 0.20

    normalize : bool, default=True
        If True, normalizes each document's feature vector to unit norm using
        :func:`sklearn.preprocessing.normalize`.

        .. versionadded:: 0.22



    Returns
    -------

    data: sparse matrix of shape (n_samples, n_features)
        The input data matrix.
    target: ndarray of shape (n_samples,)
        The target labels.
    target_names: list of shape (n_classes,)
        The names of target classes.
    DESCR: str
        The full description of the dataset.




    """
    remove_list = []
    if remove_headers:
        remove_list.append("headers")
    if remove_footers:
        remove_list.append("footers")
    if remove_quotes:
        remove_list.append("quotes")

    remove = (
        Tuple(remove_list) if remove_headers or remove_footers or remove_quotes else ()
    )

    out = fetch_20newsgroups_vectorized(
        subset=subset,
        download_if_missing=download_if_missing,
        remove=remove,
        normalize=normalize,
    )

    data = out["data"]
    target = out["target"]
    DESCR = out["DESCR"]
    target_names = out["target_names"]

    return data, target, target_names, DESCR


@NodeDecorator(
    node_id="sklearn.datasets.fetch_20newsgroups_vectorized_as_frame",
    name="fetch_20newsgroups_vectorized_as_frame",
    outputs=[
        {"name": "data"},
        {"name": "target"},
        {"name": "target_names"},
        {"name": "DESCR"},
    ],
)
def _20newsgroups_vectorized_as_frame(
    subset: Subset = "train",
    remove_headers: bool = False,
    remove_footers: bool = False,
    remove_quotes: bool = False,
    download_if_missing: bool = True,
    normalize: bool = True,
) -> Tuple[DataFrame, Series, list, str]:
    """Load and vectorize the 20 newsgroups dataset (classification).

    Download it if necessary.

    This is a convenience function; the transformation is done using the
    default settings for
    :class:`~sklearn.feature_extraction.text.CountVectorizer`. For more
    advanced usage (stopword filtering, n-gram extraction, etc.), combine
    fetch_20newsgroups with a custom
    :class:`~sklearn.feature_extraction.text.CountVectorizer`,
    :class:`~sklearn.feature_extraction.text.HashingVectorizer`,
    :class:`~sklearn.feature_extraction.text.TfidfTransformer` or
    :class:`~sklearn.feature_extraction.text.TfidfVectorizer`.

    The resulting counts are normalized using
    :func:`sklearn.preprocessing.normalize` unless normalize is set to False.

    =================   ==========
    Classes                     20
    Samples total            18846
    Dimensionality          130107
    Features                  real
    =================   ==========

    Read more in the :ref:`User Guide <20newsgroups_dataset>`.

    Parameters
    ----------
    subset : {'train', 'test', 'all'}, default='train'
        Select the dataset to load: 'train' for the training set, 'test'
        for the test set, 'all' for both, with shuffled ordering.

    remove : tuple, default=()
        May contain any subset of ('headers', 'footers', 'quotes'). Each of
        these are kinds of text that will be detected and removed from the
        newsgroup posts, preventing classifiers from overfitting on
        metadata.

        'headers' removes newsgroup headers, 'footers' removes blocks at the
        ends of posts that look like signatures, and 'quotes' removes lines
        that appear to be quoting another post.

    data_home : str or path-like, default=None
        Specify an download and cache folder for the datasets. If None,
        all scikit-learn data is stored in '~/scikit_learn_data' subfolders.

    download_if_missing : bool, default=True
        If False, raise an OSError if the data is not locally available
        instead of trying to download the data from the source site.

    return_X_y : bool, default=False
        If True, returns ``(data.data, data.target)`` instead of a Bunch
        object.

        .. versionadded:: 0.20

    normalize : bool, default=True
        If True, normalizes each document's feature vector to unit norm using
        :func:`sklearn.preprocessing.normalize`.

        .. versionadded:: 0.22



    Returns
    -------

    data: dataframe of shape (n_samples, n_features)
        The input data matrix. a pandas DataFrame with sparse columns.
    target: series of shape (n_samples,)
        The target labels. a pandas Series.
    target_names: list of shape (n_classes,)
        The names of target classes.
    DESCR: str
        The full description of the dataset.

    """
    remove_list = []
    if remove_headers:
        remove_list.append("headers")
    if remove_footers:
        remove_list.append("footers")
    if remove_quotes:
        remove_list.append("quotes")

    remove = (
        Tuple(remove_list) if remove_headers or remove_footers or remove_quotes else ()
    )

    out = fetch_20newsgroups_vectorized(
        subset=subset,
        download_if_missing=download_if_missing,
        remove=remove,
        normalize=normalize,
        as_frame=True,
    )

    data = out["data"]
    target = out["target"]
    DESCR = out["DESCR"]
    target_names = out["target_names"]

    return data, target, target_names, DESCR


@NodeDecorator(
    node_id="sklearn.datasets.fetch_california_housing",
    name="fetch_california_housing",
    outputs=[
        {"name": "data"},
        {"name": "target"},
        {"name": "DESCR"},
        {"name": "target_names"},
    ],
)
def _california_housing(
    download_if_missing: bool = True,
) -> Tuple[np.ndarray, np.ndarray, List[str], str]:
    """Load the California housing dataset (regression).

    ==============   ==============
    Samples total             20640
    Dimensionality                8
    Features                   real
    Target           real 0.15 - 5.
    ==============   ==============

    Read more in the :ref:`User Guide <california_housing_dataset>`.

    Parameters
    ----------
    data_home : str or path-like, default=None
        Specify another download and cache folder for the datasets. By default
        all scikit-learn data is stored in '~/scikit_learn_data' subfolders.

    download_if_missing : bool, default=True
        If False, raise an OSError if the data is not locally available
        instead of trying to download the data from the source site.

    return_X_y : bool, default=False
        If True, returns ``(data.data, data.target)`` instead of a Bunch
        object.

        .. versionadded:: 0.20

    as_frame : bool, default=False
        If True, the data is a pandas DataFrame including columns with
        appropriate dtypes (numeric, string or categorical). The target is
        a pandas DataFrame or Series depending on the number of target_columns.

        .. versionadded:: 0.23

    Returns
    -------

    data : ndarray, shape (20640, 8)
        Each row corresponding to the 8 feature values in order.
        If ``as_frame`` is True, ``data`` is a pandas object.
    target : numpy array of shape (20640,)
        Each value corresponds to the average
        house value in units of 100,000.
        If ``as_frame`` is True, ``target`` is a pandas object.
    feature_names : list of length 8
        Array of ordered feature names used in the dataset.
    DESCR : str
        Description of the California housing dataset.


    Notes
    -----

    This dataset consists of 20,640 samples and 9 features.

    Examples
    --------
    >>> from sklearn.datasets import fetch_california_housing
    >>> housing = fetch_california_housing()
    >>> print(housing.data.shape, housing.target.shape)
    (20640, 8) (20640,)
    >>> print(housing.feature_names[0:6])
    ['MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 'Population', 'AveOccup']

    """

    out = fetch_california_housing(
        download_if_missing=download_if_missing,
    )
    data = out["data"]
    target = out["target"]
    target_names = out["target_names"]
    DESCR = out["DESCR"]

    return data, target, DESCR, target_names


@NodeDecorator(
    node_id="sklearn.datasets.fetch_california_housing_as_frame",
    name="fetch_california_housing_as_frame",
    outputs=[
        {"name": "data"},
        {"name": "target"},
        {"name": "target_names"},
        {"name": "DESCR"},
    ],
)
def _california_housing_as_frame(
    download_if_missing: bool = True,
) -> Tuple[DataFrame, Series, List[str], str]:
    """Load the California housing dataset (regression).

    ==============   ==============
    Samples total             20640
    Dimensionality                8
    Features                   real
    Target           real 0.15 - 5.
    ==============   ==============

    Read more in the :ref:`User Guide <california_housing_dataset>`.

    Parameters
    ----------
    data_home : str or path-like, default=None
        Specify another download and cache folder for the datasets. By default
        all scikit-learn data is stored in '~/scikit_learn_data' subfolders.

    download_if_missing : bool, default=True
        If False, raise an OSError if the data is not locally available
        instead of trying to download the data from the source site.


    Returns
    -------

    data : dataframe, shape (20640, 8)
        Each row corresponding to the 8 feature values in order.
        If ``as_frame`` is True, ``data`` is a pandas object.
    target : series of shape (20640,)
        Each value corresponds to the average
        house value in units of 100,000.
        If ``as_frame`` is True, ``target`` is a pandas object.
    feature_names : list of length 8
        Array of ordered feature names used in the dataset.
    DESCR : str
        Description of the California housing dataset.


    Notes
    -----

    This dataset consists of 20,640 samples and 9 features.

    Examples
    --------
    >>> from sklearn.datasets import fetch_california_housing
    >>> housing = fetch_california_housing()
    >>> print(housing.data.shape, housing.target.shape)
    (20640, 8) (20640,)
    >>> print(housing.feature_names[0:6])
    ['MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 'Population', 'AveOccup']

    """

    out = fetch_california_housing(
        download_if_missing=download_if_missing, as_frame=True
    )
    data = out["data"]
    target = out["target"]
    target_names = out["target_names"]
    DESCR = out["DESCR"]

    return data, target, target_names, DESCR


@NodeDecorator(
    node_id="sklearn.datasets.fetch_covtype",
    name="fetch_covtype",
    outputs=[
        {"name": "data"},
        {"name": "target"},
        {"name": "DESCR"},
        {"name": "feature_names"},
        {"name": "target_names"},
    ],
)
def _covtype(
    download_if_missing: bool = True,
    random_state: Optional[Union[int, RandomState]] = None,
    shuffle: bool = False,
) -> Tuple[np.ndarray, np.ndarray, str, List[str], List[str]]:
    """Load the covertype dataset (classification).

    Download it if necessary.

    =================   ============
    Classes                        7
    Samples total             581012
    Dimensionality                54
    Features                     int
    =================   ============

    Read more in the :ref:`User Guide <covtype_dataset>`.

    Parameters
    ----------
    data_home : str or path-like, default=None
        Specify another download and cache folder for the datasets. By default
        all scikit-learn data is stored in '~/scikit_learn_data' subfolders.

    download_if_missing : bool, default=True
        If False, raise an OSError if the data is not locally available
        instead of trying to download the data from the source site.

    random_state : int, RandomState instance or None, default=None
        Determines random number generation for dataset shuffling. Pass an int
        for reproducible output across multiple function calls.
        See :term:`Glossary <random_state>`.

    shuffle : bool, default=False
        Whether to shuffle dataset.


    Returns
    -------

    data : ndarray of shape (581012, 54)
        Each row corresponds to the 54 features in the dataset.
    target : ndarray of shape (581012,)
        Each value corresponds to one of
        the 7 forest covertypes with values
        ranging between 1 to 7.

    DESCR : str
        Description of the forest covertype dataset.
    feature_names : list
        The names of the dataset columns.
    target_names: list
        The names of the target columns.



    Examples
    --------
    >>> from sklearn.datasets import fetch_covtype
    >>> cov_type = fetch_covtype()
    >>> cov_type.data.shape
    (581012, 54)
    >>> cov_type.target.shape
    (581012,)
    >>> # Let's check the 4 first feature names
    >>> cov_type.feature_names[:4]
    ['Elevation', 'Aspect', 'Slope', 'Horizontal_Distance_To_Hydrology']
    """

    out = fetch_covtype(
        download_if_missing=download_if_missing,
        random_state=random_state,
        shuffle=shuffle,
    )

    data = out["data"]
    target = out["target"]
    DESCR = out["DESCR"]
    feature_names = out["feature_names"]
    target_names = out["target_names"]

    return data, target, DESCR, feature_names, target_names


@NodeDecorator(
    node_id="sklearn.datasets.fetch_covtype_as_frame",
    name="fetch_covtype_as_frame",
    outputs=[
        {"name": "data"},
        {"name": "target"},
        {"name": "DESCR"},
        {"name": "feature_names"},
        {"name": "target_names"},
    ],
)
def _covtype_as_frame(
    download_if_missing: bool = True,
    random_state: Optional[Union[int, RandomState]] = None,
    shuffle: bool = False,
) -> Tuple[DataFrame, Series, str, List[str], List[str]]:
    """Load the covertype dataset (classification).

    Download it if necessary.

    =================   ============
    Classes                        7
    Samples total             581012
    Dimensionality                54
    Features                     int
    =================   ============

    Read more in the :ref:`User Guide <covtype_dataset>`.

    Parameters
    ----------
    data_home : str or path-like, default=None
        Specify another download and cache folder for the datasets. By default
        all scikit-learn data is stored in '~/scikit_learn_data' subfolders.

    download_if_missing : bool, default=True
        If False, raise an OSError if the data is not locally available
        instead of trying to download the data from the source site.

    random_state : int, RandomState instance or None, default=None
        Determines random number generation for dataset shuffling. Pass an int
        for reproducible output across multiple function calls.
        See :term:`Glossary <random_state>`.

    shuffle : bool, default=False
        Whether to shuffle dataset.


    Returns
    -------

    data : ndarray of shape (581012, 54)
        Each row corresponds to the 54 features in the dataset.
    target : ndarray of shape (581012,)
        Each value corresponds to one of
        the 7 forest covertypes with values
        ranging between 1 to 7.

    DESCR : str
        Description of the forest covertype dataset.
    feature_names : list
        The names of the dataset columns.
    target_names: list
        The names of the target columns.



    Examples
    --------
    >>> from sklearn.datasets import fetch_covtype
    >>> cov_type = fetch_covtype()
    >>> cov_type.data.shape
    (581012, 54)
    >>> cov_type.target.shape
    (581012,)
    >>> # Let's check the 4 first feature names
    >>> cov_type.feature_names[:4]
    ['Elevation', 'Aspect', 'Slope', 'Horizontal_Distance_To_Hydrology']
    """

    out = fetch_covtype(
        download_if_missing=download_if_missing,
        random_state=random_state,
        shuffle=shuffle,
        as_frame=True,
    )

    data = out["data"]
    target = out["target"]
    DESCR = out["DESCR"]
    feature_names = out["feature_names"]
    target_names = out["target_names"]

    return data, target, DESCR, feature_names, target_names


class KDDSubset(Enum):
    sa = "SA"
    sf = "SF"
    http = "http"
    smtp = "smtp"
    NONE = None

    @classmethod
    def default(cls):
        return cls.NONE.value


@NodeDecorator(
    node_id="sklearn.datasets.fetch_kddcup99",
    name="fetch_kddcup99",
    outputs=[
        {"name": "data"},
        {"name": "target"},
        {"name": "DESCR"},
        {"name": "feature_names"},
        {"name": "target_names"},
    ],
)
def _kddcup99(
    subset: Optional[KDDSubset] = None,
    shuffle: bool = False,
    random_state: Optional[Union[int, RandomState]] = None,
    percent10: bool = False,
    download_if_missing: bool = True,
) -> Tuple[np.ndarray, np.ndarray, str, List[str], List[str]]:
    """Load the kddcup99 dataset (classification).

    Download it if necessary.

    =================   ====================================
    Classes                                               23
    Samples total                                    4898431
    Dimensionality                                        41
    Features            discrete (int) or continuous (float)
    =================   ====================================

    Read more in the :ref:`User Guide <kddcup99_dataset>`.

    .. versionadded:: 0.18

    Parameters
    ----------
    subset : {'SA', 'SF', 'http', 'smtp'}, default=None
        To return the corresponding classical subsets of kddcup 99.
        If None, return the entire kddcup 99 dataset.

    data_home : str or path-like, default=None
        Specify another download and cache folder for the datasets. By default
        all scikit-learn data is stored in '~/scikit_learn_data' subfolders.

        .. versionadded:: 0.19

    shuffle : bool, default=False
        Whether to shuffle dataset.

    random_state : int, RandomState instance or None, default=None
        Determines random number generation for dataset shuffling and for
        selection of abnormal samples if `subset='SA'`. Pass an int for
        reproducible output across multiple function calls.
        See :term:`Glossary <random_state>`.

    percent10 : bool, default=True
        Whether to load only 10 percent of the data.

    download_if_missing : bool, default=True
        If False, raise an OSError if the data is not locally available
        instead of trying to download the data from the source site.



    Returns
    -------


    data : ndarrayof shape (494021, 41)
        The data matrix to learn.
    target : ndarray of shape (494021,)
        The regression target for each sample.
    DESCR : str
        The full description of the dataset.
    feature_names : list
        The names of the dataset columns
    target_names: list
        The names of the target columns


    """

    out = fetch_kddcup99(
        download_if_missing=download_if_missing,
        percent10=percent10,
        subset=subset,
        random_state=random_state,
        shuffle=shuffle,
    )

    data = out["data"]
    target = out["target"]
    DESCR = out["DESCR"]
    feature_names = out["feature_names"]
    target_names = out["target_names"]

    return data, target, DESCR, feature_names, target_names


@NodeDecorator(
    node_id="sklearn.datasets.fetch_kddcup99_as_frame",
    name="fetch_kddcup99_as_frame",
    outputs=[
        {"name": "data"},
        {"name": "target"},
        {"name": "DESCR"},
        {"name": "feature_names"},
        {"name": "target_names"},
    ],
)
def _kddcup99_as_frame(
    subset: Optional[KDDSubset] = None,
    shuffle: bool = False,
    random_state: Optional[Union[int, RandomState]] = None,
    percent10: bool = False,
    download_if_missing: bool = True,
) -> Tuple[DataFrame, Series, str, List[str], List[str]]:
    """Load the kddcup99 dataset (classification).

    Download it if necessary.

    =================   ====================================
    Classes                                               23
    Samples total                                    4898431
    Dimensionality                                        41
    Features            discrete (int) or continuous (float)
    =================   ====================================

    Read more in the :ref:`User Guide <kddcup99_dataset>`.

    .. versionadded:: 0.18

    Parameters
    ----------
    subset : {'SA', 'SF', 'http', 'smtp'}, default=None
        To return the corresponding classical subsets of kddcup 99.
        If None, return the entire kddcup 99 dataset.

    data_home : str or path-like, default=None
        Specify another download and cache folder for the datasets. By default
        all scikit-learn data is stored in '~/scikit_learn_data' subfolders.

        .. versionadded:: 0.19

    shuffle : bool, default=False
        Whether to shuffle dataset.

    random_state : int, RandomState instance or None, default=None
        Determines random number generation for dataset shuffling and for
        selection of abnormal samples if `subset='SA'`. Pass an int for
        reproducible output across multiple function calls.
        See :term:`Glossary <random_state>`.

    percent10 : bool, default=True
        Whether to load only 10 percent of the data.

    download_if_missing : bool, default=True
        If False, raise an OSError if the data is not locally available
        instead of trying to download the data from the source site.



    Returns
    -------


    data : dataframe of shape (494021, 41)
        The data matrix to learn. a pandas DataFrame.
    target :  series of shape (494021,)
        The regression target for each sample. A pandas Series.
    DESCR : str
        The full description of the dataset.
    feature_names : list
        The names of the dataset columns
    target_names: list
        The names of the target columns


    """

    out = fetch_kddcup99(
        download_if_missing=download_if_missing,
        percent10=percent10,
        subset=subset,
        random_state=random_state,
        shuffle=shuffle,
        as_frame=True,
    )
    data = out["data"]
    target = out["target"]
    DESCR = out["DESCR"]
    feature_names = out["feature_names"]
    target_names = out["target_names"]

    return data, target, DESCR, feature_names, target_names


class LFWSubet(Enum):
    train = "train"
    test = "test"
    _10fold = "10fold"

    @classmethod
    def default(cls):
        return cls.train.value


@NodeDecorator(
    node_id="sklearn.datasets.fetch_lfw_pairs",
    name="fetch_lfw_pairs",
    outputs=[
        {"name": "data"},
        {"name": "pairs"},
        {"name": "target"},
        {"name": "target_names"},
        {"name": "DESCR"},
    ],
)
def _lfw_pairs(
    subset: LFWSubet = "train",
    funneled: bool = True,
    resize: float = 0.5,
    color: bool = True,
    # slice_1: slice = slice(70, 195), #TODO
    # slice_2: slice = slice(78, 172),
    download_if_missing: bool = True,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, str]:
    """Load the Labeled Faces in the Wild (LFW) pairs dataset (classification).

    Download it if necessary.

    =================   =======================
    Classes                                   2
    Samples total                         13233
    Dimensionality                         5828
    Features            real, between 0 and 255
    =================   =======================

    In the official `README.txt`_ this task is described as the
    "Restricted" task.  As I am not sure as to implement the
    "Unrestricted" variant correctly, I left it as unsupported for now.

      .. _`README.txt`: http://vis-www.cs.umass.edu/lfw/README.txt

    The original images are 250 x 250 pixels, but the default slice and resize
    arguments reduce them to 62 x 47.

    Read more in the :ref:`User Guide <labeled_faces_in_the_wild_dataset>`.

    Parameters
    ----------
    subset : {'train', 'test', '10_folds'}, default='train'
        Select the dataset to load: 'train' for the development training
        set, 'test' for the development test set, and '10_folds' for the
        official evaluation set that is meant to be used with a 10-folds
        cross validation.

    data_home : str or path-like, default=None
        Specify another download and cache folder for the datasets. By
        default all scikit-learn data is stored in '~/scikit_learn_data'
        subfolders.

    funneled : bool, default=True
        Download and use the funneled variant of the dataset.

    resize : float, default=0.5
        Ratio used to resize the each face picture.

    color : bool, default=False
        Keep the 3 RGB channels instead of averaging them to a single
        gray level channel. If color is True the shape of the data has
        one more dimension than the shape with color = False.

    slice_ : tuple of slice, default=(slice(70, 195), slice(78, 172))
        Provide a custom 2D slice (height, width) to extract the
        'interesting' part of the jpeg files and avoid use statistical
        correlation from the background.

    download_if_missing : bool, default=True
        If False, raise an OSError if the data is not locally available
        instead of trying to download the data from the source site.

    Returns
    -------

    data : ndarray of shape (2200, 5828). Shape depends on ``subset``.
        Each row corresponds to 2 ravel'd face images
        of original size 62 x 47 pixels.
        Changing the ``slice_``, ``resize`` or ``subset`` parameters
        will change the shape of the output.
    pairs : ndarray of shape (2200, 2, 62, 47). Shape depends on ``subset``
        Each row has 2 face images corresponding
        to same or different person from the dataset
        containing 5749 people. Changing the ``slice_``,
        ``resize`` or ``subset`` parameters will change the shape of the
        output.
    target : numpy array of shape (2200,). Shape depends on ``subset``.
        Labels associated to each pair of images.
        The two label values being different persons or the same person.
    target_names : numpy array of shape (2,)
        Explains the target values of the target array.
        0 corresponds to "Different person", 1 corresponds to "same person".
    DESCR : str
        Description of the Labeled Faces in the Wild (LFW) dataset.
    """
    slice_ = (slice(70, 195), slice(78, 172))

    out = fetch_lfw_pairs(
        subset=subset,
        funneled=funneled,
        resize=resize,
        color=color,
        slice_=slice_,
        download_if_missing=download_if_missing,
    )
    data = out["data"]
    pairs = out["pairs"]
    target = out["target"]
    target_names = out["target_names"]
    DESCR = out["DESCR"]

    return data, pairs, target, target_names, DESCR


@NodeDecorator(
    node_id="sklearn.datasets.fetch_lfw_people",
    name="fetch_lfw_people",
    outputs=[
        {"name": "data"},
        {"name": "images"},
        {"name": "target"},
        {"name": "target_names"},
        {"name": "DESCR"},
    ],
)
def _lfw_people(
    funneled: bool = True,
    resize: Optional[float] = None,
    min_faces_per_person: int = 0,
    color: bool = True,
    # slice_1: slice = slice(70, 195),
    # slice_2: slice = slice(78, 172), # TODO
    download_if_missing: bool = True,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, str]:
    """Load the Labeled Faces in the Wild (LFW) people dataset \
(classification).

    Download it if necessary.

    =================   =======================
    Classes                                5749
    Samples total                         13233
    Dimensionality                         5828
    Features            real, between 0 and 255
    =================   =======================

    Read more in the :ref:`User Guide <labeled_faces_in_the_wild_dataset>`.

    Parameters
    ----------
    data_home : str or path-like, default=None
        Specify another download and cache folder for the datasets. By default
        all scikit-learn data is stored in '~/scikit_learn_data' subfolders.

    funneled : bool, default=True
        Download and use the funneled variant of the dataset.

    resize : float or None, default=0.5
        Ratio used to resize the each face picture. If `None`, no resizing is
        performed.

    min_faces_per_person : int, default=None # TODO: issue from sklearn comparing int with None in the function
        The extracted dataset will only retain pictures of people that have at
        least `min_faces_per_person` different pictures.

    color : bool, default=False
        Keep the 3 RGB channels instead of averaging them to a single
        gray level channel. If color is True the shape of the data has
        one more dimension than the shape with color = False.

    slice_ : tuple of slice, default=(slice(70, 195), slice(78, 172))
        Provide a custom 2D slice (height, width) to extract the
        'interesting' part of the jpeg files and avoid use statistical
        correlation from the background.

    download_if_missing : bool, default=True
        If False, raise an OSError if the data is not locally available
        instead of trying to download the data from the source site.



    Returns
    -------

    data : numpy array of shape (13233, 2914)
        Each row corresponds to a ravelled face image
        of original size 62 x 47 pixels.
        Changing the ``slice_`` or resize parameters will change the
        shape of the output.
    images : numpy array of shape (13233, 62, 47)
        Each row is a face image corresponding to one of the 5749 people in
        the dataset. Changing the ``slice_``
        or resize parameters will change the shape of the output.
    target : numpy array of shape (13233,)
        Labels associated to each face image.
        Those labels range from 0-5748 and correspond to the person IDs.
    target_names : numpy array of shape (5749,)
        Names of all persons in the dataset.
        Position in array corresponds to the person ID in the target array.
    DESCR : str
        Description of the Labeled Faces in the Wild (LFW) dataset.


    """
    slice_ = (slice(70, 195), slice(78, 172))

    out = fetch_lfw_people(
        funneled=funneled,
        resize=resize,
        color=color,
        slice_=slice_,
        download_if_missing=download_if_missing,
        min_faces_per_person=min_faces_per_person,
    )

    data = out["data"]
    images = out["images"]
    target = out["target"]
    target_names = out["target_names"]
    DESCR = out["DESCR"]

    return data, images, target, target_names, DESCR


@NodeDecorator(
    node_id="sklearn.datasets.fetch_olivetti_faces",
    name="fetch_olivetti_faces",
    outputs=[
        {"name": "data"},
        {"name": "images"},
        {"name": "target"},
        {"name": "DESCR"},
    ],
)
def _olivetti_faces(
    shuffle: bool = False,
    random_state: Union[int, RandomState, None] = 0,
    download_if_missing: bool = True,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, str]:
    """Load the Olivetti faces data-set from AT&T (classification).

    Download it if necessary.

    =================   =====================
    Classes                                40
    Samples total                         400
    Dimensionality                       4096
    Features            real, between 0 and 1
    =================   =====================

    Read more in the :ref:`User Guide <olivetti_faces_dataset>`.

    Parameters
    ----------
    data_home : str or path-like, default=None
        Specify another download and cache folder for the datasets. By default
        all scikit-learn data is stored in '~/scikit_learn_data' subfolders.

    shuffle : bool, default=False
        If True the order of the dataset is shuffled to avoid having
        images of the same person grouped.

    random_state : int, RandomState instance or None, default=0
        Determines random number generation for dataset shuffling. Pass an int
        for reproducible output across multiple function calls.
        See :term:`Glossary <random_state>`.

    download_if_missing : bool, default=True
        If False, raise an OSError if the data is not locally available
        instead of trying to download the data from the source site.



    Returns
    -------
    data: ndarray, shape (400, 4096)
        Each row corresponds to a ravelled
        face image of original size 64 x 64 pixels.
    images : ndarray, shape (400, 64, 64)
        Each row is a face image
        corresponding to one of the 40 subjects of the dataset.
    target : ndarray, shape (400,)
        Labels associated to each face image.
        Those labels are ranging from 0-39 and correspond to the
        Subject IDs.
    DESCR : str
        Description of the modified Olivetti Faces Dataset.


    """
    out = fetch_olivetti_faces(
        shuffle=shuffle,
        random_state=random_state,
        download_if_missing=download_if_missing,
    )

    data = out["data"]
    images = out["images"]
    target = out["target"]
    DESCR = out["DESCR"]

    return data, images, target, DESCR


# class Parser(Enum):
#     auto = "auto"
#     pandas = "pandas"
#     liac_arff = "liac-arff"

#     @classmethod
#     def default(cls):
#         return cls.pandas.value


# @NodeDecorator(
#     node_id = "_openml",
#     name="fetch_openml",
# )
# def _openml(
#     data_id: DataSet = 2,
#     version: Union[int, Literal["active"]] = "active",
#
#     target_column: Optional[
#         Union[Literal["default-target"], List[str], None]
#     ] = "default-target",
#     cache: bool = True,
#     return_X_y: bool = False,
#     as_frame: Union[bool, Literal["auto"]] = "auto",
#     n_retries: int = 5,
#     delay: float = 1.0,
#     parser: Parser = Parser.default(),
#     read_csv_kwargs: Optional[dict] = None,
# ) -> dict:
#     """Fetch dataset from openml by name or dataset id.

#     Datasets are uniquely identified by either an integer ID or by a
#     combination of name and version (i.e. there might be multiple
#     versions of the 'iris' dataset). Please give either name or data_id
#     (not both). In case a name is given, a version can also be
#     provided.

#     Read more in the :ref:`User Guide <openml>`.

#     .. versionadded:: 0.20

#     .. note:: EXPERIMENTAL

#         The API is experimental (particularly the return value structure),
#         and might have small backward-incompatible changes without notice
#         or warning in future releases.

#     Parameters
#     ----------
#     name : str, default=None
#         String identifier of the dataset. Note that OpenML can have multiple
#         datasets with the same name.

#     version : int or 'active', default='active'
#         Version of the dataset. Can only be provided if also ``name`` is given.
#         If 'active' the oldest version that's still active is used. Since
#         there may be more than one active version of a dataset, and those
#         versions may fundamentally be different from one another, setting an
#         exact version is highly recommended.

#     data_id : int, default=None
#         OpenML ID of the dataset. The most specific way of retrieving a
#         dataset. If data_id is not given, name (and potential version) are
#         used to obtain a dataset.

#     data_home : str or path-like, default=None
#         Specify another download and cache folder for the data sets. By default
#         all scikit-learn data is stored in '~/scikit_learn_data' subfolders.

#     target_column : str, list or None, default='default-target'
#         Specify the column name in the data to use as target. If
#         'default-target', the standard target column a stored on the server
#         is used. If ``None``, all columns are returned as data and the
#         target is ``None``. If list (of strings), all columns with these names
#         are returned as multi-target (Note: not all scikit-learn classifiers
#         can handle all types of multi-output combinations).

#     cache : bool, default=True
#         Whether to cache the downloaded datasets into `data_home`.

#     return_X_y : bool, default=False
#         If True, returns ``(data, target)`` instead of a Bunch object. See
#         below for more information about the `data` and `target` objects.

#     as_frame : bool or 'auto', default='auto'
#         If True, the data is a pandas DataFrame including columns with
#         appropriate dtypes (numeric, string or categorical). The target is
#         a pandas DataFrame or Series depending on the number of target_columns.
#         The Bunch will contain a ``frame`` attribute with the target and the
#         data. If ``return_X_y`` is True, then ``(data, target)`` will be pandas
#         DataFrames or Series as describe above.

#         If `as_frame` is 'auto', the data and target will be converted to
#         DataFrame or Series as if `as_frame` is set to True, unless the dataset
#         is stored in sparse format.

#         If `as_frame` is False, the data and target will be NumPy arrays and
#         the `data` will only contain numerical values when `parser="liac-arff"`
#         where the categories are provided in the attribute `categories` of the
#         `Bunch` instance. When `parser="pandas"`, no ordinal encoding is made.

#         .. versionchanged:: 0.24
#            The default value of `as_frame` changed from `False` to `'auto'`
#            in 0.24.

#     n_retries : int, default=3
#         Number of retries when HTTP errors or network timeouts are encountered.
#         Error with status code 412 won't be retried as they represent OpenML
#         generic errors.

#     delay : float, default=1.0
#         Number of seconds between retries.

#     parser : {"auto", "pandas", "liac-arff"}, default="auto"
#         Parser used to load the ARFF file. Two parsers are implemented:

#         - `"pandas"`: this is the most efficient parser. However, it requires
#           pandas to be installed and can only open dense datasets.
#         - `"liac-arff"`: this is a pure Python ARFF parser that is much less
#           memory- and CPU-efficient. It deals with sparse ARFF datasets.

#         If `"auto"`, the parser is chosen automatically such that `"liac-arff"`
#         is selected for sparse ARFF datasets, otherwise `"pandas"` is selected.

#         .. versionadded:: 1.2
#         .. versionchanged:: 1.4
#            The default value of `parser` changes from `"liac-arff"` to
#            `"auto"`.

#     read_csv_kwargs : dict, default=None
#         Keyword arguments passed to :func:`pandas.read_csv` when loading the data
#         from a ARFF file and using the pandas parser. It can allow to
#         overwrite some default parameters.

#         .. versionadded:: 1.3

#     Returns
#     -------
#     data : :class:`~sklearn.utils.Bunch`
#         Dictionary-like object, with the following attributes.

#         data : np.array, scipy.sparse.csr_matrix of floats, or pandas DataFrame
#             The feature matrix. Categorical features are encoded as ordinals.
#         target : np.array, pandas Series or DataFrame
#             The regression target or classification labels, if applicable.
#             Dtype is float if numeric, and object if categorical. If
#             ``as_frame`` is True, ``target`` is a pandas object.
#         DESCR : str
#             The full description of the dataset.
#         feature_names : list
#             The names of the dataset columns.
#         target_names: list
#             The names of the target columns.

#         .. versionadded:: 0.22

#         categories : dict or None
#             Maps each categorical feature name to a list of values, such
#             that the value encoded as i is ith in the list. If ``as_frame``
#             is True, this is None.
#         details : dict
#             More metadata from OpenML.
#         frame : pandas DataFrame
#             Only present when `as_frame=True`. DataFrame with ``data`` and
#             ``target``.

#     (data, target) : tuple if ``return_X_y`` is True

#         .. note:: EXPERIMENTAL

#             This interface is **experimental** and subsequent releases may
#             change attributes without notice (although there should only be
#             minor changes to ``data`` and ``target``).

#         Missing values in the 'data' are represented as NaN's. Missing values
#         in 'target' are represented as NaN's (numerical target) or None
#         (categorical target).

#     Notes
#     -----
#     The `"pandas"` and `"liac-arff"` parsers can lead to different data types
#     in the output. The notable differences are the following:

#     - The `"liac-arff"` parser always encodes categorical features as `str` objects.
#       To the contrary, the `"pandas"` parser instead infers the type while
#       reading and numerical categories will be casted into integers whenever
#       possible.
#     - The `"liac-arff"` parser uses float64 to encode numerical features
#       tagged as 'REAL' and 'NUMERICAL' in the metadata. The `"pandas"`
#       parser instead infers if these numerical features corresponds
#       to integers and uses panda's Integer extension dtype.
#     - In particular, classification datasets with integer categories are
#       typically loaded as such `(0, 1, ...)` with the `"pandas"` parser while
#       `"liac-arff"` will force the use of string encoded class labels such as
#       `"0"`, `"1"` and so on.
#     - The `"pandas"` parser will not strip single quotes - i.e. `'` - from
#       string columns. For instance, a string `'my string'` will be kept as is
#       while the `"liac-arff"` parser will strip the single quotes. For
#       categorical columns, the single quotes are stripped from the values.

#     In addition, when `as_frame=False` is used, the `"liac-arff"` parser
#     returns ordinally encoded data where the categories are provided in the
#     attribute `categories` of the `Bunch` instance. Instead, `"pandas"` returns
#     a NumPy array were the categories are not encoded.

#     Examples
#     --------
#     >>> from sklearn.datasets import fetch_openml
#     >>> adult = fetch_openml("adult", version=2)  # doctest: +SKIP
#     >>> adult.frame.info()  # doctest: +SKIP
#     <class 'pandas.core.frame.DataFrame'>
#     RangeIndex: 48842 entries, 0 to 48841
#     Data columns (total 15 columns):
#      #   Column          Non-Null Count  Dtype
#     ---  ------          --------------  -----
#      0   age             48842 non-null  int64
#      1   workclass       46043 non-null  category
#      2   fnlwgt          48842 non-null  int64
#      3   education       48842 non-null  category
#      4   education-num   48842 non-null  int64
#      5   marital-status  48842 non-null  category
#      6   occupation      46033 non-null  category
#      7   relationship    48842 non-null  category
#      8   race            48842 non-null  category
#      9   sex             48842 non-null  category
#      10  capital-gain    48842 non-null  int64
#      11  capital-loss    48842 non-null  int64
#      12  hours-per-week  48842 non-null  int64
#      13  native-country  47985 non-null  category
#      14  class           48842 non-null  category
#     dtypes: category(9), int64(6)
#     memory usage: 2.7 MB

#     """

#     def create_openml():
#         return fetch_openml(
#             version=version,
#             data_id=data_id,
#
#             target_column=target_column,
#             cache=cache,
#             return_X_y=return_X_y,
#             as_frame=as_frame,
#             n_retries=n_retries,
#             delay=delay,
#             parser=parser,
#             read_csv_kwargs=read_csv_kwargs,
#         )

#     return create_openml()


@NodeDecorator(
    node_id="sklearn.datasets.fetch_rcv1",
    name="fetch_rcv1",
    outputs=[
        {"name": "data"},
        {"name": "target"},
        {"name": "sample_id"},
        {"name": "target_names"},
        {"name": "DESCR"},
    ],
)
def _rcv1(
    subset: Subset = "train",
    shuffle: bool = False,
    random_state: Union[int, RandomState, None] = 0,
    download_if_missing: bool = True,
) -> Tuple[spmatrix, spmatrix, np.ndarray, np.ndarray, str]:
    """Load the RCV1 multilabel dataset (classification).

    Download it if necessary.

    Version: RCV1-v2, vectors, full sets, topics multilabels.

    =================   =====================
    Classes                               103
    Samples total                      804414
    Dimensionality                      47236
    Features            real, between 0 and 1
    =================   =====================

    Read more in the :ref:`User Guide <rcv1_dataset>`.

    .. versionadded:: 0.17

    Parameters
    ----------
    data_home : str or path-like, default=None
        Specify another download and cache folder for the datasets. By default
        all scikit-learn data is stored in '~/scikit_learn_data' subfolders.

    subset : {'train', 'test', 'all'}, default='all'
        Select the dataset to load: 'train' for the training set
        (23149 samples), 'test' for the test set (781265 samples),
        'all' for both, with the training samples first if shuffle is False.
        This follows the official LYRL2004 chronological split.

    download_if_missing : bool, default=True
        If False, raise an OSError if the data is not locally available
        instead of trying to download the data from the source site.

    random_state : int, RandomState instance or None, default=None
        Determines random number generation for dataset shuffling. Pass an int
        for reproducible output across multiple function calls.
        See :term:`Glossary <random_state>`.

    shuffle : bool, default=False
        Whether to shuffle dataset.


    Returns
    -------
    - data : sparse matrix of shape (804414, 47236), dtype=np.float64
        The array has 0.16% of non zero values. Will be of CSR format.
    - target : sparse matrix of shape (804414, 103), dtype=np.uint8
        Each sample has a value of 1 in its categories, and 0 in others.
        The array has 3.15% of non zero values. Will be of CSR format.
    - sample_id : ndarray of shape (804414,), dtype=np.uint32,
        Identification number of each sample, as ordered in dataset.data.
    - target_names : ndarray of shape (103,), dtype=object
        Names of each target (RCV1 topics), as ordered in dataset.target.
    - DESCR : str
        Description of the RCV1 dataset.

    """
    out = fetch_rcv1(
        subset=subset,
        shuffle=shuffle,
        random_state=random_state,
        download_if_missing=download_if_missing,
    )

    data = out["data"]
    target = out["target"]
    sample_id = out["sample_id"]
    target_names = out["target_names"]
    DESCR = out["DESCR"]

    return data, target, sample_id, target_names, DESCR


# @NodeDecorator(
#     node_id="_species_distributions",
#     name="fetch_species_distributions",
#     outputs=[
#         {"name": "coverages"},
#         {"name": "train"},
#         {"name": "test"},
#         {"name": "Nx"},
#         {"name": "Ny"},
#         {"name": "x_left_lower_corner"},
#         {"name": "y_left_lower_corner"},
#         {"name": "grid_size"},
#     ],
# )
# def _species_distributions(
#     download_if_missing: bool = True,
# ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, int, int, float, float, float]:
#     """Loader for species distribution dataset from Phillips et. al. (2006).

#     Read more in the :ref:`User Guide <species_distribution_dataset>`.

#     Parameters
#     ----------
#     data_home : str or path-like, default=None
#         Specify another download and cache folder for the datasets. By default
#         all scikit-learn data is stored in '~/scikit_learn_data' subfolders.

#     download_if_missing : bool, default=True
#         If False, raise an OSError if the data is not locally available
#         instead of trying to download the data from the source site.

#     Returns
#     -------

#     coverages : array, shape = [14, 1592, 1212]
#         These represent the 14 features measured
#         at each point of the map grid.
#         The latitude/longitude values for the grid are discussed below.
#         Missing data is represented by the value -9999.
#     train : record array, shape = (1624,)
#         The training points for the data.  Each point has three fields:

#         - train['species'] is the species name
#         - train['dd long'] is the longitude, in degrees
#         - train['dd lat'] is the latitude, in degrees
#     test : record array, shape = (620,)
#         The test points for the data.  Same format as the training data.
#     Nx, Ny : integers
#         The number of longitudes (x) and latitudes (y) in the grid
#     x_left_lower_corner, y_left_lower_corner : floats
#         The (x,y) position of the lower-left corner, in degrees
#     grid_size : float
#         The spacing between points of the grid, in degrees

#     Notes
#     -----

#     This dataset represents the geographic distribution of species.
#     The dataset is provided by Phillips et. al. (2006).

#     The two species are:

#     - `"Bradypus variegatus"
#       <http://www.iucnredlist.org/details/3038/0>`_ ,
#       the Brown-throated Sloth.

#     - `"Microryzomys minutus"
#       <http://www.iucnredlist.org/details/13408/0>`_ ,
#       also known as the Forest Small Rice Rat, a rodent that lives in Peru,
#       Colombia, Ecuador, Peru, and Venezuela.

#     - For an example of using this dataset with scikit-learn, see
#       :ref:`examples/applications/plot_species_distribution_modeling.py
#       <sphx_glr_auto_examples_applications_plot_species_distribution_modeling.py>`.

#     References
#     ----------

#     * `"Maximum entropy modeling of species geographic distributions"
#       <http://rob.schapire.net/papers/ecolmod.pdf>`_
#       S. J. Phillips, R. P. Anderson, R. E. Schapire - Ecological Modelling,
#       190:231-259, 2006.

#     Examples
#     --------
#     >>> from sklearn.datasets import fetch_species_distributions
#     >>> species = fetch_species_distributions()
#     >>> species.train[:5]
#     array([(b'microryzomys_minutus', -64.7   , -17.85  ),
#            (b'microryzomys_minutus', -67.8333, -16.3333),
#            (b'microryzomys_minutus', -67.8833, -16.3   ),
#            (b'microryzomys_minutus', -67.8   , -16.2667),
#            (b'microryzomys_minutus', -67.9833, -15.9   )],
#           dtype=[('species', 'S22'), ('dd long', '<f4'), ('dd lat', '<f4')])

#     """

#     out = fetch_species_distributions(
#         download_if_missing=download_if_missing,
#     )
#     coverages = out["coverages"]
#     train = (out["train"],)  # TODO
#     test = (out["test"],)  # TODO
#     Nx = (out["Nx"],)
#     Ny = (out["Ny"],)
#     x_left_lower_corner = (out["x_left_lower_corner"],)
#     y_left_lower_corner = (out["y_left_lower_corner"],)
#     grid_size = (out["grid_size"],)
#     return (
#         coverages,
#         train,
#         test,
#         Nx,
#         Ny,
#         x_left_lower_corner,
#         y_left_lower_corner,
#         grid_size,
#     )


@NodeDecorator(
    node_id="sklearn.datasets.load_breast_cancer",
    name="load_breast_cancer",
    outputs=[
        {"name": "data"},
        {"name": "target"},
        {"name": "feature_names"},
        {"name": "target_names"},
        {"name": "DESCR"},
        {"name": "filename"},
    ],
)
def _breast_cancer() -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, str, str]:
    """Load and return the breast cancer wisconsin dataset (classification).

    The breast cancer dataset is a classic and very easy binary classification
    dataset.

    =================   ==============
    Classes                          2
    Samples per class    212(M),357(B)
    Samples total                  569
    Dimensionality                  30
    Features            real, positive
    =================   ==============

    The copy of UCI ML Breast Cancer Wisconsin (Diagnostic) dataset is
    downloaded from:
    https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic

    Read more in the :ref:`User Guide <breast_cancer_dataset>`.


    Returns
    -------
    data : {ndarray, dataframe} of shape (569, 30)
        The data matrix. If `as_frame=True`, `data` will be a pandas
        DataFrame.
    target : {ndarray, Series} of shape (569,)
        The classification target. If `as_frame=True`, `target` will be
        a pandas Series.
    feature_names : ndarray of shape (30,)
        The names of the dataset columns.
    target_names : ndarray of shape (2,)
        The names of target classes.
    DESCR : str
        The full description of the dataset.
    filename : str
        The path to the location of the data.

    Examples
    --------
    Let's say you are interested in the samples 10, 50, and 85, and want to
    know their class name.

    >>> from sklearn.datasets import load_breast_cancer
    >>> data = load_breast_cancer()
    >>> data.target[[10, 50, 85]]
    array([0, 1, 0])
    >>> list(data.target_names)
    ['malignant', 'benign']
    """

    out = load_breast_cancer(
        return_X_y=False,
    )

    data = out["data"]
    target = out["target"]
    feature_names = out["feature_names"]
    target_names = out["target_names"]
    DESCR = out["DESCR"]
    filename = out["filename"]

    return data, target, feature_names, target_names, DESCR, filename


@NodeDecorator(
    node_id="sklearn.datasets.load_breast_cancer_as_frame",
    name="load_breast_cancer_as_frame",
    outputs=[
        {"name": "data"},
        {"name": "target"},
        {"name": "feature_names"},
        {"name": "target_names"},
        {"name": "DESCR"},
        {"name": "filename"},
    ],
)
def _breast_cancer_as_frame() -> (
    Tuple[DataFrame, Series, np.ndarray, np.ndarray, str, str]
):
    """Load and return the breast cancer wisconsin dataset (classification).

    The breast cancer dataset is a classic and very easy binary classification
    dataset.

    =================   ==============
    Classes                          2
    Samples per class    212(M),357(B)
    Samples total                  569
    Dimensionality                  30
    Features            real, positive
    =================   ==============

    The copy of UCI ML Breast Cancer Wisconsin (Diagnostic) dataset is
    downloaded from:
    https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic

    Read more in the :ref:`User Guide <breast_cancer_dataset>`.


    Returns
    -------
    data :  dataframe of shape (569, 30)
        The data matrix. If `as_frame=True`, `data` will be a pandas
        DataFrame.
    target : Series of shape (569,)
        The classification target. If `as_frame=True`, `target` will be
        a pandas Series.
    feature_names : ndarray of shape (30,)
        The names of the dataset columns.
    target_names : ndarray of shape (2,)
        The names of target classes.
    DESCR : str
        The full description of the dataset.
    filename : str
        The path to the location of the data.

    Examples
    --------
    Let's say you are interested in the samples 10, 50, and 85, and want to
    know their class name.

    >>> from sklearn.datasets import load_breast_cancer
    >>> data = load_breast_cancer()
    >>> data.target[[10, 50, 85]]
    array([0, 1, 0])
    >>> list(data.target_names)
    ['malignant', 'benign']
    """

    out = load_breast_cancer(return_X_y=False, as_frame=True)

    data = out["data"]
    target = out["target"]
    feature_names = out["feature_names"]
    target_names = out["target_names"]
    DESCR = out["DESCR"]
    filename = out["filename"]

    return data, target, feature_names, target_names, DESCR, filename


@NodeDecorator(
    node_id="sklearn.datasets.load_diabetes",
    name="load_diabetes",
    outputs=[
        {"name": "data"},
        {"name": "target"},
        {"name": "feature_names"},
        {"name": "DESCR"},
        {"name": "data_filename"},
        {"name": "target_filename"},
    ],
)
def _diabetes(
    scaled: bool = True,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, str, str]:
    """Load and return the diabetes dataset (regression).

    ==============   ==================
    Samples total    442
    Dimensionality   10
    Features         real, -.2 < x < .2
    Targets          integer 25 - 346
    ==============   ==================

    .. note::
       The meaning of each feature (i.e. `feature_names`) might be unclear
       (especially for `ltg`) as the documentation of the original dataset is
       not explicit. We provide information that seems correct in regard with
       the scientific literature in this field of research.

    Read more in the :ref:`User Guide <diabetes_dataset>`.

    Parameters
    ----------
    scaled : bool, default=True
        If True, the feature variables are mean centered and scaled by the
        standard deviation times the square root of `n_samples`.
        If False, raw data is returned for the feature variables.

        .. versionadded:: 1.1

    Returns
    -------
        data : ndarray of shape (442, 10)
            The data matrix. If `as_frame=True`, `data` will be a pandas
            DataFrame.
        target: ndarray of shape (442,)
            The regression target. If `as_frame=True`, `target` will be
            a pandas Series.
        feature_names: list
            The names of the dataset columns.
        DESCR: str
            The full description of the dataset.
        data_filename: str
            The path to the location of the data.
        target_filename: str
            The path to the location of the target.

    Examples
    --------
    >>> from sklearn.datasets import load_diabetes
    >>> diabetes = load_diabetes()
    >>> diabetes.target[:3]
    array([151.,  75., 141.])
    >>> diabetes.data.shape
    (442, 10)

    """

    out = load_diabetes(
        scaled=scaled,
    )

    data = out["data"]
    target = out["target"]
    feature_names = out["feature_names"]
    DESCR = out["DESCR"]
    data_filename = out["data_filename"]
    target_filename = out["target_filename"]

    return data, target, feature_names, DESCR, data_filename, target_filename


@NodeDecorator(
    node_id="sklearn.datasets.load_diabetes_as_frame",
    name="load_diabetes_as_frame",
    outputs=[
        {"name": "data"},
        {"name": "target"},
        {"name": "feature_names"},
        {"name": "DESCR"},
        {"name": "data_filename"},
        {"name": "target_filename"},
    ],
)
def _diabetes_as_frame(
    scaled: bool = True,
) -> Tuple[DataFrame, Series, np.ndarray, np.ndarray, str, str]:
    """Load and return the diabetes dataset (regression).

    ==============   ==================
    Samples total    442
    Dimensionality   10
    Features         real, -.2 < x < .2
    Targets          integer 25 - 346
    ==============   ==================

    .. note::
       The meaning of each feature (i.e. `feature_names`) might be unclear
       (especially for `ltg`) as the documentation of the original dataset is
       not explicit. We provide information that seems correct in regard with
       the scientific literature in this field of research.

    Read more in the :ref:`User Guide <diabetes_dataset>`.

    Parameters
    ----------
    scaled : bool, default=True
        If True, the feature variables are mean centered and scaled by the
        standard deviation times the square root of `n_samples`.
        If False, raw data is returned for the feature variables.

        .. versionadded:: 1.1

    Returns
    -------
        data : DataFrame of shape (442, 10)
            The data matrix. If `as_frame=True`, `data` will be a pandas
            DataFrame.
        target: Series of shape (442,)
            The regression target. If `as_frame=True`, `target` will be
            a pandas Series.
        feature_names: list
            The names of the dataset columns.
        DESCR: str
            The full description of the dataset.
        data_filename: str
            The path to the location of the data.
        target_filename: str
            The path to the location of the target.

    Examples
    --------
    >>> from sklearn.datasets import load_diabetes
    >>> diabetes = load_diabetes()
    >>> diabetes.target[:3]
    array([151.,  75., 141.])
    >>> diabetes.data.shape
    (442, 10)

    """

    out = load_diabetes(scaled=scaled, as_frame=True)

    data = out["data"]
    target = out["target"]
    feature_names = out["feature_names"]
    DESCR = out["DESCR"]
    data_filename = out["data_filename"]
    target_filename = out["target_filename"]

    return data, target, feature_names, DESCR, data_filename, target_filename


@NodeDecorator(
    node_id="sklearn.datasets.load_digits",
    name="load_digits",
    outputs=[
        {"name": "data"},
        {"name": "target"},
        {"name": "feature_names"},
        {"name": "target_names"},
        {"name": "images"},
        {"name": "DESCR"},
    ],
)
def _digits(
    n_class: int = 10,
) -> Tuple[np.ndarray, np.ndarray, List[str], List[str], np.ndarray, str]:
    """Load and return the digits dataset (classification).

    Each datapoint is a 8x8 image of a digit.

    =================   ==============
    Classes                         10
    Samples per class             ~180
    Samples total                 1797
    Dimensionality                  64
    Features             integers 0-16
    =================   ==============

    This is a copy of the test set of the UCI ML hand-written digits datasets
    https://archive.ics.uci.edu/ml/datasets/Optical+Recognition+of+Handwritten+Digits

    Read more in the :ref:`User Guide <digits_dataset>`.

    Parameters
    ----------
    n_class : int, default=10
        The number of classes to return. Between 0 and 10.


    Returns
    -------
    data : ndarray of shape (1797, 64)
        The flattened data matrix. If `as_frame=True`, `data` will be
        a pandas DataFrame.
    target: ndarray of shape (1797,)
        The classification target. If `as_frame=True`, `target` will be
        a pandas Series.
    feature_names: list
        The names of the dataset columns.
    target_names: list
        The names of target classes.
    images: {ndarray} of shape (1797, 8, 8)
        The raw image data.
    DESCR: str
        The full description of the dataset.


    Examples
    --------
    To load the data and visualize the images::

        >>> from sklearn.datasets import load_digits
        >>> digits = load_digits()
        >>> print(digits.data.shape)
        (1797, 64)
        >>> import matplotlib.pyplot as plt
        >>> plt.gray()
        >>> plt.matshow(digits.images[0])
        <...>
        >>> plt.show()

    """

    out = load_digits(
        n_class=n_class,
    )

    data = out["data"]
    target = out["target"]
    feature_names = out["feature_names"]
    target_names = out["target_names"]
    images = out["images"]
    DESCR = out["DESCR"]

    return data, target, feature_names, target_names, DESCR, images


@NodeDecorator(
    node_id="sklearn.datasets.load_digits_as_frame",
    name="load_digits_as_frame",
    outputs=[
        {"name": "data"},
        {"name": "target"},
        {"name": "feature_names"},
        {"name": "target_names"},
        {"name": "images"},
        {"name": "DESCR"},
    ],
)
def _digits_as_frame(
    n_class: int = 10,
) -> Tuple[DataFrame, Series, List[str], List[str], np.ndarray, str]:
    """Load and return the digits dataset (classification).

    Each datapoint is a 8x8 image of a digit.

    =================   ==============
    Classes                         10
    Samples per class             ~180
    Samples total                 1797
    Dimensionality                  64
    Features             integers 0-16
    =================   ==============

    This is a copy of the test set of the UCI ML hand-written digits datasets
    https://archive.ics.uci.edu/ml/datasets/Optical+Recognition+of+Handwritten+Digits

    Read more in the :ref:`User Guide <digits_dataset>`.

    Parameters
    ----------
    n_class : int, default=10
        The number of classes to return. Between 0 and 10.


    Returns
    -------
    data : dataframe of shape (1797, 64)
        The flattened data matrix. If `as_frame=True`, `data` will be
        a pandas DataFrame.
    target: Series of shape (1797,)
        The classification target. If `as_frame=True`, `target` will be
        a pandas Series.
    feature_names: list
        The names of the dataset columns.
    target_names: list
        The names of target classes.
    images: {ndarray} of shape (1797, 8, 8)
        The raw image data.
    DESCR: str
        The full description of the dataset.


    Examples
    --------
    To load the data and visualize the images::

        >>> from sklearn.datasets import load_digits
        >>> digits = load_digits()
        >>> print(digits.data.shape)
        (1797, 64)
        >>> import matplotlib.pyplot as plt
        >>> plt.gray()
        >>> plt.matshow(digits.images[0])
        <...>
        >>> plt.show()

    """

    out = load_digits(
        n_class=n_class,
    )

    data = out["data"]
    target = out["target"]
    feature_names = out["feature_names"]
    target_names = out["target_names"]
    images = out["images"]
    DESCR = out["DESCR"]

    return data, target, feature_names, target_names, DESCR, images


# class DecodeError(Enum):
#     STRICT = "strict"
#     IGNORE = "ignore"
#     REPLACE = "replace"

#     @classmethod
#     def default(cls):
#         return cls.STRICT.value


# @NodeDecorator(
#     node_id = "_text_files",
#     name="load_files",
# )
# def _text_files(
#     container_path: str = "path/to/textfiles",
#     description: Optional[str] = "Folder with text files",
#     categories: Optional[List[str]] = None,
#     load_content: bool = True,
#     decode_error: DecodeError = DecodeError.default(),
#     shuffle: bool = True,
#     encoding: Optional[str] = "utf-8",
#     random_state: Optional[Union[int, RandomState, None]] = 0,
#     allowed_extensions: Optional[List[str]] = None,
# ) -> dict:
#     """Load text files with categories as subfolder names.

#     Individual samples are assumed to be files stored a two levels folder
#     structure such as the following:

#         container_folder/
#             category_1_folder/
#                 file_1.txt
#                 file_2.txt
#                 ...
#                 file_42.txt
#             category_2_folder/
#                 file_43.txt
#                 file_44.txt
#                 ...

#     The folder names are used as supervised signal label names. The individual
#     file names are not important.

#     This function does not try to extract features into a numpy array or scipy
#     sparse matrix. In addition, if load_content is false it does not try to
#     load the files in memory.

#     To use text files in a scikit-learn classification or clustering algorithm,
#     you will need to use the :mod:`~sklearn.feature_extraction.text` module to
#     build a feature extraction transformer that suits your problem.

#     If you set load_content=True, you should also specify the encoding of the
#     text using the 'encoding' parameter. For many modern text files, 'utf-8'
#     will be the correct encoding. If you leave encoding equal to None, then the
#     content will be made of bytes instead of Unicode, and you will not be able
#     to use most functions in :mod:`~sklearn.feature_extraction.text`.

#     Similar feature extractors should be built for other kind of unstructured
#     data input such as images, audio, video, ...

#     If you want files with a specific file extension (e.g. `.txt`) then you
#     can pass a list of those file extensions to `allowed_extensions`.

#     Read more in the :ref:`User Guide <datasets>`.

#     Parameters
#     ----------
#     container_path : str
#         Path to the main folder holding one subfolder per category.

#     description : str, default=None
#         A paragraph describing the characteristic of the dataset: its source,
#         reference, etc.

#     categories : list of str, default=None
#         If None (default), load all the categories. If not None, list of
#         category names to load (other categories ignored).

#     load_content : bool, default=True
#         Whether to load or not the content of the different files. If true a
#         'data' attribute containing the text information is present in the data
#         structure returned. If not, a filenames attribute gives the path to the
#         files.

#     shuffle : bool, default=True
#         Whether or not to shuffle the data: might be important for models that
#         make the assumption that the samples are independent and identically
#         distributed (i.i.d.), such as stochastic gradient descent.

#     encoding : str, default=None
#         If None, do not try to decode the content of the files (e.g. for images
#         or other non-text content). If not None, encoding to use to decode text
#         files to Unicode if load_content is True.

#     decode_error : {'strict', 'ignore', 'replace'}, default='strict'
#         Instruction on what to do if a byte sequence is given to analyze that
#         contains characters not of the given `encoding`. Passed as keyword
#         argument 'errors' to bytes.decode.

#     random_state : int, RandomState instance or None, default=0
#         Determines random number generation for dataset shuffling. Pass an int
#         for reproducible output across multiple function calls.
#         See :term:`Glossary <random_state>`.

#     allowed_extensions : list of str, default=None
#         List of desired file extensions to filter the files to be loaded.

#     Returns
#     -------
#     data : :class:`~sklearn.utils.Bunch`
#         Dictionary-like object, with the following attributes.

#         data : list of str
#             Only present when `load_content=True`.
#             The raw text data to learn.
#         target : ndarray
#             The target labels (integer index).
#         target_names : list
#             The names of target classes.
#         DESCR : str
#             The full description of the dataset.
#         filenames: ndarray
#             The filenames holding the dataset.

#     Examples
#     --------
#     >>> from sklearn.datasets import load_files
#     >>> container_path = "./"
#     >>> load_files(container_path)  # doctest: +SKIP

#     """

#     def create_text_files():
#         return load_files(
#             container_path=container_path,
#             description=description,
#             categories=categories,
#             load_content=load_content,
#             shuffle=shuffle,
#             encoding=encoding,
#             decode_error=decode_error,
#             random_state=random_state,
#             allowed_extensions=allowed_extensions,
#         )

#     return create_text_files()


@NodeDecorator(
    node_id="sklearn.datasets.load_iris",
    name="load_iris",
    outputs=[
        {"name": "data"},
        {"name": "target"},
        {"name": "feature_names"},
        {"name": "target_names"},
        {"name": "DESCR"},
        {"name": "filename"},
    ],
)
def _iris() -> Tuple[np.ndarray, np.ndarray, List[str], List[str], str, str]:
    """Load and return the iris dataset (classification).

    The iris dataset is a classic and very easy multi-class classification
    dataset.

    =================   ==============
    Classes                          3
    Samples per class               50
    Samples total                  150
    Dimensionality                   4
    Features            real, positive
    =================   ==============

    Read more in the :ref:`User Guide <iris_dataset>`.

    Parameters
    ----------
    return_X_y : bool, default=False
        If True, returns ``(data, target)`` instead of a Bunch object. See
        below for more information about the `data` and `target` object.

        .. versionadded:: 0.18

    as_frame : bool, default=False
        If True, the data is a pandas DataFrame including columns with
        appropriate dtypes (numeric). The target is
        a pandas DataFrame or Series depending on the number of target columns.
        If `return_X_y` is True, then (`data`, `target`) will be pandas
        DataFrames or Series as described below.

        .. versionadded:: 0.23

    Returns
    -------
    data : ndarray of shape (150, 4)
        The data matrix. If `as_frame=True`, `data` will be a pandas
        DataFrame.
    target: ndarray of shape (150,)
        The classification target. If `as_frame=True`, `target` will be
        a pandas Series.
    feature_names: list
        The names of the dataset columns.
    target_names: list
        The names of target classes.
    DESCR: str
        The full description of the dataset.
    filename: str
            The path to the location of the data.


    Notes
    -----
        .. versionchanged:: 0.20
            Fixed two wrong data points according to Fisher's paper.
            The new version is the same as in R, but not as in the UCI
            Machine Learning Repository.

    Examples
    --------
    Let's say you are interested in the samples 10, 25, and 50, and want to
    know their class name.

    >>> from sklearn.datasets import load_iris
    >>> data = load_iris()
    >>> data.target[[10, 25, 50]]
    array([0, 0, 1])
    >>> list(data.target_names)
    ['setosa', 'versicolor', 'virginica']

    See :ref:`sphx_glr_auto_examples_datasets_plot_iris_dataset.py` for a more
    detailed example of how to work with the iris dataset.

    """

    out = load_iris()

    data = out["data"]
    target = out["target"]
    feature_names = out["feature_names"]
    target_names = out["target_names"]
    DESCR = out["DESCR"]
    filename = out["filename"]

    return data, target, feature_names, target_names, DESCR, filename


@NodeDecorator(
    node_id="sklearn.datasets.load_iris_as_frame",
    name="load_iris_as_frame",
    outputs=[
        {"name": "data"},
        {"name": "target"},
        {"name": "feature_names"},
        {"name": "target_names"},
        {"name": "DESCR"},
        {"name": "filename"},
    ],
)
def _iris_as_frame() -> Tuple[DataFrame, Series, List[str], List[str], str, str]:
    """Load and return the iris dataset (classification).

    The iris dataset is a classic and very easy multi-class classification
    dataset.

    =================   ==============
    Classes                          3
    Samples per class               50
    Samples total                  150
    Dimensionality                   4
    Features            real, positive
    =================   ==============

    Read more in the :ref:`User Guide <iris_dataset>`.

    Parameters
    ----------
    return_X_y : bool, default=False
        If True, returns ``(data, target)`` instead of a Bunch object. See
        below for more information about the `data` and `target` object.

        .. versionadded:: 0.18

    as_frame : bool, default=False
        If True, the data is a pandas DataFrame including columns with
        appropriate dtypes (numeric). The target is
        a pandas DataFrame or Series depending on the number of target columns.
        If `return_X_y` is True, then (`data`, `target`) will be pandas
        DataFrames or Series as described below.

        .. versionadded:: 0.23

    Returns
    -------
    data : dataframe of shape (150, 4)
        The data matrix. If `as_frame=True`, `data` will be a pandas
        DataFrame.
    target: Series of shape (150,)
        The classification target. If `as_frame=True`, `target` will be
        a pandas Series.
    feature_names: list
        The names of the dataset columns.
    target_names: list
        The names of target classes.
    DESCR: str
        The full description of the dataset.
    filename: str
            The path to the location of the data.


    Notes
    -----
        .. versionchanged:: 0.20
            Fixed two wrong data points according to Fisher's paper.
            The new version is the same as in R, but not as in the UCI
            Machine Learning Repository.

    Examples
    --------
    Let's say you are interested in the samples 10, 25, and 50, and want to
    know their class name.

    >>> from sklearn.datasets import load_iris
    >>> data = load_iris()
    >>> data.target[[10, 25, 50]]
    array([0, 0, 1])
    >>> list(data.target_names)
    ['setosa', 'versicolor', 'virginica']

    See :ref:`sphx_glr_auto_examples_datasets_plot_iris_dataset.py` for a more
    detailed example of how to work with the iris dataset.

    """

    out = load_iris(as_frame=True)

    data = out["data"]
    target = out["target"]
    feature_names = out["feature_names"]
    target_names = out["target_names"]
    DESCR = out["DESCR"]
    filename = out["filename"]

    return data, target, feature_names, target_names, DESCR, filename


@NodeDecorator(
    node_id="sklearn.datasets.load_linnerud",
    name="load_linnerud",
    outputs=[
        {"name": "data"},
        {"name": "target"},
        {"name": "feature_names"},
        {"name": "target_names"},
        {"name": "DESCR"},
        {"name": "data_filename"},
        {"name": "target_filename"},
    ],
)
def _linnerud() -> Tuple[np.ndarray, np.ndarray, List[str], List[str], str, str, str]:
    """Load and return the physical exercise Linnerud dataset.

    This dataset is suitable for multi-output regression tasks.

    ==============   ============================
    Samples total    20
    Dimensionality   3 (for both data and target)
    Features         integer
    Targets          integer
    ==============   ============================

    Read more in the :ref:`User Guide <linnerrud_dataset>`.


    Returns
    -------

    data : ndarray of shape (20, 3)
        The data matrix. If `as_frame=True`, `data` will be a pandas
        DataFrame.
    target: ndarray of shape (20, 3)
        The regression targets. If `as_frame=True`, `target` will be
        a pandas DataFrame.
    feature_names: list
        The names of the dataset columns.
    target_names: list
        The names of the target columns.
    DESCR: str
        The full description of the dataset.
    data_filename: str
        The path to the location of the data.
    target_filename: str
        The path to the location of the target.


    """

    out = load_linnerud()

    data = out["data"]
    target = out["target"]
    feature_names = out["feature_names"]
    target_names = out["target_names"]
    DESCR = out["DESCR"]
    data_filename = out["data_filename"]
    target_filename = out["target_filename"]

    return (
        data,
        target,
        feature_names,
        target_names,
        DESCR,
        data_filename,
        target_filename,
    )


@NodeDecorator(
    node_id="sklearn.datasets.load_linnerud_as_frame",
    name="load_linnerud_as_frame",
    outputs=[
        {"name": "data"},
        {"name": "target"},
        {"name": "feature_names"},
        {"name": "target_names"},
        {"name": "DESCR"},
        {"name": "data_filename"},
        {"name": "target_filename"},
    ],
)
def _linnerud_as_frame() -> (
    Tuple[DataFrame, DataFrame, List[str], List[str], str, str, str]
):
    """Load and return the physical exercise Linnerud dataset.

    This dataset is suitable for multi-output regression tasks.

    ==============   ============================
    Samples total    20
    Dimensionality   3 (for both data and target)
    Features         integer
    Targets          integer
    ==============   ============================

    Read more in the :ref:`User Guide <linnerrud_dataset>`.


    Returns
    -------

    data : dataframe of shape (20, 3)
        The data matrix. If `as_frame=True`, `data` will be a pandas
        DataFrame.
    target: series of shape (20, 3)
        The regression targets. If `as_frame=True`, `target` will be
        a pandas DataFrame.
    feature_names: list
        The names of the dataset columns.
    target_names: list
        The names of the target columns.
    DESCR: str
        The full description of the dataset.
    data_filename: str
        The path to the location of the data.
    target_filename: str
        The path to the location of the target.


    """

    out = load_linnerud(as_frame=True)

    data = out["data"]
    target = out["target"]
    feature_names = out["feature_names"]
    target_names = out["target_names"]
    DESCR = out["DESCR"]
    data_filename = out["data_filename"]
    target_filename = out["target_filename"]

    return (
        data,
        target,
        feature_names,
        target_names,
        DESCR,
        data_filename,
        target_filename,
    )


class SampleImage(Enum):
    china = "china.jpg"
    flower = "flower.jpg"

    @classmethod
    def default(cls):
        return cls.flower.value


@NodeDecorator(
    node_id="sklearn.datasets.load_sample_image",
    name="load_sample_image",
)
def _sample_image(
    image_name: SampleImage = SampleImage.default(),
) -> np.ndarray:
    """Load the numpy array of a single sample image.

    Read more in the :ref:`User Guide <sample_images>`.

    Parameters
    ----------
    image_name : {`china.jpg`, `flower.jpg`}
        The name of the sample image loaded.

    Returns
    -------
    img : 3D array
        The image as a numpy array: height x width x color.

    Examples
    --------

    >>> from sklearn.datasets import load_sample_image
    >>> china = load_sample_image('china.jpg')   # doctest: +SKIP
    >>> china.dtype                              # doctest: +SKIP
    dtype('uint8')
    >>> china.shape                              # doctest: +SKIP
    (427, 640, 3)
    >>> flower = load_sample_image('flower.jpg') # doctest: +SKIP
    >>> flower.dtype                             # doctest: +SKIP
    dtype('uint8')
    >>> flower.shape                             # doctest: +SKIP
    (427, 640, 3)
    """

    return load_sample_image(image_name=image_name)


# @NodeDecorator(
#     node_id = "_svmlight_file",
#     name="load_svmlight_file",
# )
# def _svmlight_file(
#     f: Union[str, int, os.PathLike],
#     n_features: Optional[int] = None,
#     dtype: Type[np.generic] = np.float32,
#     multilabel: bool = False,
#     zero_based: Optional[Union[Literal["auto"], bool]] = "auto",
#     query_id: bool = False,
#     offset: int = 0,
#     length: int = -1,
# ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
#     """Load datasets in the svmlight / libsvm format into sparse CSR matrix.

#     This format is a text-based format, with one sample per line. It does
#     not store zero valued features hence is suitable for sparse dataset.

#     The first element of each line can be used to store a target variable
#     to predict.

#     This format is used as the default format for both svmlight and the
#     libsvm command line programs.

#     Parsing a text based source can be expensive. When repeatedly
#     working on the same dataset, it is recommended to wrap this
#     loader with joblib.Memory.cache to store a memmapped backup of the
#     CSR results of the first call and benefit from the near instantaneous
#     loading of memmapped structures for the subsequent calls.

#     In case the file contains a pairwise preference constraint (known
#     as "qid" in the svmlight format) these are ignored unless the
#     query_id parameter is set to True. These pairwise preference
#     constraints can be used to constraint the combination of samples
#     when using pairwise loss functions (as is the case in some
#     learning to rank problems) so that only pairs with the same
#     query_id value are considered.

#     This implementation is written in Cython and is reasonably fast.
#     However, a faster API-compatible loader is also available at:

#       https://github.com/mblondel/svmlight-loader

#     Parameters
#     ----------
#     f : str, path-like, file-like or int
#         (Path to) a file to load. If a path ends in ".gz" or ".bz2", it will
#         be uncompressed on the fly. If an integer is passed, it is assumed to
#         be a file descriptor. A file-like or file descriptor will not be closed
#         by this function. A file-like object must be opened in binary mode.

#         .. versionchanged:: 1.2
#            Path-like objects are now accepted.

#     n_features : int, default=None
#         The number of features to use. If None, it will be inferred. This
#         argument is useful to load several files that are subsets of a
#         bigger sliced dataset: each subset might not have examples of
#         every feature, hence the inferred shape might vary from one
#         slice to another.
#         n_features is only required if ``offset`` or ``length`` are passed a
#         non-default value.

#     dtype : numpy data type, default=np.float64
#         Data type of dataset to be loaded. This will be the data type of the
#         output numpy arrays ``X`` and ``y``.

#     multilabel : bool, default=False
#         Samples may have several labels each (see
#         https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/multilabel.html).

#     zero_based : bool or "auto", default="auto"
#         Whether column indices in f are zero-based (True) or one-based
#         (False). If column indices are one-based, they are transformed to
#         zero-based to match Python/NumPy conventions.
#         If set to "auto", a heuristic check is applied to determine this from
#         the file contents. Both kinds of files occur "in the wild", but they
#         are unfortunately not self-identifying. Using "auto" or True should
#         always be safe when no ``offset`` or ``length`` is passed.
#         If ``offset`` or ``length`` are passed, the "auto" mode falls back
#         to ``zero_based=True`` to avoid having the heuristic check yield
#         inconsistent results on different segments of the file.

#     query_id : bool, default=False
#         If True, will return the query_id array for each file.

#     offset : int, default=0
#         Ignore the offset first bytes by seeking forward, then
#         discarding the following bytes up until the next new line
#         character.

#     length : int, default=-1
#         If strictly positive, stop reading any new line of data once the
#         position in the file has reached the (offset + length) bytes threshold.

#     Returns
#     -------
#     X : scipy.sparse matrix of shape (n_samples, n_features)
#         The data matrix.

#     y : ndarray of shape (n_samples,), or a list of tuples of length n_samples
#         The target. It is a list of tuples when ``multilabel=True``, else a
#         ndarray.

#     query_id : array of shape (n_samples,)
#        The query_id for each sample. Only returned when query_id is set to
#        True.

#     See Also
#     --------
#     load_svmlight_files : Similar function for loading multiple files in this
#         format, enforcing the same number of features/columns on all of them.

#     Examples
#     --------
#     To use joblib.Memory to cache the svmlight file::

#         from joblib import Memory
#         from .datasets import load_svmlight_file
#         mem = Memory("./mycache")

#         @mem.cache
#         def get_data():
#             data = load_svmlight_file("mysvmlightfile")
#             return data[0], data[1]

#         X, y = get_data()

#     """

#     def create_svmlight_file():
#         return load_svmlight_file(
#             f=f,
#             n_features=n_features,
#             dtype=dtype,
#             multilabel=multilabel,
#             zero_based=zero_based,
#             query_id=query_id,
#             offset=offset,
#             length=length,
#         )

#     return create_svmlight_file()


@NodeDecorator(
    node_id="sklearn.datasets.load_wine",
    name="load_wine",
    outputs=[
        {"name": "data"},
        {"name": "target"},
        {"name": "feature_names"},
        {"name": "target_names"},
        {"name": "DESCR"},
    ],
)
def _wine() -> Tuple[np.ndarray, np.ndarray, List[str], List[str], str]:
    """Load and return the wine dataset (classification).

    .. versionadded:: 0.18

    The wine dataset is a classic and very easy multi-class classification
    dataset.

    =================   ==============
    Classes                          3
    Samples per class        [59,71,48]
    Samples total                  178
    Dimensionality                  13
    Features            real, positive
    =================   ==============

    The copy of UCI ML Wine Data Set dataset is downloaded and modified to fit
    standard format from:
    https://archive.ics.uci.edu/ml/machine-learning-databases/wine/wine.data

    Read more in the :ref:`User Guide <wine_dataset>`.

    Returns
    -------
        data : ndarray of shape (178, 13)
            The data matrix. If `as_frame=True`, `data` will be a pandas
            DataFrame.
        target: ndarray of shape (178,)
            The classification target. If `as_frame=True`, `target` will be
            a pandas Series.
        feature_names: list
            The names of the dataset columns.
        target_names: list
            The names of target classes.
        DESCR: str
            The full description of the dataset.

    Examples
    --------
    Let's say you are interested in the samples 10, 80, and 140, and want to
    know their class name.

    >>> from sklearn.datasets import load_wine
    >>> data = load_wine()
    >>> data.target[[10, 80, 140]]
    array([0, 1, 2])
    >>> list(data.target_names)
    ['class_0', 'class_1', 'class_2']

    """
    out = load_wine()
    data = out["data"]
    target = out["target"]
    feature_names = out["feature_names"]
    target_names = out["target_names"]
    DESCR = out["DESCR"]

    return data, target, feature_names, target_names, DESCR


@NodeDecorator(
    node_id="sklearn.datasets.load_wine_as_frame",
    name="load_wine_as_frame",
    outputs=[
        {"name": "data"},
        {"name": "target"},
        {"name": "feature_names"},
        {"name": "target_names"},
        {"name": "DESCR"},
    ],
)
def _wine_as_frame() -> Tuple[DataFrame, Series, List[str], List[str], str]:
    """Load and return the wine dataset (classification).

    .. versionadded:: 0.18

    The wine dataset is a classic and very easy multi-class classification
    dataset.

    =================   ==============
    Classes                          3
    Samples per class        [59,71,48]
    Samples total                  178
    Dimensionality                  13
    Features            real, positive
    =================   ==============

    The copy of UCI ML Wine Data Set dataset is downloaded and modified to fit
    standard format from:
    https://archive.ics.uci.edu/ml/machine-learning-databases/wine/wine.data

    Read more in the :ref:`User Guide <wine_dataset>`.

    Returns
    -------
        data : Dataframe of shape (178, 13)
            The data matrix. If `as_frame=True`, `data` will be a pandas
            DataFrame.
        target: Series of shape (178,)
            The classification target. If `as_frame=True`, `target` will be
            a pandas Series.
        feature_names: list
            The names of the dataset columns.
        target_names: list
            The names of target classes.
        DESCR: str
            The full description of the dataset.

    Examples
    --------
    Let's say you are interested in the samples 10, 80, and 140, and want to
    know their class name.

    >>> from sklearn.datasets import load_wine
    >>> data = load_wine()
    >>> data.target[[10, 80, 140]]
    array([0, 1, 2])
    >>> list(data.target_names)
    ['class_0', 'class_1', 'class_2']

    """
    out = load_wine(as_frame=True)
    data = out["data"]
    target = out["target"]
    feature_names = out["feature_names"]
    target_names = out["target_names"]
    DESCR = out["DESCR"]

    return data, target, feature_names, target_names, DESCR


LOADERS_NODE_SHELF = Shelf(
    nodes=[
        _20newsgroups,
        _20newsgroups_vectorized,
        _20newsgroups_vectorized_as_frame,
        _california_housing,
        _california_housing_as_frame,
        _covtype,
        _covtype_as_frame,
        _kddcup99,
        _kddcup99_as_frame,
        _lfw_pairs,
        _lfw_people,
        _olivetti_faces,
        # _openml,
        _rcv1,
        # _species_distributions,
        _breast_cancer,
        _breast_cancer_as_frame,
        _diabetes,
        _diabetes_as_frame,
        _digits,
        _digits_as_frame,
        # _text_files,
        _iris,
        _iris_as_frame,
        _linnerud,
        _linnerud_as_frame,
        _sample_image,
        # _svmlight_file,
        _wine,
        _wine_as_frame,
    ],
    subshelves=[],
    name="Loaders",
    description="The sklearn.datasets package embeds some small toy datasets as introduced in the Getting Started section. This package also features helpers to fetch larger datasets commonly used by the machine learning community to benchmark algorithms on data that comes from the ‘real world’. To evaluate the impact of the scale of the dataset (n_samples and n_features) while controlling the statistical properties of the data (typically the correlation and informativeness of the features), it is also possible to generate synthetic data.",
)


@NodeDecorator(
    node_id = "sklearn.datasets.make_biclusters",
    name="make_biclusters",
    outputs=[
        {"name": "X"},
        {"name": "rows"},
        {"name": "cols"},
    ],
)
def _biclusters(
    shape: Tuple[int, int],
    n_clusters: int,
    noise: float = 0.0,
    minval: float = 10,
    maxval: float = 100,
    shuffle: bool = True,
    random_state: Optional[Union[int, RandomState]] = None,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Generate a constant block diagonal structure array for biclustering.

    Read more in the :ref:`User Guide <sample_generators>`.

    Parameters
    ----------
    shape : tuple of shape (n_rows, n_cols)
        The shape of the result.

    n_clusters : int
        The number of biclusters.

    noise : float, default=0.0
        The standard deviation of the gaussian noise.

    minval : float, default=10
        Minimum value of a bicluster.

    maxval : float, default=100
        Maximum value of a bicluster.

    shuffle : bool, default=True
        Shuffle the samples.

    random_state : int, RandomState instance or None, default=None
        Determines random number generation for dataset creation. Pass an int
        for reproducible output across multiple function calls.
        See :term:`Glossary <random_state>`.

    Returns
    -------
    X : ndarray of shape `shape`
        The generated array.

    rows : ndarray of shape (n_clusters, X.shape[0])
        The indicators for cluster membership of each row.

    cols : ndarray of shape (n_clusters, X.shape[1])
        The indicators for cluster membership of each column.

    See Also
    --------
    make_checkerboard: Generate an array with block checkerboard structure for
        biclustering.

    References
    ----------

    .. [1] Dhillon, I. S. (2001, August). Co-clustering documents and
        words using bipartite spectral graph partitioning. In Proceedings
        of the seventh ACM SIGKDD international conference on Knowledge
        discovery and data mining (pp. 269-274). ACM.

    """

    X, rows,cols = make_biclusters(
        shape=shape,
        n_clusters=n_clusters,
        noise=noise,
        minval=minval,
        maxval=maxval,
        shuffle=shuffle,
        random_state=random_state,
    )


    return X, rows,cols


@NodeDecorator(
    node_id = "sklearn.datasets.make_blobs",
    name="make_blobs",
    outputs=[
        {"name": "X"},
        {"name": "y"},
        {"name": "center"},
    ],
)
def _blobs(
    n_samples: Union[int, np.ndarray] = 100,
    n_features: int = 2,
    centers: Optional[Union[int, np.ndarray]] = None,
    cluster_std: Union[float, np.ndarray] = 1.0,
    center_box: Union[tuple[float, float]] = (-10.0, 10.0),
    shuffle: bool = True,
    random_state: Optional[Union[int, RandomState]] = None,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Generate isotropic Gaussian blobs for clustering.

    For an example of usage, see
    :ref:`sphx_glr_auto_examples_datasets_plot_random_dataset.py`.

    Read more in the :ref:`User Guide <sample_generators>`.

    Parameters
    ----------
    n_samples : int or array-like, default=100
        If int, it is the total number of points equally divided among
        clusters.
        If array-like, each element of the sequence indicates
        the number of samples per cluster.

        .. versionchanged:: v0.20
            one can now pass an array-like to the ``n_samples`` parameter

    n_features : int, default=2
        The number of features for each sample.

    centers : int or array-like of shape (n_centers, n_features), default=None
        The number of centers to generate, or the fixed center locations.
        If n_samples is an int and centers is None, 3 centers are generated.
        If n_samples is array-like, centers must be
        either None or an array of length equal to the length of n_samples.

    cluster_std : float or array-like of float, default=1.0
        The standard deviation of the clusters.

    center_box : tuple of float (min, max), default=(-10.0, 10.0)
        The bounding box for each cluster center when centers are
        generated at random.

    shuffle : bool, default=True
        Shuffle the samples.

    random_state : int, RandomState instance or None, default=None
        Determines random number generation for dataset creation. Pass an int
        for reproducible output across multiple function calls.
        See :term:`Glossary <random_state>`.


    Returns
    -------
    X : ndarray of shape (n_samples, n_features)
        The generated samples.

    y : ndarray of shape (n_samples,)
        The integer labels for cluster membership of each sample.

    centers : ndarray of shape (n_centers, n_features)
        The centers of each cluster.

    See Also
    --------
    make_classification : A more intricate variant.

    Examples
    --------
    >>> from sklearn.datasets import make_blobs
    >>> X, y = make_blobs(n_samples=10, centers=3, n_features=2,
    ...                   random_state=0)
    >>> print(X.shape)
    (10, 2)
    >>> y
    array([0, 0, 1, 0, 2, 2, 2, 1, 1, 0])
    >>> X, y = make_blobs(n_samples=[3, 3, 4], centers=None, n_features=2,
    ...                   random_state=0)
    >>> print(X.shape)
    (10, 2)
    >>> y
    array([0, 1, 2, 0, 2, 2, 2, 1, 1, 0])

    """

    X, y, center = make_blobs(
        n_samples=n_samples,
        n_features=n_features,
        centers=centers,
        cluster_std=cluster_std,
        center_box=center_box,
        shuffle=shuffle,
        random_state=random_state,
        return_centers=True,
    )

    return X, y,center


@NodeDecorator(
    node_id = "sklearn.datasets.make_checkerboard",
    name="make_checkerboard",
    outputs=[
        {"name": "X"},
        {"name": "rows"},
        {"name": "cols"},
    ],
)
def _checkerboard(
    shape: Tuple[int, int],
    n_clusters: Union[int, np.ndarray, Tuple[int, int]],
    noise: float = 0.0,
    minval: float = 10,
    maxval: float = 100,
    shuffle: bool = True,
    random_state: Optional[Union[int, RandomState]] = None,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Generate an array with block checkerboard structure for biclustering.

    Read more in the :ref:`User Guide <sample_generators>`.

    Parameters
    ----------
    shape : tuple of shape (n_rows, n_cols)
        The shape of the result.

    n_clusters : int or array-like or shape (n_row_clusters, n_column_clusters)
        The number of row and column clusters.

    noise : float, default=0.0
        The standard deviation of the gaussian noise.

    minval : float, default=10
        Minimum value of a bicluster.

    maxval : float, default=100
        Maximum value of a bicluster.

    shuffle : bool, default=True
        Shuffle the samples.

    random_state : int, RandomState instance or None, default=None
        Determines random number generation for dataset creation. Pass an int
        for reproducible output across multiple function calls.
        See :term:`Glossary <random_state>`.

    Returns
    -------
    X : ndarray of shape `shape`
        The generated array.

    rows : ndarray of shape (n_clusters, X.shape[0])
        The indicators for cluster membership of each row.

    cols : ndarray of shape (n_clusters, X.shape[1])
        The indicators for cluster membership of each column.

    See Also
    --------
    make_biclusters : Generate an array with constant block diagonal structure
        for biclustering.

    References
    ----------
    .. [1] Kluger, Y., Basri, R., Chang, J. T., & Gerstein, M. (2003).
        Spectral biclustering of microarray data: coclustering genes
        and conditions. Genome research, 13(4), 703-716.

    """

    X, rows,cols = make_checkerboard(
        shape=shape,
        n_clusters=n_clusters,
        noise=noise,
        minval=minval,
        maxval=maxval,
        shuffle=shuffle,
        random_state=random_state,
    )


    return X, rows,cols


@NodeDecorator(
    node_id = "sklearn.datasets.make_circles",
    name="make_circles",
    outputs=[
        {"name": "X"},
        {"name": "y"},
    ],
)
def _circles(
    n_samples: Union[int, Tuple[int, int]] = 100,
    shuffle: bool = True,
    noise: Optional[float] = None,
    random_state: Optional[Union[int, RandomState]] = None,
    factor: float = 0.8,
) -> Tuple[np.ndarray, np.ndarray]:
    """Make a large circle containing a smaller circle in 2d.

    A simple toy dataset to visualize clustering and classification
    algorithms.

    Read more in the :ref:`User Guide <sample_generators>`.

    Parameters
    ----------
    n_samples : int or tuple of shape (2,), dtype=int, default=100
        If int, it is the total number of points generated.
        For odd numbers, the inner circle will have one point more than the
        outer circle.
        If two-element tuple, number of points in outer circle and inner
        circle.

        .. versionchanged:: 0.23
           Added two-element tuple.

    shuffle : bool, default=True
        Whether to shuffle the samples.

    noise : float, default=None
        Standard deviation of Gaussian noise added to the data.

    random_state : int, RandomState instance or None, default=None
        Determines random number generation for dataset shuffling and noise.
        Pass an int for reproducible output across multiple function calls.
        See :term:`Glossary <random_state>`.

    factor : float, default=.8
        Scale factor between inner and outer circle in the range `[0, 1)`.

    Returns
    -------
    X : ndarray of shape (n_samples, 2)
        The generated samples.

    y : ndarray of shape (n_samples,)
        The integer labels (0 or 1) for class membership of each sample.

    Examples
    --------
    >>> from sklearn.datasets import make_circles
    >>> X, y = make_circles(random_state=42)
    >>> X.shape
    (100, 2)
    >>> y.shape
    (100,)
    >>> list(y[:5])
    [1, 1, 1, 0, 0]

    """

    X, y = make_circles(
        n_samples=n_samples,
        shuffle=shuffle,
        noise=noise,
        random_state=random_state,
        factor=factor,
    )

    return X, y


@NodeDecorator(
    node_id = "sklearn.datasets.make_classification",
    name="make_classification",
    outputs=[
        {"name": "X"},
        {"name": "y"},
    ],
)
def _classification(
    n_samples: int = 100,
    n_features: int = 20,
    n_informative: int = 2,
    n_redundant: int = 2,
    n_repeated: int = 0,
    n_classes: int = 2,
    n_clusters_per_class: int = 2,
    weights: Optional[np.ndarray] = None,
    flip_y: float = 0.01,
    class_sep: float = 0.75,
    hypercube: bool = True,
    shift: Optional[Union[float, np.ndarray, None]] = 0.0,
    scale: Optional[Union[float, np.ndarray, None]] = 1.0,
    shuffle: bool = True,
    random_state: Optional[Union[int, RandomState]] = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """Generate a random n-class classification problem.

    This initially creates clusters of points normally distributed (std=1)
    about vertices of an ``n_informative``-dimensional hypercube with sides of
    length ``2*class_sep`` and assigns an equal number of clusters to each
    class. It introduces interdependence between these features and adds
    various types of further noise to the data.

    Without shuffling, ``X`` horizontally stacks features in the following
    order: the primary ``n_informative`` features, followed by ``n_redundant``
    linear combinations of the informative features, followed by ``n_repeated``
    duplicates, drawn randomly with replacement from the informative and
    redundant features. The remaining features are filled with random noise.
    Thus, without shuffling, all useful features are contained in the columns
    ``X[:, :n_informative + n_redundant + n_repeated]``.

    For an example of usage, see
    :ref:`sphx_glr_auto_examples_datasets_plot_random_dataset.py`.

    Read more in the :ref:`User Guide <sample_generators>`.

    Parameters
    ----------
    n_samples : int, default=100
        The number of samples.

    n_features : int, default=20
        The total number of features. These comprise ``n_informative``
        informative features, ``n_redundant`` redundant features,
        ``n_repeated`` duplicated features and
        ``n_features-n_informative-n_redundant-n_repeated`` useless features
        drawn at random.

    n_informative : int, default=2
        The number of informative features. Each class is composed of a number
        of gaussian clusters each located around the vertices of a hypercube
        in a subspace of dimension ``n_informative``. For each cluster,
        informative features are drawn independently from  N(0, 1) and then
        randomly linearly combined within each cluster in order to add
        covariance. The clusters are then placed on the vertices of the
        hypercube.

    n_redundant : int, default=2
        The number of redundant features. These features are generated as
        random linear combinations of the informative features.

    n_repeated : int, default=0
        The number of duplicated features, drawn randomly from the informative
        and the redundant features.

    n_classes : int, default=2
        The number of classes (or labels) of the classification problem.

    n_clusters_per_class : int, default=2
        The number of clusters per class.

    weights : array-like of shape (n_classes,) or (n_classes - 1,),\
              default=None
        The proportions of samples assigned to each class. If None, then
        classes are balanced. Note that if ``len(weights) == n_classes - 1``,
        then the last class weight is automatically inferred.
        More than ``n_samples`` samples may be returned if the sum of
        ``weights`` exceeds 1. Note that the actual class proportions will
        not exactly match ``weights`` when ``flip_y`` isn't 0.

    flip_y : float, default=0.01
        The fraction of samples whose class is assigned randomly. Larger
        values introduce noise in the labels and make the classification
        task harder. Note that the default setting flip_y > 0 might lead
        to less than ``n_classes`` in y in some cases.

    class_sep : float, default=1.0
        The factor multiplying the hypercube size.  Larger values spread
        out the clusters/classes and make the classification task easier.

    hypercube : bool, default=True
        If True, the clusters are put on the vertices of a hypercube. If
        False, the clusters are put on the vertices of a random polytope.

    shift : float, ndarray of shape (n_features,) or None, default=0.0
        Shift features by the specified value. If None, then features
        are shifted by a random value drawn in [-class_sep, class_sep].

    scale : float, ndarray of shape (n_features,) or None, default=1.0
        Multiply features by the specified value. If None, then features
        are scaled by a random value drawn in [1, 100]. Note that scaling
        happens after shifting.

    shuffle : bool, default=True
        Shuffle the samples and the features.

    random_state : int, RandomState instance or None, default=None
        Determines random number generation for dataset creation. Pass an int
        for reproducible output across multiple function calls.
        See :term:`Glossary <random_state>`.

    Returns
    -------
    X : ndarray of shape (n_samples, n_features)
        The generated samples.

    y : ndarray of shape (n_samples,)
        The integer labels for class membership of each sample.

    See Also
    --------
    make_blobs : Simplified variant.
    make_multilabel_classification : Unrelated generator for multilabel tasks.

    Notes
    -----
    The algorithm is adapted from Guyon [1] and was designed to generate
    the "Madelon" dataset.

    References
    ----------
    .. [1] I. Guyon, "Design of experiments for the NIPS 2003 variable
           selection benchmark", 2003.

    Examples
    --------
    >>> from sklearn.datasets import make_classification
    >>> X, y = make_classification(random_state=42)
    >>> X.shape
    (100, 20)
    >>> y.shape
    (100,)
    >>> list(y[:5])
    [0, 0, 1, 1, 0]

    """

    X, y = make_classification(
        n_samples=n_samples,
        n_features=n_features,
        n_informative=n_informative,
        n_redundant=n_redundant,
        n_repeated=n_repeated,
        n_classes=n_classes,
        n_clusters_per_class=n_clusters_per_class,
        weights=weights,
        flip_y=flip_y,
        class_sep=class_sep,
        hypercube=hypercube,
        shift=shift,
        scale=scale,
        shuffle=shuffle,
        random_state=random_state,
    )


    return X, y


@NodeDecorator(
    node_id = "sklearn.datasets.make_friedman1",
    name="make_friedman1",
    outputs=[
        {"name": "X"},
        {"name": "y"},
    ],
)
def _friedman1(
    n_samples: int = 100,
    n_features: int = 10,
    noise: float = 0.0,
    random_state: Optional[Union[int, RandomState]] = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """Generate the "Friedman #1" regression problem.

    This dataset is described in Friedman [1] and Breiman [2].

    Inputs `X` are independent features uniformly distributed on the interval
    [0, 1]. The output `y` is created according to the formula::

        y(X) = 10 * sin(pi * X[:, 0] * X[:, 1]) + 20 * (X[:, 2] - 0.5) ** 2 \
+ 10 * X[:, 3] + 5 * X[:, 4] + noise * N(0, 1).

    Out of the `n_features` features, only 5 are actually used to compute
    `y`. The remaining features are independent of `y`.

    The number of features has to be >= 5.

    Read more in the :ref:`User Guide <sample_generators>`.

    Parameters
    ----------
    n_samples : int, default=100
        The number of samples.

    n_features : int, default=10
        The number of features. Should be at least 5.

    noise : float, default=0.0
        The standard deviation of the gaussian noise applied to the output.

    random_state : int, RandomState instance or None, default=None
        Determines random number generation for dataset noise. Pass an int
        for reproducible output across multiple function calls.
        See :term:`Glossary <random_state>`.

    Returns
    -------
    X : ndarray of shape (n_samples, n_features)
        The input samples.

    y : ndarray of shape (n_samples,)
        The output values.

    References
    ----------
    .. [1] J. Friedman, "Multivariate adaptive regression splines", The Annals
           of Statistics 19 (1), pages 1-67, 1991.

    .. [2] L. Breiman, "Bagging predictors", Machine Learning 24,
           pages 123-140, 1996.

    Examples
    --------
    >>> from sklearn.datasets import make_friedman1
    >>> X, y = make_friedman1(random_state=42)
    >>> X.shape
    (100, 10)
    >>> y.shape
    (100,)
    >>> list(y[:3])
    [16.8..., 5.8..., 9.4...]

    """

    X, y = make_friedman1(
        n_samples=n_samples,
        n_features=n_features,
        noise=noise,
        random_state=random_state,
    )


    return X, y



@NodeDecorator(
    node_id = "sklearn.datasets.make_friedman2",
    name="make_friedman2",
    outputs=[
        {"name": "X"},
        {"name": "y"},
    ],
)
def _friedman2(
    n_samples: int = 100,
    noise: float = 0.0,
    random_state: Optional[Union[int, RandomState]] = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """Generate the "Friedman #2" regression problem.

    This dataset is described in Friedman [1] and Breiman [2].

    Inputs `X` are 4 independent features uniformly distributed on the
    intervals::

        0 <= X[:, 0] <= 100,
        40 * pi <= X[:, 1] <= 560 * pi,
        0 <= X[:, 2] <= 1,
        1 <= X[:, 3] <= 11.

    The output `y` is created according to the formula::

        y(X) = (X[:, 0] ** 2 + (X[:, 1] * X[:, 2] \
 - 1 / (X[:, 1] * X[:, 3])) ** 2) ** 0.5 + noise * N(0, 1).

    Read more in the :ref:`User Guide <sample_generators>`.

    Parameters
    ----------
    n_samples : int, default=100
        The number of samples.

    noise : float, default=0.0
        The standard deviation of the gaussian noise applied to the output.

    random_state : int, RandomState instance or None, default=None
        Determines random number generation for dataset noise. Pass an int
        for reproducible output across multiple function calls.
        See :term:`Glossary <random_state>`.

    Returns
    -------
    X : ndarray of shape (n_samples, 4)
        The input samples.

    y : ndarray of shape (n_samples,)
        The output values.

    References
    ----------
    .. [1] J. Friedman, "Multivariate adaptive regression splines", The Annals
           of Statistics 19 (1), pages 1-67, 1991.

    .. [2] L. Breiman, "Bagging predictors", Machine Learning 24,
           pages 123-140, 1996.

    Examples
    --------
    >>> from sklearn.datasets import make_friedman2
    >>> X, y = make_friedman2(random_state=42)
    >>> X.shape
    (100, 4)
    >>> y.shape
    (100,)
    >>> list(y[:3])
    [1229.4..., 27.0..., 65.6...]]

    """

    X, y = make_friedman2(
        n_samples=n_samples,
        noise=noise,
        random_state=random_state,
    )

    return X, y


@NodeDecorator(
    node_id = "sklearn.datasets.make_friedman3",
    name="make_friedman3",
    outputs=[
        {"name": "X"},
        {"name": "y"},
    ],
)
def _friedman3(
    n_samples: int = 100,
    noise: float = 0.0,
    random_state: Optional[Union[int, RandomState]] = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """Generate the "Friedman #3" regression problem.

    This dataset is described in Friedman [1] and Breiman [2].

    Inputs `X` are 4 independent features uniformly distributed on the
    intervals::

        0 <= X[:, 0] <= 100,
        40 * pi <= X[:, 1] <= 560 * pi,
        0 <= X[:, 2] <= 1,
        1 <= X[:, 3] <= 11.

    The output `y` is created according to the formula::

        y(X) = arctan((X[:, 1] * X[:, 2] - 1 / (X[:, 1] * X[:, 3])) \
/ X[:, 0]) + noise * N(0, 1).

    Read more in the :ref:`User Guide <sample_generators>`.

    Parameters
    ----------
    n_samples : int, default=100
        The number of samples.

    noise : float, default=0.0
        The standard deviation of the gaussian noise applied to the output.

    random_state : int, RandomState instance or None, default=None
        Determines random number generation for dataset noise. Pass an int
        for reproducible output across multiple function calls.
        See :term:`Glossary <random_state>`.

    Returns
    -------
    X : ndarray of shape (n_samples, 4)
        The input samples.

    y : ndarray of shape (n_samples,)
        The output values.

    References
    ----------
    .. [1] J. Friedman, "Multivariate adaptive regression splines", The Annals
           of Statistics 19 (1), pages 1-67, 1991.

    .. [2] L. Breiman, "Bagging predictors", Machine Learning 24,
           pages 123-140, 1996.

    Examples
    --------
    >>> from sklearn.datasets import make_friedman3
    >>> X, y = make_friedman3(random_state=42)
    >>> X.shape
    (100, 4)
    >>> y.shape
    (100,)
    >>> list(y[:3])
    [1.5..., 0.9..., 0.4...]

    """

    X, y = make_friedman3(
        n_samples=n_samples,
        noise=noise,
        random_state=random_state,
    )

    return X, y



@NodeDecorator(
    node_id = "sklearn.datasets.make_gaussian_quantiles",
    name="make_gaussian_quantiles",
    outputs=[
        {"name": "X"},
        {"name": "y"},
    ],
)
def _gaussian_quantiles(
    mean: Optional[np.ndarray] = None,
    cov: float = 1.0,
    n_samples: int = 100,
    n_features: int = 2,
    n_classes: int = 3,
    shuffle: bool = True,
    random_state: Optional[Union[int, RandomState]] = None,
) -> Tuple[np.ndarray, np.ndarray]:
    r"""Generate isotropic Gaussian and label samples by quantile.

    This classification dataset is constructed by taking a multi-dimensional
    standard normal distribution and defining classes separated by nested
    concentric multi-dimensional spheres such that roughly equal numbers of
    samples are in each class (quantiles of the :math:`\chi^2` distribution).

    For an example of usage, see
    :ref:`sphx_glr_auto_examples_datasets_plot_random_dataset.py`.

    Read more in the :ref:`User Guide <sample_generators>`.

    Parameters
    ----------
    mean : array-like of shape (n_features,), default=None
        The mean of the multi-dimensional normal distribution.
        If None then use the origin (0, 0, ...).

    cov : float, default=1.0
        The covariance matrix will be this value times the unit matrix. This
        dataset only produces symmetric normal distributions.

    n_samples : int, default=100
        The total number of points equally divided among classes.

    n_features : int, default=2
        The number of features for each sample.

    n_classes : int, default=3
        The number of classes.

    shuffle : bool, default=True
        Shuffle the samples.

    random_state : int, RandomState instance or None, default=None
        Determines random number generation for dataset creation. Pass an int
        for reproducible output across multiple function calls.
        See :term:`Glossary <random_state>`.

    Returns
    -------
    X : ndarray of shape (n_samples, n_features)
        The generated samples.

    y : ndarray of shape (n_samples,)
        The integer labels for quantile membership of each sample.

    Notes
    -----
    The dataset is from Zhu et al [1].

    References
    ----------
    .. [1] J. Zhu, H. Zou, S. Rosset, T. Hastie, "Multi-class AdaBoost", 2009.

    Examples
    --------
    >>> from sklearn.datasets import make_gaussian_quantiles
    >>> X, y = make_gaussian_quantiles(random_state=42)
    >>> X.shape
    (100, 2)
    >>> y.shape
    (100,)
    >>> list(y[:5])
    [2, 0, 1, 0, 2]

    """

    X, y = make_gaussian_quantiles(
        mean=mean,
        cov=cov,
        n_samples=n_samples,
        n_features=n_features,
        n_classes=n_classes,
        shuffle=shuffle,
        random_state=random_state,
    )


    return X, y


@NodeDecorator(
    node_id = "sklearn.datasets.make_hastie_10_2",
    name="make_hastie_10_2",
    outputs=[
        {"name": "X"},
        {"name": "y"},
    ],
)
def _hastie_10_2(
    n_samples: int = 100,
    random_state: Optional[Union[int, RandomState]] = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """Generate data for binary classification used in Hastie et al. 2009, Example 10.2.

    The ten features are standard independent Gaussian and
    the target ``y`` is defined by::

      y[i] = 1 if np.sum(X[i] ** 2) > 9.34 else -1

    Read more in the :ref:`User Guide <sample_generators>`.

    Parameters
    ----------
    n_samples : int, default=12000
        The number of samples.

    random_state : int, RandomState instance or None, default=None
        Determines random number generation for dataset creation. Pass an int
        for reproducible output across multiple function calls.
        See :term:`Glossary <random_state>`.

    Returns
    -------
    X : ndarray of shape (n_samples, 10)
        The input samples.

    y : ndarray of shape (n_samples,)
        The output values.

    See Also
    --------
    make_gaussian_quantiles : A generalization of this dataset approach.

    References
    ----------
    .. [1] T. Hastie, R. Tibshirani and J. Friedman, "Elements of Statistical
           Learning Ed. 2", Springer, 2009.
    """

    X, y = make_hastie_10_2(
        n_samples=n_samples,
        random_state=random_state,
    )


    return X, y


@NodeDecorator(
    node_id = "sklearn.datasets.make_low_rank_matrix",
    name="make_low_rank_matrix",
    outputs=[
        {"name": "X"},
    ],
)
def _low_rank_matrix(
    n_samples: int = 100,
    n_features: int = 100,
    effective_rank: int = 10,
    tail_strength: float = 0.5,
    random_state: Optional[Union[int, RandomState]] = None,
) -> np.ndarray:
    """Generate a mostly low rank matrix with bell-shaped singular values.

    Most of the variance can be explained by a bell-shaped curve of width
    effective_rank: the low rank part of the singular values profile is::

        (1 - tail_strength) * exp(-1.0 * (i / effective_rank) ** 2)

    The remaining singular values' tail is fat, decreasing as::

        tail_strength * exp(-0.1 * i / effective_rank).

    The low rank part of the profile can be considered the structured
    signal part of the data while the tail can be considered the noisy
    part of the data that cannot be summarized by a low number of linear
    components (singular vectors).

    This kind of singular profiles is often seen in practice, for instance:
     - gray level pictures of faces
     - TF-IDF vectors of text documents crawled from the web

    Read more in the :ref:`User Guide <sample_generators>`.

    Parameters
    ----------
    n_samples : int, default=100
        The number of samples.

    n_features : int, default=100
        The number of features.

    effective_rank : int, default=10
        The approximate number of singular vectors required to explain most of
        the data by linear combinations.

    tail_strength : float, default=0.5
        The relative importance of the fat noisy tail of the singular values
        profile. The value should be between 0 and 1.

    random_state : int, RandomState instance or None, default=None
        Determines random number generation for dataset creation. Pass an int
        for reproducible output across multiple function calls.
        See :term:`Glossary <random_state>`.

    Returns
    -------
    X : ndarray of shape (n_samples, n_features)
        The matrix

    """

    X = make_low_rank_matrix(
        n_samples=n_samples,
        n_features=n_features,
        effective_rank=effective_rank,
        tail_strength=tail_strength,
        random_state=random_state,
    )
    return X


@NodeDecorator(
    node_id = "sklearn.datasets.make_moons",
    name="make_moons",
    outputs=[
        {"name": "X"},
        {"name": "y"},
    ],
)
def _moons(
    n_samples: Union[int, Tuple[int, int]] = 100,
    shuffle: bool = True,
    noise: Optional[float] = None,
    random_state: Optional[Union[int, RandomState]] = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """Make two interleaving half circles.

    A simple toy dataset to visualize clustering and classification
    algorithms. Read more in the :ref:`User Guide <sample_generators>`.

    Parameters
    ----------
    n_samples : int or tuple of shape (2,), dtype=int, default=100
        If int, the total number of points generated.
        If two-element tuple, number of points in each of two moons.

        .. versionchanged:: 0.23
           Added two-element tuple.

    shuffle : bool, default=True
        Whether to shuffle the samples.

    noise : float, default=None
        Standard deviation of Gaussian noise added to the data.

    random_state : int, RandomState instance or None, default=None
        Determines random number generation for dataset shuffling and noise.
        Pass an int for reproducible output across multiple function calls.
        See :term:`Glossary <random_state>`.

    Returns
    -------
    X : ndarray of shape (n_samples, 2)
        The generated samples.

    y : ndarray of shape (n_samples,)
        The integer labels (0 or 1) for class membership of each sample.

    """

    X, y = make_moons(
        n_samples=n_samples,
        shuffle=shuffle,
        noise=noise,
        random_state=random_state,
    )


    return X, y


class ReturnIndicator(Enum):
    dense = "dense"
    sparse = "sparse"
    false = False

    @classmethod
    def default(cls):
        return cls.dense.value


@NodeDecorator(
    node_id = "sklearn.datasets.make_multilabel_classification",
    name="make_multilabel_classification",
    outputs=[
        {"name": "X"},
        {"name": "Y"},
        {"name": "p_c"},
        {"name": "p_w_c"},
    ],
)
def _multilabel_classification(
    n_samples: int = 100,
    n_features: int = 20,
    n_classes: int = 5,
    n_labels: int = 2,
    length: int = 50,
    allow_unlabeled: bool = True,
    sparse: bool = False,
    return_indicator: Union[ReturnIndicator, bool] = ReturnIndicator.default(),
    random_state: Optional[Union[int, RandomState]] = None,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Generate a random multilabel classification problem.

    For each sample, the generative process is:
        - pick the number of labels: n ~ Poisson(n_labels)
        - n times, choose a class c: c ~ Multinomial(theta)
        - pick the document length: k ~ Poisson(length)
        - k times, choose a word: w ~ Multinomial(theta_c)

    In the above process, rejection sampling is used to make sure that
    n is never zero or more than `n_classes`, and that the document length
    is never zero. Likewise, we reject classes which have already been chosen.

    For an example of usage, see
    :ref:`sphx_glr_auto_examples_datasets_plot_random_multilabel_dataset.py`.

    Read more in the :ref:`User Guide <sample_generators>`.

    Parameters
    ----------
    n_samples : int, default=100
        The number of samples.

    n_features : int, default=20
        The total number of features.

    n_classes : int, default=5
        The number of classes of the classification problem.

    n_labels : int, default=2
        The average number of labels per instance. More precisely, the number
        of labels per sample is drawn from a Poisson distribution with
        ``n_labels`` as its expected value, but samples are bounded (using
        rejection sampling) by ``n_classes``, and must be nonzero if
        ``allow_unlabeled`` is False.

    length : int, default=50
        The sum of the features (number of words if documents) is drawn from
        a Poisson distribution with this expected value.

    allow_unlabeled : bool, default=True
        If ``True``, some instances might not belong to any class.

    sparse : bool, default=False
        If ``True``, return a sparse feature matrix.

        .. versionadded:: 0.17
           parameter to allow *sparse* output.

    return_indicator : {'dense', 'sparse'} or False, default='dense'
        If ``'dense'`` return ``Y`` in the dense binary indicator format. If
        ``'sparse'`` return ``Y`` in the sparse binary indicator format.
        ``False`` returns a list of lists of labels.



    random_state : int, RandomState instance or None, default=None
        Determines random number generation for dataset creation. Pass an int
        for reproducible output across multiple function calls.
        See :term:`Glossary <random_state>`.

    Returns
    -------
    X : ndarray of shape (n_samples, n_features)
        The generated samples.

    Y : {ndarray, sparse matrix} of shape (n_samples, n_classes)
        The label sets. Sparse matrix should be of CSR format.

    p_c : ndarray of shape (n_classes,)
        The probability of each class being drawn. 

    p_w_c : ndarray of shape (n_features, n_classes)
        The probability of each feature being drawn given each class.

    Examples
    --------
    >>> from sklearn.datasets import make_multilabel_classification
    >>> X, y = make_multilabel_classification(n_labels=3, random_state=42)
    >>> X.shape
    (100, 20)
    >>> y.shape
    (100, 5)
    >>> list(y[:3])
    [array([1, 1, 0, 1, 0]), array([0, 1, 1, 1, 0]), array([0, 1, 0, 0, 0])]


    """

    X, Y, p_c, p_w_c = make_multilabel_classification(
        n_samples=n_samples,
        n_features=n_features,
        n_classes=n_classes,
        n_labels=n_labels,
        length=length,
        allow_unlabeled=allow_unlabeled,
        sparse=sparse,
        return_indicator=return_indicator,
        return_distributions=True,
        random_state=random_state,
    )


    return X, Y, p_c, p_w_c


@NodeDecorator(
    node_id="sklearn.datasets.make_regression",
    name="make_regression",
    outputs=[
        {"name": "X"},
        {"name": "y"},
        {"name": "coefs"},
    ],
)

@controlled_wrapper(make_regression, wrapper_attribute="__fnwrapped__")
def _regression(
    n_samples: int = 100,
    n_features: int = 100,
    n_informative: int = 10,
    n_targets: int = 1,
    bias: float = 0.0,
    effective_rank: Optional[int] = None,
    tail_strength: float = 0.5,
    noise: float = 0.0,
    shuffle: bool = True,
    coef: bool = True,
    random_state: Optional[Union[int, RandomState]] = None,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    X, y, coefs = make_regression(
        n_samples=n_samples,
        n_features=n_features,
        n_informative=n_informative,
        n_targets=n_targets,
        bias=bias,
        effective_rank=effective_rank,
        tail_strength=tail_strength,
        noise=noise,
        shuffle=shuffle,
        coef=coef,
        random_state=random_state,
    )

    return X, y, coefs


@NodeDecorator(
    node_id="sklearn.datasets.make_s_curve",
    name="make_s_curve",
    outputs=[
        {"name": "X"},
        {"name": "t"},
    ],
)

@controlled_wrapper(make_s_curve, wrapper_attribute="__fnwrapped__")
def _s_curve(
    n_samples: int = 100,
    noise: float = 0.0,
    random_state: Optional[Union[int, RandomState]] = None,
) -> Tuple[np.ndarray, np.ndarray]:
    X, t = make_s_curve(
        n_samples=n_samples,
        noise=noise,
        random_state=random_state,
    )


    return X, t
@NodeDecorator(
    node_id="sklearn.datasets.make_sparse_coded_signal",
    name="make_sparse_coded_signal",
    outputs=[
        {"name": "data"},
        {"name": "dictionary"},
        {"name": "code"},
        
    ],
)

@controlled_wrapper(make_sparse_coded_signal, wrapper_attribute="__fnwrapped__")
def _sparse_coded_signal(
    n_samples: int,
    n_components: int,
    n_features: int,
    n_nonzero_coefs: int,
    random_state: Optional[Union[int, RandomState]] = None,
    data_transposed: bool = False,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    data, dictionary, code = make_sparse_coded_signal(
        n_samples=n_samples,
        n_components=n_components,
        n_features=n_features,
        n_nonzero_coefs=n_nonzero_coefs,
        data_transposed=data_transposed,
        random_state=random_state,
    )

    

    return data, dictionary, code
class SparseFormat(Enum):
    bsr ='bsr'
    csr ='csr'
    dok = 'dok'
    coo = 'coo'
    lil = 'lil'
    dia = 'dia'
    csc = 'csc'
    NONE = None
    
    @classmethod
    def default(cls):
        return cls.NONE.value
@NodeDecorator(
    node_id="sklearn.datasets.make_sparse_spd_matrix",
    name="make_sparse_spd_matrix",
    outputs=[
        {"name": "prec"},
    ],
)

@controlled_wrapper(make_sparse_spd_matrix, wrapper_attribute="__fnwrapped__")
def _sparse_spd_matrix(
    n_dim: int=1,
    alpha: float=0.95,
    norm_diag: bool=False,
    smallest_coef: float=0.1,
    largest_coef: float=0.9,
    sparse_format: SparseFormat=SparseFormat.default(),
    random_state: Optional[Union[int, RandomState]] = None,
) -> np.ndarray:
    prec = make_sparse_spd_matrix(
        n_dim=n_dim,
        alpha=alpha,
        norm_diag=norm_diag,
        smallest_coef=smallest_coef,
        largest_coef=largest_coef,
        sparse_format=sparse_format,
        random_state=random_state,
    )
    return prec

@NodeDecorator(
    node_id="sklearn.datasets.make_sparse_uncorrelated",
    name="make_sparse_uncorrelated",
    outputs=[
        {"name": "X"},
        {"name": "y"},
    ],
)

@controlled_wrapper(make_sparse_uncorrelated, wrapper_attribute="__fnwrapped__")
def _sparse_uncorrelated(
    n_samples: int = 100,
    n_features:int =10,
    random_state: Optional[Union[int, RandomState]] = None,
) -> Tuple[np.ndarray, np.ndarray]:
    X, y = make_sparse_uncorrelated(
        n_samples=n_samples,
        n_features=n_features,
        random_state=random_state,
    )

    return X, y

@NodeDecorator(
    node_id="sklearn.datasets.make_spd_matrix",
    name="make_spd_matrix",
    outputs=[
        {"name": "X"},
    ],
)

@controlled_wrapper(make_spd_matrix, wrapper_attribute="__fnwrapped__")
def _spd_matrix(
    n_dim: int,
    random_state: Optional[Union[int, RandomState]] = None,
) -> np.ndarray:
    X = make_spd_matrix(
        n_dim=n_dim,
        random_state=random_state,
    )

    return X

@NodeDecorator(
    node_id="sklearn.datasets.make_swiss_roll",
    name="make_swiss_roll",
    outputs=[
        {"name": "X"},
        {"name": "t"},
    ],
)

@controlled_wrapper(make_swiss_roll, wrapper_attribute="__fnwrapped__")
def _swiss_roll(
    n_samples: int = 100,
    noise:float =0.0,
    random_state: Optional[Union[int, RandomState]] = None,
    hole: bool = False,
) -> Tuple[np.ndarray, np.ndarray]:
    X, t = make_swiss_roll(
        n_samples=n_samples,
        noise=noise,
        random_state=random_state,
        hole=hole,
    )

    return X, t
SAMPLE_GENERATOR_NODE_SHELF = Shelf(
    nodes=[
        _biclusters,
        _blobs,
        _checkerboard,
        _circles,
        _classification,
        _friedman1,
        _friedman2,
        _friedman3,
        _gaussian_quantiles,
        _hastie_10_2,
        _low_rank_matrix,
        _moons,
        _multilabel_classification,
        _regression,
        _s_curve,
        _sparse_coded_signal,
        _sparse_spd_matrix,
        _sparse_uncorrelated,
        _spd_matrix,
        _swiss_roll
    ],
    subshelves=[],
    name="Samples generator",
    description="The sklearn.datasets package embeds some small toy datasets as introduced in the Getting Started section. This package also features helpers to fetch larger datasets commonly used by the machine learning community to benchmark algorithms on data that comes from the ‘real world’. To evaluate the impact of the scale of the dataset (n_samples and n_features) while controlling the statistical properties of the data (typically the correlation and informativeness of the features), it is also possible to generate synthetic data.",
)

DATASET_NODE_SHELF = Shelf(
    nodes=[],
    subshelves=[LOADERS_NODE_SHELF, SAMPLE_GENERATOR_NODE_SHELF],
    name="Datasets",
    description="The sklearn.datasets module includes utilities to load datasets, including methods to load and fetch popular reference datasets. It also features some artificial data generators.",
)
