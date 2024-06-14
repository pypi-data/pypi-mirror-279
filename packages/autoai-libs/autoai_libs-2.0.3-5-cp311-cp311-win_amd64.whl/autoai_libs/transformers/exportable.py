################################################################################
# IBM Confidential
# OCO Source Materials
# 5737-H76, 5725-W78, 5900-A1R, 5737-L65
# (c) Copyright IBM Corp. 2019-2024. All Rights Reserved.
# The source code for this program is not published or otherwise divested of its trade secrets,
# irrespective of what has been deposited with the U.S. Copyright Office.
################################################################################

import logging
import warnings
from time import time

import numpy as np
import sklearn
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.utils.validation import check_array

from autoai_libs.utils.exportable_utils import (
    compress_str_column,
    convert_float32,
    global_missing_values_reference_list,
    numpy_boolean2float,
    numpy_floatstr2float,
    numpy_permute_array,
    numpy_replace_values,
    numpy_select_columns,
    numpy_whatis,
    setValueOrDefault,
)

sklearn_version_list = sklearn.__version__.split(".")
global_sklearn_version_family = sklearn_version_list[1]
if sklearn_version_list[0] == "1":
    global_sklearn_version_family = sklearn_version_list[0]

debug_transform_return = False
debug = False
debug_timings = False
debug_catnum = False

debug_date_transformer = False

logger = logging.getLogger("autoai_libs")


class ColumnSelector(BaseEstimator, TransformerMixin):
    """
    Selects a subset of columns for a given numpy array or subset of elements of a list
    """

    def __init__(self, columns_indices_list, activate_flag=True):
        """

        :param columns_indices_list: list of indices to select numpy columns or list elements
        :param activate_flag: determines whether transformer is active or not
        """
        self.activate_flag = activate_flag
        self.columns_indices_list = columns_indices_list
        self.columns_selected_flag = False

    def fit(self, X, y=None):
        assert X.ndim == 2
        self._check_n_features(X, reset=True)

        if debug:
            if isinstance(X, list):
                logger.debug("ColumnSelector: Starting fit(" + str(len(X)) + "x" + str(1) + ")")
            else:
                logger.debug(
                    "ColumnSelector: Starting fit("
                    + str(X.shape[0])
                    + "x"
                    + str(X.reshape(X.shape[0], -1).shape[1])
                    + ")"
                )
            if debug_timings:
                start_time = time()

        if self.activate_flag:
            # do fit here
            a = 1

        if debug:
            if debug_timings:
                elapsed_time = time() - start_time
                if isinstance(X, list):
                    logger.debug(
                        "ColumnSelector: Ending fit("
                        + str(len(X))
                        + "x"
                        + str(1)
                        + "), elapsed_time (s): "
                        + str(elapsed_time)
                    )
                else:
                    logger.debug(
                        "ColumnSelector: Ending fit("
                        + str(X.shape[0])
                        + "x"
                        + str(X.reshape(X.shape[0], -1).shape[1])
                        + "), elapsed_time (s): "
                        + str(elapsed_time)
                    )
            else:
                if isinstance(X, list):
                    logger.debug("ColumnSelector: Ending fit(" + str(len(X)) + "x" + str(1) + ")")
                else:
                    logger.debug(
                        "ColumnSelector: Ending fit("
                        + str(X.shape[0])
                        + "x"
                        + str(X.reshape(X.shape[0], -1).shape[1])
                        + ")"
                    )

        return self

    def transform(self, X):
        check_array(
            X, ensure_min_features=1, ensure_min_samples=1, dtype=None, force_all_finite="allow-nan", accept_sparse=True
        )

        if hasattr(self, "n_features_in_") and self.activate_flag:
            self._check_n_features(X, reset=False)

        if debug:
            if isinstance(X, list):
                logger.debug("ColumnSelector: Starting transform(" + str(len(X)) + "x" + str(1) + ")")
            else:
                logger.debug(
                    "ColumnSelector: Starting transform("
                    + str(X.shape[0])
                    + "x"
                    + str(X.reshape(X.shape[0], -1).shape[1])
                    + ")"
                )
            if debug_timings:
                start_time = time()

        if self.activate_flag:
            Y, self.columns_selected_flag = numpy_select_columns(X, columns_indices_list=self.columns_indices_list)
        else:
            self.columns_selected_flag = False
            Y = X

        if debug:
            if debug_timings:
                elapsed_time = time() - start_time
                if isinstance(X, list):
                    logger.debug(
                        "ColumnSelector: Ending transform("
                        + str(len(X))
                        + "x"
                        + str(1)
                        + "), elapsed_time (s): "
                        + str(elapsed_time)
                    )
                else:
                    logger.debug(
                        "ColumnSelector: Ending transform("
                        + str(Y.shape[0])
                        + "x"
                        + str(Y.reshape(Y.shape[0], -1).shape[1])
                        + "), elapsed_time (s): "
                        + str(elapsed_time)
                    )
            else:
                if isinstance(X, list):
                    logger.debug("ColumnSelector: Ending transform(" + str(len(X)) + "x" + str(1) + ")")
                else:
                    logger.debug(
                        "ColumnSelector: Ending transform("
                        + str(Y.shape[0])
                        + "x"
                        + str(Y.reshape(Y.shape[0], -1).shape[1])
                        + ")"
                    )

        if debug_transform_return:
            logger.debug(f"{self.__class__.__name__}.transform({X})->{Y}")
        return Y


