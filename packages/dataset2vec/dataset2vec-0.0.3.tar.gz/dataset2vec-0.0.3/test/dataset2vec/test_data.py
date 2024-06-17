from pathlib import Path
from unittest.mock import Mock, patch

import numpy as np
import pandas as pd
import pytest
import torch

from dataset2vec.data import Dataset2VecLoader, RepeatableDataset2VecLoader
from dataset2vec.utils import InvalidDataTypeException


@patch("dataset2vec.data.DataUtils.sample_random_subset")
@patch("numpy.random.choice")
def test__sample_batch_idx(
    np_random_choice_mock: Mock, sample_random_subset_mock: Mock
) -> None:
    # Given
    np_random_choice_mock.return_value = np.array([0, 2, 4])
    sample_random_subset_mock.return_value = np.array([1, 2])
    X, y = torch.rand((10, 4)), torch.rand(10, 1)

    # When
    loader = Dataset2VecLoader([])
    rows_idx, features_idx, targets_idx = (
        loader._Dataset2VecLoader__sample_batch_idx(X, y)  # type: ignore
    )

    # Then
    assert (rows_idx == np.array([0, 2, 4])).all()
    assert (features_idx == np.array([1, 2])).all()
    assert (targets_idx == np.array([1, 2])).all()


@patch(
    "dataset2vec.data.Dataset2VecLoader._Dataset2VecLoader__sample_batch_idx"
)
def test__generate_dataset_subsample(sample_batch_idx_mock: Mock) -> None:
    # Given
    X1, y1 = torch.rand((10, 8)), torch.rand(10, 1)
    X2, y2 = torch.rand((10, 8)), torch.rand(10, 1)
    loader = Dataset2VecLoader([])
    loader.Xs = [X1, X2]
    loader.ys = [y1, y2]
    sample_batch_idx_mock.return_value = (
        np.array([1, 3, 5]),
        np.array([1, 3]),
        np.array([0]),
    )

    # When
    subsample_X, subsample_y = (
        loader._Dataset2VecLoader__generate_dataset_subsample(1)  # type: ignore # noqa: E501
    )

    # Then
    assert subsample_X.shape == (3, 2)
    assert torch.allclose(subsample_X, X2[[1, 3, 5]].T[[1, 3]].T)
    assert subsample_y.shape == (3, 1)
    assert torch.allclose(subsample_y, y2[[1, 3, 5]])


@patch("numpy.random.uniform")
def test__get_random_datasets_indices_from_one_dataset(
    unform_mock: Mock,
) -> None:
    # Given
    loader = Dataset2VecLoader([])
    loader.n_datasets = 10
    unform_mock.return_value = 0.8

    # When
    idx_1, idx_2 = loader._Dataset2VecLoader__get_random_datasets_indices()  # type: ignore # noqa: E501

    # Then
    assert idx_1 == idx_2
    assert idx_1 < 10 and idx_1 >= 0


@patch("numpy.random.uniform")
def test__get_random_datasets_indices_from_two_datasets(
    unform_mock: Mock,
) -> None:
    # Given
    loader = Dataset2VecLoader([])
    loader.n_datasets = 10
    unform_mock.return_value = 0.4

    # When
    idx_1, idx_2 = loader._Dataset2VecLoader__get_random_datasets_indices()  # type: ignore # noqa: E501

    # Then
    assert idx_1 != idx_2
    assert idx_1 < 10 and idx_1 >= 0
    assert idx_2 < 10 and idx_2 >= 0


