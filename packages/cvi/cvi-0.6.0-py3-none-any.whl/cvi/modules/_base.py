"""
Utilities that are common across all CVI objects.

# Authors
- Sasha Petrenko <sap625@mst.edu>
"""

# Standard library imports
from typing import (
    Callable,
    Union
)
from abc import abstractmethod

# Custom imports
import numpy as np

# --------------------------------------------------------------------------- #
# CLASSES
# --------------------------------------------------------------------------- #


class LabelMap():
    """
    Internal map between labels and the incremental CVI categories.
    """

    def __init__(self):
        self.map = dict()

    def get_internal_label(self, label: int) -> int:
        """
        Gets the internal label and updates the label map if the label is new.
        """

        # Initialize the internal label
        internal_label = None

        # If the label is in the map, return that
        if label in self.map:
            internal_label = self.map[label]
        # Otherwise, create an incremented new label and return that
        else:
            # Correct for python zero-indexing by not including the +1
            internal_label = len(self.map.items())
            self.map[label] = internal_label

        return internal_label


class CVI():
    """
    Superclass containing elements shared between all CVIs.
    """

    def __init__(self):
        """
        CVI base class initialization method.
        """

        self._label_map = LabelMap()
        self._dim = 0
        self._n_samples = 0
        self._n = []                 # dim
        self._v = np.zeros([0, 0])   # n_clusters x dim
        self._CP = []                # dim
        self._G = np.zeros([0, 0])   # n_clusters x dim
        self._n_clusters = 0
        self.criterion_value = 0.0
        self._is_setup = False

    def _setup(self, sample: np.ndarray):
        """
        Common CVI procedure for incremental setup.

        Parameters
        ----------
        data : numpy.ndarray
            Sample vector of features.
        """

        # Infer the dimension as the length of the provided sample
        self._dim = len(sample)

        # Set the sizes of common arrays for consistent appending
        self._v = np.zeros([0, self._dim])
        self._G = np.zeros([0, self._dim])

        # Declare that the CVI is internally setup
        self._is_setup = True

    def _setup_batch(self, data: np.ndarray):
        """
        Common CVI procedure for batch setup.

        Parameters
        ----------
        data : np.ndarray
            A batch of samples with some feature dimension.
        """

        # Infer the data dimension and number of samples
        self._n_samples, self._dim = data.shape
        self._is_setup = True

    @abstractmethod
    def _param_inc(self, sample: np.ndarray, label: int):
        raise NotImplementedError

    @abstractmethod
    def _param_batch(self, data: np.ndarray, labels: np.ndarray):
        raise NotImplementedError

    @abstractmethod
    def _evaluate(self):
        raise NotImplementedError

    def get_cvi(self, data: np.ndarray, label: Union[int, np.ndarray]) -> float:
        """
        Updates the CVI parameters and then evaluates and returns the criterion value.

        This method accepts _either_ a single vector of data with an integer label (incremental mode) _or_ a batch of samples with a vector of integer labels (batch mode).

        Parameters
        ----------
        data : np.ndarray
            The sample(s) of features used for clustering.
        label : Union[int, np.ndarray]
            The label(s) prescribed to the sample(s) by the clustering algorithm.

        Returns
        -------
        float
            The CVI's criterion value.
        """

        # If we got 1D data, do a quick update
        if (data.ndim == 1):
            self._param_inc(data, label)

        # Otherwise, we got 2D data and do the correct update
        elif (data.ndim == 2):

            # If we haven't done a batch update yet
            if not self._is_setup:

                # Check that there are at least two unique labels
                if not len(np.unique(label)) > 1:
                    raise ValueError(
                        "Batch CVI mode requires at least two unique labels"
                    )

                # Do a batch update
                self._param_batch(data, label)

            # Otherwise, we are already setup
            else:

                # Error until batch to incremental is supported
                raise ValueError(
                    "Switching from batch to incremental not supported"
                )

                # Do many incremental updates
                # for ix in range(len(label)):
                #     self._param_inc(data[ix, :], label[ix])

        # Otherwise, we got incorrectly dimensioned data
        else:

            # Error until some intelligent data sanitization is implemented
            raise ValueError(
                f"Please provide 1D or 2D numpy array, recieved ndim={data.ndim}"
            )

        # Regardless of path, evaluate and extract the criterion value
        self._evaluate()
        criterion_value = self.criterion_value

        # Return the criterion value
        return criterion_value


# --------------------------------------------------------------------------- #
# DECORATORS
# --------------------------------------------------------------------------- #


def _add_docs(docstring: str) -> Callable[[], None]:
    """
    A decorator for appending a string to the docstring of a function.

    Parameters
    ----------
    docstring : str
        The docstring that you want to append to the decorated function.
    """

    def dec(func):
        func.__doc__ = func.__doc__ + docstring
        return func

    return dec


# --------------------------------------------------------------------------- #
# DOCSTRINGS
# --------------------------------------------------------------------------- #

# This docstring documents the shared API for incremental setup
_setup_doc = (
    """
    Sets up the dimensions of the CVI based on the sample size.

    Parameters
    ----------
    sample : numpy.ndarray
        A sample vector of features.
    """
)

# This docstring documents the shared API for incremental parameter updates
_param_inc_doc = (
    """
    Parameters
    ----------
    sample : numpy.ndarray
        A sample row vector of features.
    label : int
        An integer label for the cluster, zero-indexed.
    """
)

# This docstring documents the shared API for batch parameter updates
_param_batch_doc = (
    """
    Parameters
    ----------
    sample : numpy.ndarray
        A batch of samples; each row is a new sample of features.
    label : numpy.ndarray
        A vector of integer labels, zero-indexed.
    """
)

# This docstring documents the shared API for criterion value evaluation
_evaluate_doc = (
    """
    Updates the internal `criterion_value` parameter.
    """
)