class NumpyColumnSelector(BaseEstimator, TransformerMixin):
    """
    Selects a subset of columns of a numpy array
    """

    def __init__(self, columns=None):
        if columns is None:
            self.columns = []
        else:
            self.columns = columns  # list of column names to select

    def fit(self, X, y=None):
        self._check_n_features(X, reset=True)
        return self

    def transform(self, X):
        assert X.ndim == 2
        check_array(
            X, ensure_min_features=1, ensure_min_samples=1, dtype=None, force_all_finite="allow-nan", accept_sparse=True
        )

        if hasattr(self, "n_features_in_"):
            self._check_n_features(X, reset=False)

        if debug:
            logger.debug(
                "NumpyColumnSelector: Starting transform("
                + str(X.shape[0])
                + "x"
                + str(X.reshape(X.shape[0], -1).shape[1])
                + ")"
            )
            if debug_timings:
                start_time = time()

        # Y=X.copy()
        if self.columns:
            Y = X[:, self.columns]
        else:
            Y = X

        if debug:
            if debug_timings:
                elapsed_time = time() - start_time
                logger.debug(
                    "NumpyColumnSelector: Ending transform("
                    + str(Y.shape[0])
                    + "x"
                    + str(Y.reshape(Y.shape[0], -1).shape[1])
                    + "), elapsed_time (s): "
                    + str(elapsed_time)
                )
            else:
                logger.debug(
                    "NumpyColumnSelector: Ending transform("
                    + str(Y.shape[0])
                    + "x"
                    + str(Y.reshape(Y.shape[0], -1).shape[1])
                )

        if debug_transform_return:
            logger.debug(f"{self.__class__.__name__}.transform({X})->{Y}")
        return Y


class NumpyApplyAlongAxis(BaseEstimator, TransformerMixin):
    """
    Transformer that applies a function to 1-D slices along the given axis on a subset of rows or columns
    """

    def __init__(self, func1d, axis=None, index_list=None, *args, **kwargs):
        self.func1d = func1d
        if axis is None:
            self.axis = 0  # Default is columns
        else:
            self.axis = axis
        if index_list is None:
            self.index_list = []
        else:
            self.index_list = index_list

        self.args = args
        self.kwargs = kwargs

    def fit(self, X, y=None):
        self._check_n_features(X, reset=True)
        return self

    def transform(self, X):
        assert X.ndim == 2
        check_array(
            X, ensure_min_features=1, ensure_min_samples=1, dtype=None, force_all_finite="allow-nan", accept_sparse=True
        )

        if hasattr(self, "n_features_in_"):
            self._check_n_features(X, reset=False)

        if debug:
            logger.debug(
                "NumpyApplyAlongAxis: Starting transform("
                + str(X.shape[0])
                + "x"
                + str(X.reshape(X.shape[0], -1).shape[1])
                + ")"
            )

        Z_list = []
        if self.index_list:
            if self.axis == 0 or self.axis == 1:
                if self.axis == 0:
                    X_slice = X[:, self.index_list]
                else:
                    X_slice = X[self.index_list, :]

                Y = np.apply_along_axis(self.func1d, self.axis, X_slice)

        else:
            Y = X
        if debug:
            logger.debug(
                "NumpyApplyAlongAxis: Ending transform("
                + str(Y.shape[0])
                + "x"
                + str(Y.reshape(Y.shape[0], -1).shape[1])
                + ")"
            )

        if debug_transform_return:
            logger.debug(f"{self.__class__.__name__}.transform({X})->{Y}")
        return Y


class NumpyReplaceMissingValues(BaseEstimator, TransformerMixin):
    """
    Given a numpy array and a reference list of missing values for it,
    replaces missing values with a special value (typically a special missing value such as np.nan).
    """

    def __init__(self, missing_values, filling_values=np.nan):
        """

        :param missing_values: list of values considered as "missing" for the array
        :param filling_values: value to replace the missing values
        """
        if missing_values is None:
            self.missing_values = []
        else:
            self.missing_values = missing_values  # list of missing values to be replaced

        if filling_values is None:
            self.filling_values = np.nan
        else:
            self.filling_values = filling_values  # filling value for the missing values

    def fit(self, X, y=None):
        self._check_n_features(X, reset=True)
        return self

    def transform(self, X):
        assert X.ndim == 2
        check_array(
            X, ensure_min_features=1, ensure_min_samples=1, dtype=None, force_all_finite="allow-nan", accept_sparse=True
        )

        if hasattr(self, "n_features_in_"):
            self._check_n_features(X, reset=False)

        if debug:
            logger.debug(
                "NumpyReplaceMissingValues: Starting transform("
                + str(X.shape[0])
                + "x"
                + str(X.reshape(X.shape[0], -1).shape[1])
                + ")"
            )
            if debug_timings:
                start_time = time()

        Y = numpy_replace_values(
            X, filling_value=self.filling_values, reference_values_list=self.missing_values, invert_flag=False
        )

        if debug:
            if debug_timings:
                elapsed_time = time() - start_time
                logger.debug(
                    "NumpyReplaceMissingValues: Ending transform("
                    + str(Y.shape[0])
                    + "x"
                    + str(Y.reshape(Y.shape[0], -1).shape[1])
                    + "), elapsed_time (s): "
                    + str(elapsed_time)
                )
            else:
                logger.debug(
                    "NumpyReplaceMissingValues: Ending transform("
                    + str(Y.shape[0])
                    + "x"
                    + str(Y.reshape(Y.shape[0], -1).shape[1])
                    + ")"
                )

        if debug_transform_return:
            logger.debug(f"{self.__class__.__name__}.transform({X})->{Y}")
        return Y