@patch(
    "dataset2vec.data.Dataset2VecLoader"
    "._Dataset2VecLoader__generate_dataset_subsample"
)
@patch(
    "dataset2vec.data.Dataset2VecLoader"
    "._Dataset2VecLoader__get_random_datasets_indices"
)
def test__get_single_example(
    get_random_datasets_indices_mock: Mock,
    generate_dataset_subsample_mock: Mock,
) -> None:
    # Given
    get_random_datasets_indices_mock.return_value = np.array([1, 2])
    sample_X, sample_y = torch.rand(10, 4), torch.rand(10, 1)
    generate_dataset_subsample_mock.return_value = (sample_X, sample_y)
    loader = Dataset2VecLoader([])

    # When
    X1, y1, X2, y2, label = loader._Dataset2VecLoader__get_single_example()  # type: ignore # noqa: E501

    # Then
    assert torch.allclose(X1, sample_X)
    assert torch.allclose(X2, sample_X)
    assert torch.allclose(y1, sample_y)
    assert torch.allclose(y2, sample_y)
    assert label == 0


@patch(
    "dataset2vec.data.Dataset2VecLoader._Dataset2VecLoader__get_single_example"
)
def test__get_batch(get_single_example_mock: Mock) -> None:
    # Given
    sample_batch = (torch.rand(10, 4), (10, 1), (5, 5), (5, 1), 1)
    get_single_example_mock.return_value = sample_batch
    loader = Dataset2VecLoader([], batch_size=32)

    # When
    batch = loader._Dataset2VecLoader__get_batch()  # type: ignore

    # Then
    assert len(batch) == 32
    assert all([obs == sample_batch for obs in batch])


def test__normalize_type_to_pandas_when_pandas() -> None:
    # Given
    df = pd.DataFrame(np.random.uniform(size=(10, 4)))
    loader = Dataset2VecLoader([])

    # When
    output = loader._Dataset2VecLoader__normalize_type_to_pandas(df)  # type: ignore # noqa: E501

    # Then
    assert isinstance(output, pd.DataFrame)
    assert output.equals(df)


def test__normalize_type_to_pandas_when_numpy() -> None:
    # Given
    arr = np.random.uniform(size=(10, 4))
    loader = Dataset2VecLoader([])

    # When
    output = loader._Dataset2VecLoader__normalize_type_to_pandas(arr)  # type: ignore # noqa: E501

    # Then
    assert isinstance(output, pd.DataFrame)
    assert (arr == output.values).all()


def test__normalize_type_to_pandas_when_tensor() -> None:
    # Given
    arr = torch.rand(10, 4)
    loader = Dataset2VecLoader([])

    # When
    output = loader._Dataset2VecLoader__normalize_type_to_pandas(arr)  # type: ignore # noqa: E501

    # Then
    assert isinstance(output, pd.DataFrame)
    assert (arr.numpy() == output.values).all()


def test__normalize_type_to_pandas_when_improper_type() -> None:
    # Given
    arr = ["1", "2", "3"]
    loader = Dataset2VecLoader([])

    # Then
    with pytest.raises(InvalidDataTypeException):
        loader._Dataset2VecLoader__normalize_type_to_pandas(arr)  # type: ignore # noqa: E501


def test__convert_numpy_to_torch_when_invalid_type_passed() -> None:
    # Given
    arr = ["1", "2", "3"]
    loader = Dataset2VecLoader([])

    # Then
    with pytest.raises(InvalidDataTypeException):
        loader._Dataset2VecLoader__convert_numpy_to_torch(arr)  # type: ignore # noqa: E501


def test__convert_numpy_to_torch_when_float_array_passed() -> None:
    # Given
    arr = np.random.uniform(size=(10, 4))
    loader = Dataset2VecLoader([])

    # When
    output = loader._Dataset2VecLoader__convert_numpy_to_torch(arr)  # type: ignore # noqa: E501

    # Then
    assert output.dtype == torch.float
    assert (output.numpy() == arr.astype(np.float32)).all()


