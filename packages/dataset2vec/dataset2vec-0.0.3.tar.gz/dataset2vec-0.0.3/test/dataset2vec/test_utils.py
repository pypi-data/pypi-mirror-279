from typing import Any
from unittest.mock import Mock, patch

import numpy as np
import pandas as pd
import pytest
from torch import Tensor

from dataset2vec.utils import DataUtils, Validators


def test_preprocessing_pipeline() -> None:
    # Given
    pipeline = DataUtils.get_preprocessing_pipeline()
    data = pd.DataFrame(
        {"col1": [1, 2, 3], "col2": [1, None, 3], "col3": ["A", "B", "A"]}
    )
    expected_df = pd.DataFrame(
        {
            "pipeline-1__col3_A": [1, 0, 1],
            "pipeline-1__col3_B": [0, 1, 0],
            "pipeline-2__col1": [0, 0.5, 1],
            "pipeline-2__col2": [0, 0.5, 1],
        }
    )

    # When
    preprocessed_data = pipeline.fit_transform(data)

    # Then
    assert np.isclose(expected_df.values, preprocessed_data).all()


@patch("numpy.random.uniform")
def test_sample_random_subset_when_int_passed(uniform_mock: Mock) -> None:
    # Given
    uniform_mock.return_value = np.array([0.3, 0.2, 0.6, 0.4])
    expected_subset = np.array([0, 1, 3])

    # When
    actual_subset = DataUtils.sample_random_subset(4)

    # Then
    assert (actual_subset == expected_subset).all()


@patch("numpy.random.uniform")
def test_sample_random_subset_when_array_passed(uniform_mock: Mock) -> None:
    # Given
    uniform_mock.return_value = np.array([0.3, 0.2, 0.6, 0.4])
    expected_subset = np.array([1, 3, 7])

    # When
    random_subset = DataUtils.sample_random_subset(np.array([1, 3, 5, 7]))

    # Then
    assert (random_subset == expected_subset).all()


def test_index_tensor_using_lists() -> None:
    # Given
    tensor = Tensor(
        [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
    )
    rows_idx = np.array([1, 2])
    cols_idx = np.array([2, 3])
    expected_indexed_tensor = Tensor([[7, 8], [11, 12]])

    # When
    actual_indexed_tensor = DataUtils.index_tensor_using_lists(
        tensor, rows_idx, cols_idx
    )

    # Then
    print(actual_indexed_tensor)
    assert (actual_indexed_tensor == expected_indexed_tensor).all()


def test_is_positive_when_proper_input() -> None:
    # Given
    input = 1

    # Then
    Validators.is_positive(input)


def test_is_positive_when_improper_input() -> None:
    # Given
    input = -11

    # Then
    with pytest.raises(AssertionError):
        Validators.is_positive(input)


def test_non_negative_when_proper_input() -> None:
    # Given
    input = 0

    # Then
    Validators.non_negative(input)


def test_non_negative_when_improper_input() -> None:
    # Given
    input = -11

    # Then
    with pytest.raises(AssertionError):
        Validators.non_negative(input)


def test_all_elements_positive_when_proper_input() -> None:
    # Given
    input = [1, 2, 3]

    # Then
    Validators.all_elements_positive(input)


def test_all_elements_positive_when_improper_input() -> None:
    # Given
    input = [1, -22, 3]

    # Then
    with pytest.raises(AssertionError):
        Validators.all_elements_positive(input)


def test_non_empty_when_proper_input() -> None:
    # Given
    input = [1, 2, 3]

    # Then
    Validators.non_empty(input)


def test_non_empty_when_improper_input() -> None:
    # Given
    input: list[Any] = []

    # Then
    with pytest.raises(AssertionError):
        Validators.non_empty(input)