class NumpyReplaceUnknownValues(BaseEstimator, TransformerMixin):
    """
    Given a numpy array and a reference list of known values for each column,
    replaces values that are not part of a reference list with a special value
    (typically np.nan). This is typically used to remove labels for columns in a test dataset
    that have not been seen in the corresponding columns of the training dataset.
    """

    def __init__(
        self, known_values_list=None, filling_values=None, missing_values_reference_list=None, filling_values_list=None
    ):
        """

        :param known_values_list: reference list of lists of known values for each column
        :param filling_values: special value assigned to unknown values
        """

        if missing_values_reference_list is None:
            self.missing_values_reference_list = global_missing_values_reference_list
        else:
            self.missing_values_reference_list = missing_values_reference_list

        if known_values_list is None:
            self.known_values_list = []
        else:
            self.known_values_list = known_values_list  # list of known values to the transformer

        if filling_values is None:
            self.filling_values = np.nan
        else:
            self.filling_values = filling_values  # filling value for the unknown values

        if filling_values_list is None:
            self.filling_values_list = []
        else:
            self.filling_values_list = filling_values_list

    def fit(self, X, y=None):
        self._check_n_features(X, reset=True)

        if type(self.known_values_list) is list:
            if len(self.known_values_list) == 0:
                from autoai_libs.utils.exportable_utils import numpy_get_categories

                numpy_get_categories(
                    X, range(X.shape[0]), self.missing_values_reference_list, categories_list2=self.known_values_list
                )
        return self

    def transform(self, X):
        assert X.ndim == 2
        check_array(
            X, ensure_min_features=1, ensure_min_samples=1, dtype=None, force_all_finite="allow-nan", accept_sparse=True
        )

        if hasattr(self, "n_features_in_"):
            self._check_n_features(X, reset=False)

        if debug:
            logger.debug(
                "NumpyReplaceUnknownValues: Starting transform("
                + str(X.shape[0])
                + "x"
                + str(X.reshape(X.shape[0], -1).shape[1])
                + ")"
            )
            if debug_timings:
                start_time = time()

        Y = numpy_replace_values(
            X, filling_value=self.filling_values, reference_values_list=self.known_values_list, invert_flag=True
        )

        if debug:
            if debug_timings:
                elapsed_time = time() - start_time
                logger.debug(
                    "NumpyReplaceUnknownValues: Ending transform("
                    + str(Y.shape[0])
                    + "x"
                    + str(Y.reshape(Y.shape[0], -1).shape[1])
                    + "), elapsed_time (s): "
                    + str(elapsed_time)
                )
            else:
                logger.debug(
                    "NumpyReplaceUnknownValues: Ending transform("
                    + str(Y.shape[0])
                    + "x"
                    + str(Y.reshape(Y.shape[0], -1).shape[1])
                    + ")"
                    + "\n"
                )

        if debug_transform_return:
            logger.debug(f"{self.__class__.__name__}.transform({X})->{Y}")
        return Y


class NumpyPermuteArray(BaseEstimator, TransformerMixin):
    """
    Rearranges columns or rows of a numpy array based on a list of indices
    """

    def __init__(self, permutation_indices=None, axis=None):
        """
        :param permutation_indices: list of indexes based on which columns will be rearranged
        :param axis: 0 permute along columns, 1, permute along rows
        """
        if permutation_indices is None:
            self.permutation_indices = []
        else:
            self.permutation_indices = permutation_indices

        if axis is None:
            self.axis = 0
        else:
            self.axis = axis

    def fit(self, X, y=None):
        self._check_n_features(X, reset=True)
        return self

    def transform(self, X):
        assert X.ndim == 2
        check_array(
            X, ensure_min_features=1, ensure_min_samples=1, dtype=None, force_all_finite="allow-nan", accept_sparse=True
        )

        if hasattr(self, "n_features_in_"):
            self._check_n_features(X, reset=False)

        if debug:
            logger.debug(
                "NumpyPermuteArray: Starting transform("
                + str(X.shape[0])
                + "x"
                + str(X.reshape(X.shape[0], -1).shape[1])
                + ")"
            )
            if debug_timings:
                start_time = time()

        Y = numpy_permute_array(X, self.permutation_indices, self.axis)

        if debug:
            if debug_timings:
                elapsed_time = time() - start_time
                logger.debug(
                    "NumpyPermuteArray: Ending transform("
                    + str(X.shape[0])
                    + "x"
                    + str(X.reshape(X.shape[0], -1).shape[1])
                    + "), elapsed_time (s): "
                    + str(elapsed_time)
                )
            else:
                logger.debug(
                    "NumpyPermuteArray: Ending transform("
                    + str(X.shape[0])
                    + "x"
                    + str(X.reshape(X.shape[0], -1).shape[1])
                    + ")\n"
                )

        Y = Y.reshape(Y.shape[0], -1)
        if debug_transform_return:
            logger.debug(f"{self.__class__.__name__}.transform({X})->{Y}")
        return Y