@patch("pandas.read_csv")
@patch("sklearn.pipeline.Pipeline.fit_transform")
def test__read_data_if_needed_when_path_list_passed(
    fit_transform_mock: Mock,
    read_csv_mock: Mock,
) -> None:
    # Given
    output_data = np.random.uniform(size=(10, 4))
    read_csv_mock.return_value = pd.DataFrame(output_data)
    fit_transform_mock.side_effect = lambda X: X

    # When
    loader = Dataset2VecLoader([Path("path1"), Path("path2"), Path("path3")])

    # Then
    assert read_csv_mock.call_count == 3
    assert all(
        (
            torch.isclose(
                X, torch.from_numpy(output_data[:, :-1]).type(torch.float32)
            ).all()
        )
        for X in loader.Xs
    )
    assert all(
        torch.isclose(
            y,
            torch.from_numpy(output_data[:, -1])
            .reshape(-1, 1)
            .type(torch.float32),
        ).all()
        for y in loader.ys
    )


def test__setup_xs() -> None:
    # Given
    sample_data = pd.DataFrame(
        {
            "col1": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
            "col2": ["A", "B", "A", "A", "B", "B", "B", "A"],
            "col3": [0, 1, 0, 1, 0, 0, 0, 1],
        },
    )

    # When
    loader = Dataset2VecLoader([sample_data])

    # Then
    assert len(loader.Xs) == 1
    assert isinstance(loader.Xs[0], torch.Tensor)
    assert (loader.Xs[0][:, 2].max() - 1).abs() <= 1e-6
    assert (loader.Xs[0][:, 2].min()).abs() <= 1e-1
    assert (loader.Xs[0][:, 0] == torch.Tensor([1, 0, 1, 1, 0, 0, 0, 1])).all()
    assert (loader.Xs[0][:, 1] == torch.Tensor([0, 1, 0, 0, 1, 1, 1, 0])).all()


def test__setup_ys() -> None:
    # Given
    sample_data = pd.DataFrame(
        {
            "col1": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
            "col2": ["A", "B", "A", "A", "B", "B", "B", "A"],
            "col3": [0, 1, 0, 1, 0, 0, 0, 1],
        },
    )

    # When
    loader = Dataset2VecLoader([sample_data])

    # Then
    assert len(loader.ys) == 1
    assert isinstance(loader.ys[0], torch.Tensor)
    assert loader.ys[0].shape == (8, 1)
    assert (
        loader.ys[0] == torch.Tensor([[0], [1], [0], [1], [0], [0], [0], [1]])
    ).all()


@patch("dataset2vec.data.Dataset2VecLoader._Dataset2VecLoader__get_batch")
def test__loader_returns_proper_number_of_batches(
    get_batch_mock: Mock,
) -> None:
    # Given
    get_batch_mock.return_value = ()
    loader = Dataset2VecLoader([], n_batches=100)

    # When
    batches = list(loader)

    # Then
    assert len(batches) == 100


@patch(
    "dataset2vec.data.Dataset2VecLoader._Dataset2VecLoader__get_single_example"
)
def test__loader_returns_properly_sized_batch(
    get_single_example_mock: Mock,
) -> None:
    # Given
    get_single_example_mock.return_value = ()
    loader = Dataset2VecLoader([], batch_size=32)

    # When
    batches = list(loader)

    # Then
    assert len(batches[0]) == 32


def test_repeatable_loader_returns_repeatable_output() -> None:
    # Given
    loader = RepeatableDataset2VecLoader([torch.rand(8, 8), torch.rand(8, 10)])

    # When
    batches_1 = list(loader)
    batches_2 = list(loader)

    # Then
    assert len(batches_1) == 100
    assert len(batches_2) == 100
    assert len(batches_1[0]) == 32
    assert len(batches_2[0]) == 32
    assert all(
        [
            [
                (o1[0] == o2[0]).all()
                and (o1[1] == o2[1]).all()
                and (o1[2] == o2[2]).all()
                and (o1[3] == o2[3]).all()
                and (o1[4] == o2[4])
                for o1, o2 in zip(b1, b2)
            ]
            for b1, b2 in zip(batches_1, batches_2)
        ]
    )
