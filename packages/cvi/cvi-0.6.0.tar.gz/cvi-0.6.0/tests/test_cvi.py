"""
    test_cvi.py

# Description
Tests the cvi package.

# Authors
- Sasha Petrenko <sap625@mst.edu>
"""

# --------------------------------------------------------------------------- #
# STANDARD IMPORTS
# --------------------------------------------------------------------------- #

import os
from pathlib import Path
import logging as lg
from dataclasses import dataclass
from typing import (
    List,
    Dict,
    Tuple,
)

# --------------------------------------------------------------------------- #
# CUSTOM IMPORTS
# --------------------------------------------------------------------------- #

import pytest
import numpy as np
import pandas as pd
import sklearn.metrics as skm

# --------------------------------------------------------------------------- #
# LOCAL IMPORTS
# --------------------------------------------------------------------------- #

import src.cvi as cvi

print(f"\nTesting path is: {os.getcwd()}")


# --------------------------------------------------------------------------- #
# UTILITY FUNCTIONS
# --------------------------------------------------------------------------- #


def get_cvis() -> List[cvi.CVI]:
    """
    Returns a list of constructed CVI modules.

    Returns
    -------
    List[cvi.CVI]
        A list of constructed CVI objects for fresh use.
    """

    # Construct a list of CVI objects
    cvis = [
        local_cvi() for local_cvi in cvi.MODULES
    ]

    return cvis


def get_one_cvi() -> cvi.CVI:
    """
    Returns a single CVI for tests that test for common usage.

    Returns
    -------
    cvi.CVI
        A single constructed CVI object.
    """

    # Construct a CVI object
    local_cvi = cvi.CH()

    # Return the constructed object
    return local_cvi


def log_data(local_data: Dict):
    """
    Info-logs aspects of the passed data dictionary for diagnosis.

    Parameters
    ----------
    local_data : Dict
        A dictionary containing arrays of samples and labels.
    """

    # Log the type, shape, and number of samples and labels
    lg.info(
        f"Samples: type {type(local_data['samples'])}, "
        f"shape {local_data['samples'].shape}"
    )
    lg.info(
        f"Labels: type {type(local_data['labels'])}, "
        f"shape {local_data['labels'].shape}"
    )


def get_sample(local_data: Dict, index: int) -> Tuple[np.ndarray, int]:
    """
    Grabs a sample and label from the data dictionary at the provided index.

    Parameters
    ----------
    local_data : Dict
        Dictionary containing an array of samples and vector of labels.
    index : int
        The index to load the sample at.

    Returns
    -------
    Tuple[np.ndarray, int]
        A tuple of sample features and the integer label prescribed to the sample.
    """

    # Grab a sample and label at the index
    sample = local_data["samples"][index, :]
    label = local_data["labels"][index]

    return sample, label


def load_pd_csv(data_path: Path, frac: float) -> pd.DataFrame:
    """
    Loads a csv file using pandas, subsampling the data at the given fraction while preservign order.

    Parameters
    ----------
    data_path : Path
        The pathlib.Path where the data .csv file is.
    frac : float
        The data subsampling fraction within (0, 1].

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame containing the subsampled data.
    """

    # Load the data as a pandas array, subsample, and preserve order by the index
    local_data = (
        pd.read_csv(data_path)
        .sample(frac=frac)
        .sort_index()
    )

    return local_data