class OptStandardScaler(BaseEstimator, TransformerMixin):
    """
    This transformer implements an optional StandardScaler.
    It acts as a StandardScaler() if use_scaler_flag is True.
    Otherwise it returns the input numpy array unchanged
    """

    def __init__(self, use_scaler_flag=True, **kwargs):
        """

        :param use_scaler_flag: Act as StandardScaler() if true, do nothing if false. Deault is True
        StandardScaler parameters. See:
        http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html
        :param num_scaler_copy:
        :param num_scaler_with_mean:
        :param num_scaler_with_std:
        """

        self.use_scaler_flag = use_scaler_flag

        if self.use_scaler_flag:
            self.num_scaler_copy = kwargs.get("num_scaler_copy", True)
            self.num_scaler_with_mean = kwargs.get("num_scaler_with_mean", True)
            self.num_scaler_with_std = kwargs.get("num_scaler_with_std", True)

            self.scaler = StandardScaler(
                copy=self.num_scaler_copy, with_mean=self.num_scaler_with_mean, with_std=self.num_scaler_with_std
            )

    def fit(self, X, y=None):
        assert X.ndim == 2
        self._check_n_features(X, reset=True)

        if self.use_scaler_flag:
            self.scaler.fit(X, y)
        return self

    def transform(self, X):
        check_array(
            X, ensure_min_features=1, ensure_min_samples=1, dtype=None, force_all_finite="allow-nan", accept_sparse=True
        )

        if hasattr(self, "n_features_in_"):
            self._check_n_features(X, reset=False)

        if debug:
            logger.debug(
                "OptStandardScaler: Starting transform("
                + str(X.shape[0])
                + "x"
                + str(X.reshape(X.shape[0], -1).shape[1])
                + ")"
            )
            if debug_timings:
                start_time = time()

        if self.use_scaler_flag:
            Y = self.scaler.transform(X)
        else:
            Y = X

        if debug:
            if debug_timings:
                elapsed_time = time() - start_time
                logger.debug(
                    "OptStandardScaler: Ending transform("
                    + str(Y.shape[0])
                    + "x"
                    + str(Y.reshape(Y.shape[0], -1).shape[1])
                    + "), elapsed_time (s): "
                    + str(elapsed_time)
                )
            else:
                logger.debug(
                    "OptStandardScaler: Ending transform("
                    + str(Y.shape[0])
                    + "x"
                    + str(Y.reshape(Y.shape[0], -1).shape[1])
                    + ")"
                )

        if debug_transform_return:
            logger.debug(f"{self.__class__.__name__}.transform({X})->{Y}")
        return Y


class CatImputer(BaseEstimator, TransformerMixin):
    """
    This is a wrapper for categorical imputer
    """

    def __init__(
        self,
        strategy,
        missing_values,
        sklearn_version_family=global_sklearn_version_family,
        activate_flag=True,
        **kwargs,
    ):
        self.sklearn_version_family = sklearn_version_family
        self.strategy = strategy
        self.missing_values = missing_values
        self.activate_flag = activate_flag

        self.imputer = SimpleImputer(strategy=strategy, missing_values=missing_values)

    def fit(self, X, y=None):
        assert X.ndim == 2
        self._check_n_features(X, reset=True)

        if debug:
            logger.debug(
                "CatImputer: Starting fit(" + str(X.shape[0]) + "x" + str(X.reshape(X.shape[0], -1).shape[1]) + ")"
            )
            if debug_timings:
                start_time = time()

        if self.activate_flag:
            self.imputer.fit(X, y)

        if debug:
            if debug_timings:
                elapsed_time = time() - start_time
                logger.debug(
                    "CatImputer: Ending fit("
                    + str(X.shape[0])
                    + "x"
                    + str(X.reshape(X.shape[0], -1).shape[1])
                    + "), elapsed_time (s): "
                    + str(elapsed_time)
                )
            else:
                logger.debug(
                    "CatImputer: Ending fit(" + str(X.shape[0]) + "x" + str(X.reshape(X.shape[0], -1).shape[1]) + ")"
                )

        return self

    def transform(self, X):
        check_array(
            X, ensure_min_features=1, ensure_min_samples=1, dtype=None, force_all_finite="allow-nan", accept_sparse=True
        )

        if hasattr(self, "n_features_in_"):
            self._check_n_features(X, reset=False)

        if debug:
            logger.debug(
                "CatImputer: Starting transform("
                + str(X.shape[0])
                + "x"
                + str(X.reshape(X.shape[0], -1).shape[1])
                + ")"
            )
            if debug_timings:
                start_time = time()

        if self.activate_flag:
            Y = self.imputer.transform(X)
        else:
            Y = X

        if debug:
            if debug_timings:
                elapsed_time = time() - start_time
                logger.debug(
                    "CatImputer: Ending transform("
                    + str(Y.shape[0])
                    + "x"
                    + str(Y.reshape(Y.shape[0], -1).shape[1])
                    + "), elapsed_time (s): "
                    + str(elapsed_time)
                )
            else:
                logger.debug(
                    "CatImputer: Ending transform("
                    + str(Y.shape[0])
                    + "x"
                    + str(Y.reshape(Y.shape[0], -1).shape[1])
                    + ")"
                )

        if debug_transform_return:
            logger.debug(f"{self.__class__.__name__}.transform({X})->{Y}")
        return Y


class CatEncoder(BaseEstimator, TransformerMixin):
    """
    This is a template for classes
    """

    def __init__(
        self,
        encoding,
        categories,
        dtype,
        handle_unknown,
        sklearn_version_family=global_sklearn_version_family,
        activate_flag=True,
    ):
        self.encoding = encoding
        self.categories = categories
        self.dtype = dtype
        self.handle_unknown = handle_unknown
        self.sklearn_version_family = sklearn_version_family
        self.activate_flag = activate_flag

        if self.sklearn_version_family == "020dev" or self.sklearn_version_family == "019":
            from sklearn.preprocessing import CategoricalEncoder

            self.encoder = CategoricalEncoder(
                encoding=encoding, categories=categories, dtype=dtype, handle_unknown=handle_unknown
            )
        else:
            from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder

            if encoding == "ordinal":
                self.encoder = OrdinalEncoder(categories=categories, dtype=dtype)
            elif encoding == "onehot" or encoding == "onehot-dense":
                if encoding == "onehot":
                    sparse_flag = True
                else:
                    sparse_flag = False

                self.encoder = OneHotEncoder(
                    categories=categories, sparse=sparse_flag, dtype=dtype, handle_unknown=handle_unknown
                )
            else:
                # use ordinal if not specified
                self.encoder = OrdinalEncoder(categories=categories, dtype=dtype)

            # elif encoding == 'label':
            #     self.encoder = LabelEncoder()

    def fit(self, X, y=None):
        assert X.ndim == 2
        self._check_n_features(X, reset=True)

        if debug:
            logger.debug(
                "CatEncoder: Starting fit(" + str(X.shape[0]) + "x" + str(X.reshape(X.shape[0], -1).shape[1]) + ")"
            )
            if debug_timings:
                start_time = time()

        if self.activate_flag:
            Y = self.encoder.fit(X, y)
            self.categories_found = self.encoder.categories_

        if debug:
            if debug_timings:
                elapsed_time = time() - start_time
                logger.debug(
                    "CatEncoder: Ending fit("
                    + str(X.shape[0])
                    + "x"
                    + str(X.reshape(X.shape[0], -1).shape[1])
                    + "), elapsed_time (s): "
                    + str(elapsed_time)
                )
            else:
                logger.debug(
                    "CatEncoder: Ending fit(" + str(X.shape[0]) + "x" + str(X.reshape(X.shape[0], -1).shape[1]) + ")"
                )

        return self

    def transform(self, X):
        check_array(
            X, ensure_min_features=1, ensure_min_samples=1, dtype=None, force_all_finite="allow-nan", accept_sparse=True
        )

        if hasattr(self, "n_features_in_"):
            self._check_n_features(X, reset=False)

        if debug:
            logger.debug(
                "CatEncoder: Starting transform("
                + str(X.shape[0])
                + "x"
                + str(X.reshape(X.shape[0], -1).shape[1])
                + ")"
            )
            if debug_timings:
                start_time = time()

        if self.activate_flag:
            try:
                Y = self.encoder.transform(X)
            except ValueError as e:
                # Handling unknown categories for different sklearn versions
                if str(e).startswith("Found unknown categories") and (
                    sklearn_version_list[0] == "1"
                    or (sklearn_version_list[0] == "0" and int(sklearn_version_list[1]) > 23)
                ):
                    stre = str(e)
                    error_msg = "".join([stre.split("[")[0], stre.split("[")[1].split("]")[1]])
                else:
                    raise e
                warnings.warn(error_msg, Warning)
                temp_handle_unknown = self.encoder.handle_unknown
                # note: set unknown values handling in sklearn
                self.encoder.handle_unknown = "ignore"
                Y = self.encoder.transform(X)
                # note: unknown values handling in sklearn back to default for fit compatibility for OrdinalEncoder
                self.encoder.handle_unknown = temp_handle_unknown
        else:
            Y = X

        if debug:
            if debug_timings:
                elapsed_time = time() - start_time
                logger.debug(
                    "CatEncoder: Ending transform("
                    + str(Y.shape[0])
                    + "x"
                    + str(Y.reshape(Y.shape[0], -1).shape[1])
                    + "), elapsed_time (s): "
                    + str(elapsed_time)
                )
            else:
                logger.debug(
                    "CatEncoder: Ending transform("
                    + str(Y.shape[0])
                    + "x"
                    + str(Y.reshape(Y.shape[0], -1).shape[1])
                    + ")"
                )

        if debug_transform_return:
            logger.debug(f"{self.__class__.__name__}.transform({X})->{Y}")
        return Y


def is_all_missing(x, bad_vals):
    try:  # Handle bad_vals as atomic
        std_bad = [v for v in bad_vals if not np.isnan(v)]
    except:
        bad_vals = [bad_vals]
        std_bad = [v for v in bad_vals if not np.isnan(v)]

    assert len(std_bad) + 1 >= len(bad_vals)
    test_nan = len(std_bad) < len(bad_vals)
    if not test_nan:
        return np.isin(x, std_bad).all()
    else:  # All nans or mixed
        it = (np.isnan(float(cell)) or np.isin(cell, std_bad) for cell in x)
        return np.fromiter(it, float).all()