def split_data_columns(df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
    """
    Splits a pandas DataFrame into numpy arrays of samples and labels, assuming the last column is labels.

    Parameters
    ----------
    df : pd.DataFrame
        A pandas DataFrame containing the samples and their corresponding labels.

    Returns
    -------
    Tuple[np.ndarray, np.ndarray]
        A tuple of numpy arrays containing the separate samples and their corresponding labels.
    """

    # Index to before the last index, correct for python 0-indexing.
    samples = df.to_numpy(dtype=float)[:, :-1]
    labels = df.to_numpy(dtype=int)[:, -1] - 1

    return samples, labels


def inline_test_diff(a: float, b: float, tolerance=1e3):
    assert (
        (abs(a - b) / ((a + b) / 2)) < tolerance
    )


# --------------------------------------------------------------------------- #
# DATACLASSES
# --------------------------------------------------------------------------- #


@dataclass
class TestData():
    """
    A container dataclass for test data.
    """

    # The test dataset dictionary
    datasets: Dict

    # Tells pytest that this is not a test class
    __test__ = False

    def count(self, dataset: str) -> int:
        """
        Returns the number of samples in a dataset entry.

        Parameters
        ----------
        dataset : str
            The key corresponding to which dataset you wish to get a count of.

        Returns
        -------
        int
            The number of samples in self.datasets[dataset].
        """

        return len(self.datasets[dataset]["labels"])


# --------------------------------------------------------------------------- #
# FIXTURES
# --------------------------------------------------------------------------- #


# Set the fixture scope to the testing session to load the data once
@pytest.fixture(scope="session")
def data() -> TestData:
    """
    Data loading test fixture.

    This fixture is run once for the entire pytest session.
    """

    # p = 0.1
    p = 1
    lg.info("LOADING DATA")

    data_path = Path("tests", "data")

    # Load the test datasets
    correct = load_pd_csv(data_path.joinpath("correct_partition.csv"), p)
    over = load_pd_csv(data_path.joinpath("over_partition.csv"), p)
    under = load_pd_csv(data_path.joinpath("under_partition.csv"), p)

    # Coerce the dataframe as two numpy arrays each for ease
    correct_samples, correct_labels = split_data_columns(correct)
    over_samples, over_labels = split_data_columns(over)
    under_samples, under_labels = split_data_columns(under)

    # Construct the dataset dictionary
    data_dict = {
        "correct": {
            "samples": correct_samples,
            "labels": correct_labels,
        },
        "over": {
            "samples": over_samples,
            "labels": over_labels,
        },
        "under": {
            "samples": under_samples,
            "labels": under_labels,
        },
    }

    # Instantiate and return the TestData object
    return TestData(data_dict)


# --------------------------------------------------------------------------- #
# TESTS
# --------------------------------------------------------------------------- #


class TestCVI:
    """
    Pytest class containing CVI/ICVI unit tests.
    """

    def test_load_data(self, data: TestData):
        """
        Test loading the partitioning data.

        Parameters
        ----------
        data : TestData
            The data loaded as a pytest fixture.
        """

        lg.info("--- TESTING DATA LOADING ---")
        lg.info(f"Data location: {id(data)}")

        for value in data.datasets.values():
            log_data(value)

    def test_loading_again(self, data: TestData):
        """
        Tests loading the data again to verify the identity of the data dictionary.

        Parameters
        ----------
        data : TestData
            The data loaded as a pytest fixture.
        """

        lg.info("--- TESTING LOADING AGAIN TO VERIFY DATA SINGLETON ---")
        log_data(data.datasets["correct"])
        lg.info(f"Data location: {id(data)}")

    def test_icvis(self, data: TestData):
        """
        Test the functionality all of the icvis.

        Parameters
        ----------
        data : TestData
            The data loaded as a pytest fixture.
        """

        lg.info("--- TESTING ALL ICVIS ---")

        # Set the tolerance for incremental/batch CVI equivalence
        tolerance = 1e-1

        for key, local_data in data.datasets.items():
            lg.info(f"Testing data: {key}")
            n_samples = data.count(key)

            # Incremental
            i_cvis = get_cvis()
            for local_cvi in i_cvis:
                for ix in range(n_samples):
                    # Grab a sample and label
                    sample, label = get_sample(local_data, ix)
                    _ = local_cvi.get_cvi(sample, label)
            # Batch
            b_cvis = get_cvis()
            for local_cvi in b_cvis:
                _ = local_cvi.get_cvi(local_data["samples"], local_data["labels"])

            # # Switch batch to incremental
            # bi_cvis = get_cvis()
            # for local_cvi in bi_cvis:
            #     # Index to half of the data
            #     split_index = n_samples // 2
            #     # Compute half of the data in batch
            #     _ = local_cvi.get_cvi(
            #         local_data["samples"][:split_index, :],
            #         local_data["labels"][:split_index]
            #     )
            #     # Compute the other half incrementally
            #     for ix in range(split_index, n_samples):
            #         # Grab a sample and label
            #         sample, label = get_sample(local_data, ix)
            #         _ = local_cvi.get_cvi(sample, label)

            # Test equivalence between batch and incremental results
            for i in range(len(i_cvis)):
                # I -> B
                a = i_cvis[i].criterion_value
                b = b_cvis[i].criterion_value
                assert (
                    (abs(a - b) / ((a + b) / 2))
                    < tolerance
                )
                # # I -> BI
                # assert (
                #     (i_cvis[i].criterion_value - bi_cvis[i].criterion_value)
                #     < tolerance
                # )
                # # B -> BI
                # assert (
                #     (b_cvis[i].criterion_value - bi_cvis[i].criterion_value)
                #     < tolerance
                # )
                lg.info(
                    f"CVI: {type(i_cvis[i]).__name__}, "
                    f"I: {b_cvis[i].criterion_value:.5f}, "
                    f"B: {i_cvis[i].criterion_value:.5f},"
                    # f"BI: {bi_cvis[i].criterion_value},"
                )

    def test_rCIP_batch(self):
        """
        This test covers and edge case where rCIP is provided only a single sample of any cluster during its batch update.
        """

        # Create data, two samples of one cluster and one sample of another
        local_data = np.array([[0, 1], [1, 1], [1, 2]])
        local_labels = np.array([0, 0, 1])

        # Create the rCIP module and run a batch iteration
        local_cvi = cvi.rCIP()
        _ = local_cvi.get_cvi(local_data, local_labels)

        # Check that the edge case produces the expected result
        assert np.array_equal(local_cvi._sigma[:, :, 1], local_cvi._delta_term)


class Test_get_cvi:
    """
    Pytest class containing all unit tests for get_cvi.
    """

    def test_error_3d_invalid(self):
        """
        Tests that 3D data is rejected.
        """

        # Create some dummy 3D data
        dim = 2
        local_data = np.zeros((dim, dim, dim))
        local_label = 0

        # Create a CVI
        local_cvi = get_one_cvi()

        # Test that a 3D array is invalud
        with pytest.raises(ValueError):
            # Try passing a 3D array
            local_cvi.get_cvi(local_data, local_label)

    def test_error_batch_to_inc(self):
        """
        Tests that batch to incremental mode is not supported yet.
        """

        # Create some dummy 2D data
        dim = 2
        local_data = np.zeros((dim, dim))
        local_label = 0

        # Create a CVI and tell it that it is setup
        local_cvi = get_one_cvi()
        local_cvi._is_setup = True

        # Test that switching from batch to incremental is not supported
        with pytest.raises(ValueError):
            local_cvi.get_cvi(local_data, local_label)

    def test_error_batch_two(self):
        """
        Tests that batch mode requires more than two labels.
        """

        # Create some dummy data with only one unique label
        dim = 2
        local_data = np.zeros((dim, dim))
        local_labels = np.zeros(dim)

        # Create a CVI object
        local_cvi = get_one_cvi()

        # Test that batch mode requires more than two labels
        with pytest.raises(ValueError):
            local_cvi.get_cvi(local_data, local_labels)


class Test_sklearn_equivalence:
    """
    Pytest class that tests for the equivalence of CVI implementations that are shared with the scikit-learn package.
    """

    def test_CH(self, data: TestData):
        lg.info("--- COMPARING WITH SCIKIT-LEARN ---")

        for key, local_data in data.datasets.items():
            lg.info(f"Testing data: {key}")

            cvi_pairs = {
                "CH": {
                    "cvi": cvi.CH(),
                    "sklearn": skm.calinski_harabasz_score,
                }
            }

            for index, pair in cvi_pairs.items():
                # local_cvi = pair["cvi"]()
                cvi_cvi = pair["cvi"].get_cvi(local_data["samples"], local_data["labels"])
                cvi_sklearn = pair["sklearn"](local_data["samples"], local_data["labels"])

                lg.info(
                    f"CVI: {index}, "
                    f"cvi: {cvi_cvi:.5f}, "
                    f"sklearn: {cvi_sklearn:.5f},"
                )

                inline_test_diff(cvi_cvi, cvi_sklearn)

# class TestCompat:
#     """
#     Compat entries tests.
#     """

#     def test_v0_modules(self, data: TestData):
#         """
#         Unit test for the v0 iCVI modules.
#         """

#         for key, local_data in data.datasets.items():
#             lg.info(f"Testing data: {key}")
#             n_samples = data.count(key)

#             # v0 modules
#             i_cvis = [
#                 local_cvi() for local_cvi in cvi.compat.v0.MODULES
#             ]

#             # Iterate over every module
#             for local_cvi in i_cvis:
#                 # Iterate over every sample and label
#                 for ix in range(n_samples):
#                     # Grab a sample and label
#                     sample, label = get_sample(local_data, ix)
#                     # Update the cvi
#                     _ = local_cvi.update(sample, label)