class NumImputer(BaseEstimator, TransformerMixin):
    """
    This is a wrapper for numerical imputer
    """

    def __init__(self, strategy, missing_values, activate_flag=True, **kwargs):
        self.strategy = strategy
        self.missing_values = missing_values
        self.activate_flag = activate_flag
        self.imputer = SimpleImputer(strategy=strategy, missing_values=missing_values)

    def fit(self, X, y=None):
        self._check_n_features(X, reset=True)

        if debug:
            logger.debug(
                "NumImputer: Starting fit(" + str(X.shape[0]) + "x" + str(X.reshape(X.shape[0], -1).shape[1]) + ")"
            )
            if debug_timings:
                start_time = time()

        if self.activate_flag:
            # We need to record which columns are made up of only missing values
            # if the strategy is not 'constant' since these columns will be DISCARDED
            # when we call transform afterwards.
            if self.strategy != "constant":
                self.bad_columns = sorted(
                    [c for c in range(X.shape[1]) if is_all_missing(X[:, c], self.missing_values)]
                )
            self.imputer.fit(X, y)

        if debug:
            if debug_timings:
                elapsed_time = time() - start_time
                logger.debug(
                    "NumImputer: Ending fit("
                    + str(X.shape[0])
                    + "x"
                    + str(X.reshape(X.shape[0], -1).shape[1])
                    + "), elapsed_time (s): "
                    + str(elapsed_time)
                )
            else:
                logger.debug(
                    "NumImputer: Ending fit(" + str(X.shape[0]) + "x" + str(X.reshape(X.shape[0], -1).shape[1]) + ")"
                )

        return self

    def transform(self, X):
        check_array(
            X, ensure_min_features=1, ensure_min_samples=1, dtype=None, force_all_finite="allow-nan", accept_sparse=True
        )

        if hasattr(self, "n_features_in_"):
            self._check_n_features(X, reset=False)

        if debug:
            logger.debug(
                "NumImputer: Starting transform("
                + str(X.shape[0])
                + "x"
                + str(X.reshape(X.shape[0], -1).shape[1])
                + ")"
            )
            if debug_timings:
                start_time = time()

        if self.activate_flag:
            Y = X.astype(float)
            Y = self.imputer.transform(Y)
            if self.strategy != "constant":
                # Place a try here so that pipelines pickled before the
                # introduction of self.bad_columns will still hopefully
                # work even though they don't have a bad_columns field.
                # Yes, this is ugly!
                # TODO: Remove this try/except when we can!
                try:
                    insertion_indices = [bi - i for i, bi in enumerate(self.bad_columns)]
                    Y = np.insert(Y, insertion_indices, 0, axis=1)
                except:
                    pass
        else:
            Y = X

        if debug:
            if debug_timings:
                elapsed_time = time() - start_time
                logger.debug(
                    "NumImputer: Ending transform("
                    + str(Y.shape[0])
                    + "x"
                    + str(Y.reshape(Y.shape[0], -1).shape[1])
                    + "), elapsed_time (s): "
                    + str(elapsed_time)
                )
            else:
                logger.debug(
                    "NumImputer: Ending transform("
                    + str(Y.shape[0])
                    + "x"
                    + str(Y.reshape(Y.shape[0], -1).shape[1])
                    + ")"
                )

        if debug_transform_return:
            logger.debug(f"{self.__class__.__name__}.transform({X})->{Y}")
        assert X.shape == Y.shape
        return Y


class AllPassPreprocessingTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        self._check_n_features(X, reset=True)

        if debug:
            logger.debug(
                "AllPassPreprocessingTransformer: Starting fit("
                + str(X.shape[0])
                + "x"
                + str(X.reshape(X.shape[0], -1).shape[1])
                + ")"
            )
            if debug_timings:
                start_time = time()

        if debug:
            if debug_timings:
                elapsed_time = time() - start_time
                logger.debug(
                    "AllPassPreprocessingTransformer: Ending fit("
                    + str(X.shape[0])
                    + "x"
                    + str(X.reshape(X.shape[0], -1).shape[1])
                    + "), elapsed_time (s): "
                    + str(elapsed_time)
                )
            else:
                logger.debug(
                    "AllPassPreprocessingTransformer: Ending fit("
                    + str(X.shape[0])
                    + "x"
                    + str(X.reshape(X.shape[0], -1).shape[1])
                    + ")"
                )

        return self

    def transform(self, X):
        assert X.ndim == 2
        check_array(
            X, ensure_min_features=1, ensure_min_samples=1, dtype=None, force_all_finite="allow-nan", accept_sparse=True
        )

        if hasattr(self, "n_features_in_"):
            self._check_n_features(X, reset=False)

        if debug:
            logger.debug(
                "AllPassPreprocessingTransformer: Starting transform("
                + str(X.shape[0])
                + "x"
                + str(X.reshape(X.shape[0], -1).shape[1])
                + ")"
            )
            if debug_timings:
                start_time = time()

        # Y = X.copy()
        Y = X

        if debug:
            if debug_timings:
                elapsed_time = time() - start_time
                logger.debug(
                    "AllPassPreprocessingTransformer: Ending transform("
                    + str(Y.shape[0])
                    + "x"
                    + str(Y.reshape(Y.shape[0], -1).shape[1])
                    + "), elapsed_time (s): "
                    + str(elapsed_time)
                )
            else:
                logger.debug(
                    "AllPassPreprocessingTransformer: Ending transform("
                    + str(Y.shape[0])
                    + "x"
                    + str(Y.reshape(Y.shape[0], -1).shape[1])
                    + ")"
                )

        if debug_transform_return:
            logger.debug(f"{self.__class__.__name__}.transform({X})->{Y}")
        return Y


class CompressStrings(BaseEstimator, TransformerMixin):
    """
    Removes spaces and special characters from string columns of a numpy array
    """

    def __init__(
        self,
        compress_type="string",
        dtypes_list=None,
        misslist_list=None,
        missing_values_reference_list=None,
        activate_flag=True,
    ):
        self.compress_type = compress_type

        if dtypes_list is None:
            self.dtypes_list = []
        else:
            self.dtypes_list = dtypes_list

        if misslist_list is None:
            self.misslist_list = []
        else:
            self.misslist_list = misslist_list

        self.activate_flag = activate_flag
        if missing_values_reference_list is None:
            self.missing_values_reference_list = global_missing_values_reference_list
        else:
            self.missing_values_reference_list = missing_values_reference_list

    def fit(self, X, y=None):
        self._check_n_features(X, reset=True)

        if debug:
            logger.debug(
                "CompressStrings: Starting fit(" + str(X.shape[0]) + "x" + str(X.reshape(X.shape[0], -1).shape[1]) + ")"
            )
            if debug_timings:
                start_time = time()

        if self.activate_flag:
            # do fit here
            a = 1

        if debug:
            if debug_timings:
                elapsed_time = time() - start_time
                logger.debug(
                    "CompressStrings: Ending fit("
                    + str(X.shape[0])
                    + "x"
                    + str(X.reshape(X.shape[0], -1).shape[1])
                    + "), elapsed_time (s): "
                    + str(elapsed_time)
                )
            else:
                logger.debug(
                    "CompressStrings: Ending fit("
                    + str(X.shape[0])
                    + "x"
                    + str(X.reshape(X.shape[0], -1).shape[1])
                    + ")"
                )

        return self

    def transform(self, X):
        assert X.ndim == 2
        check_array(
            X, ensure_min_features=1, ensure_min_samples=1, dtype=None, force_all_finite="allow-nan", accept_sparse=True
        )

        if hasattr(self, "n_features_in_"):
            self._check_n_features(X, reset=False)

        if debug:
            logger.debug(
                "CompressStrings: Starting transform("
                + str(X.shape[0])
                + "x"
                + str(X.reshape(X.shape[0], -1).shape[1])
                + ")"
            )
            if debug_timings:
                start_time = time()

        if self.activate_flag:
            Y = X.copy()
            num_columns = X.shape[1]

            if (
                self.dtypes_list
                and self.misslist_list
                and len(self.dtypes_list) == num_columns
                and len(self.misslist_list) == num_columns
            ):
                execute_numpywhatis_flag = False
            else:
                execute_numpywhatis_flag = True

            for j in range(num_columns):
                Xcol = X[:, j]

                # FIXME: reverted temporarily to old slow code that does not use cache.
                execute_numpywhatis_flag = False
                # FIXME: reverted temporarily to old slow code that does not use cache.
                # bug comes in HOUSE_PRICING column 34, row 320
                if execute_numpywhatis_flag:
                    misslist, dtype_str = numpy_whatis(Xcol, self.missing_values_reference_list)
                else:
                    dtype_str = self.dtypes_list[j]
                    misslist = self.misslist_list[j]
                if dtype_str == "char_str":
                    Y[:, j] = compress_str_column(Xcol, misslist, self.compress_type)
        else:
            Y = X

        if debug:
            if debug_timings:
                elapsed_time = time() - start_time
                logger.debug(
                    "CompressStrings: Ending transform("
                    + str(Y.shape[0])
                    + "x"
                    + str(Y.reshape(Y.shape[0], -1).shape[1])
                    + "), elapsed_time (s): "
                    + str(elapsed_time)
                )
            else:
                logger.debug(
                    "CompressStrings: Ending transform("
                    + str(Y.shape[0])
                    + "x"
                    + str(Y.reshape(Y.shape[0], -1).shape[1])
                    + ")"
                )

        if debug_transform_return:
            logger.debug(f"{self.__class__.__name__}.transform({X})->{Y}")
        return Y


class FloatStr2Float(BaseEstimator, TransformerMixin):
    def __init__(self, dtypes_list, missing_values_reference_list=None, activate_flag=True):
        self.dtypes_list = dtypes_list
        self.missing_values_reference_list = setValueOrDefault(
            missing_values_reference_list, global_missing_values_reference_list
        )

        self.activate_flag = activate_flag

    def fit(self, X, y=None):
        assert X.ndim == 2
        self._check_n_features(X, reset=True)

        if debug:
            logger.debug(
                "FloatStr2Float: Starting fit(" + str(X.shape[0]) + "x" + str(X.reshape(X.shape[0], -1).shape[1]) + ")"
            )
            if debug_timings:
                start_time = time()

        if self.activate_flag:
            # do fit here
            a = 1

        if debug:
            if debug_timings:
                elapsed_time = time() - start_time
                logger.debug(
                    "FloatStr2Float: Ending fit("
                    + str(X.shape[0])
                    + "x"
                    + str(X.reshape(X.shape[0], -1).shape[1])
                    + "), elapsed_time (s): "
                    + str(elapsed_time)
                )
            else:
                logger.debug(
                    "FloatStr2Float: Ending fit("
                    + str(X.shape[0])
                    + "x"
                    + str(X.reshape(X.shape[0], -1).shape[1])
                    + ")"
                )

        return self

    def transform(self, X):
        check_array(
            X, ensure_min_features=1, ensure_min_samples=1, dtype=None, force_all_finite="allow-nan", accept_sparse=True
        )

        if hasattr(self, "n_features_in_"):
            self._check_n_features(X, reset=False)

        if debug:
            logger.debug(
                "FloatStr2Float: Starting transform("
                + str(X.shape[0])
                + "x"
                + str(X.reshape(X.shape[0], -1).shape[1])
                + ")"
            )
            if debug_timings:
                start_time = time()

        if self.activate_flag:
            # do transform here
            num_rows = X.shape[0]
            num_columns = X.shape[1]

            Y = np.empty((num_rows, num_columns), dtype=object)

            for j, dtype in enumerate(self.dtypes_list):
                if dtype == "float_str":
                    Y[:, j] = numpy_floatstr2float(X[:, j], self.missing_values_reference_list)
                else:
                    Y[:, j] = X[:, j].copy()
        else:
            Y = X

        if debug:
            if debug_timings:
                elapsed_time = time() - start_time
                logger.debug(
                    "FloatStr2Float: Ending transform("
                    + str(Y.shape[0])
                    + "x"
                    + str(Y.reshape(Y.shape[0], -1).shape[1])
                    + "), elapsed_time (s): "
                    + str(elapsed_time)
                )
            else:
                logger.debug(
                    "FloatStr2Float: Ending transform("
                    + str(Y.shape[0])
                    + "x"
                    + str(Y.reshape(Y.shape[0], -1).shape[1])
                    + ")"
                )

        if debug_transform_return:
            logger.debug(f"{self.__class__.__name__}.transform({X})->{Y}")
        return Y


class float32_transform(BaseEstimator, TransformerMixin):
    """
    Transforms a float64 numpy array to float32
    """

    def __init__(self, activate_flag=True):
        self.activate_flag = activate_flag

    def fit(self, X, y=None):
        self._check_n_features(X, reset=True)

        if debug:
            logger.debug(
                "float32_transform: Starting fit("
                + str(X.shape[0])
                + "x"
                + str(X.reshape(X.shape[0], -1).shape[1])
                + ")"
            )
            if debug_timings:
                start_time = time()

        if self.activate_flag:
            # do fit here
            a = 1

        if debug:
            if debug_timings:
                elapsed_time = time() - start_time
                logger.debug(
                    "float32_transform: Ending fit("
                    + str(X.shape[0])
                    + "x"
                    + str(X.reshape(X.shape[0], -1).shape[1])
                    + "), elapsed_time (s): "
                    + str(elapsed_time)
                )
            else:
                logger.debug(
                    "float32_transform: Ending fit("
                    + str(X.shape[0])
                    + "x"
                    + str(X.reshape(X.shape[0], -1).shape[1])
                    + ")"
                )

        return self

    def transform(self, X):
        assert X.ndim == 2
        check_array(
            X, ensure_min_features=1, ensure_min_samples=1, dtype=None, force_all_finite="allow-nan", accept_sparse=True
        )

        if hasattr(self, "n_features_in_"):
            self._check_n_features(X, reset=False)

        if debug:
            logger.debug(
                "float32_transform: Starting transform("
                + str(X.shape[0])
                + "x"
                + str(X.reshape(X.shape[0], -1).shape[1])
                + ")"
            )
            if debug_timings:
                start_time = time()

        if self.activate_flag:
            Y = convert_float32(X)
        else:
            Y = X

        if debug:
            if debug_timings:
                elapsed_time = time() - start_time
                logger.debug(
                    "float32_transform: Ending transform("
                    + str(Y.shape[0])
                    + "x"
                    + str(Y.reshape(Y.shape[0], -1).shape[1])
                    + "), elapsed_time (s): "
                    + str(elapsed_time)
                )
            else:
                logger.debug(
                    "float32_transform: Ending transform("
                    + str(Y.shape[0])
                    + "x"
                    + str(Y.reshape(Y.shape[0], -1).shape[1])
                    + ")"
                )

        if debug_transform_return:
            logger.debug(f"{self.__class__.__name__}.transform({X})->{Y}")
        return Y


class boolean2float(BaseEstimator, TransformerMixin):
    """
    This is a template for classes
    """

    def __init__(self, activate_flag=True):
        self.activate_flag = activate_flag

    def fit(self, X, y=None):
        self._check_n_features(X, reset=True)

        if debug:
            logger.debug(
                "boolean2float: Starting fit(" + str(X.shape[0]) + "x" + str(X.reshape(X.shape[0], -1).shape[1]) + ")"
            )
            if debug_timings:
                start_time = time()

        if self.activate_flag:
            # do fit here
            a = 1

        if debug:
            if debug_timings:
                elapsed_time = time() - start_time
                logger.debug(
                    "boolean2float: Ending fit("
                    + str(X.shape[0])
                    + "x"
                    + str(X.reshape(X.shape[0], -1).shape[1])
                    + "), elapsed_time (s): "
                    + str(elapsed_time)
                )
            else:
                logger.debug(
                    "boolean2float: Ending fit(" + str(X.shape[0]) + "x" + str(X.reshape(X.shape[0], -1).shape[1]) + ")"
                )

        return self

    def transform(self, X):
        assert X.ndim == 2
        check_array(
            X, ensure_min_features=1, ensure_min_samples=1, dtype=None, force_all_finite="allow-nan", accept_sparse=True
        )

        if hasattr(self, "n_features_in_"):
            self._check_n_features(X, reset=False)

        if debug:
            logger.debug(
                "boolean2float: Starting transform("
                + str(X.shape[0])
                + "x"
                + str(X.reshape(X.shape[0], -1).shape[1])
                + ")"
            )
            if debug_timings:
                start_time = time()

        Y = 0

        if self.activate_flag:
            Y = numpy_boolean2float(X)
            a = 1
        else:
            Y = X

        if debug:
            if debug_timings:
                elapsed_time = time() - start_time
                logger.debug(
                    "boolean2float: Ending transform("
                    + str(Y.shape[0])
                    + "x"
                    + str(Y.reshape(Y.shape[0], -1).shape[1])
                    + "), elapsed_time (s): "
                    + str(elapsed_time)
                )
            else:
                logger.debug(
                    "boolean2float: Ending transform("
                    + str(Y.shape[0])
                    + "x"
                    + str(Y.reshape(Y.shape[0], -1).shape[1])
                    + ")"
                )
        if debug_transform_return:
            logger.debug(f"{self.__class__.__name__}.transform({X})->{Y}")
        return Y
