from typing import Any
from unittest.mock import Mock, patch

import pytest
from torch import Size, Tensor, equal, nn, optim, rand
from torchtest import assert_vars_change

from dataset2vec.config import Dataset2VecConfig
from dataset2vec.model import Dataset2Vec, FeedForward, ResidualBlock


@pytest.fixture
def sample_dataset2vec_config() -> Dataset2VecConfig:
    return Dataset2VecConfig(
        activation_cls=nn.ReLU,
        f_dense_hidden_size=32,
        f_res_hidden_size=32,
        f_res_n_layers=2,
        f_block_repetitions=1,
        f_out_size=64,
        g_layers_sizes=[64, 16, 8],
        h_dense_hidden_size=16,
        h_res_hidden_size=16,
        h_res_n_layers=2,
        h_block_repetitions=1,
        output_size=16,
    )


@pytest.fixture
def sample_model_input() -> tuple[Tensor, Tensor]:
    input_X = Tensor([[1, 2, 3], [4, 5, 6]])
    input_y = Tensor([[7, 8], [9, 10]])
    return (input_X, input_y)


@pytest.fixture
def sample_feature_target_pairs() -> Tensor:
    return Tensor(
        [
            [[1, 7], [4, 9]],
            [[1, 8], [4, 10]],
            [[2, 7], [5, 9]],
            [[2, 8], [5, 10]],
            [[3, 7], [6, 9]],
            [[3, 8], [6, 10]],
        ]
    )


@pytest.fixture
def sample_interdependency_encoding() -> Tensor:
    return Tensor([[5, 16], [5, 18], [7, 16], [7, 18], [9, 16], [9, 18]])


@pytest.fixture
def sample_joint_distribution_encoding() -> Tensor:
    return Tensor([42, 102])


@pytest.fixture
def sample_dataset_encoding() -> Tensor:
    return Tensor([14, 34])


def test_network_initialized_properly(
    sample_dataset2vec_config: Dataset2VecConfig,
) -> None:
    # Given
    model = Dataset2Vec(sample_dataset2vec_config)

    # Then
    # Check model params
    assert model.output_size == 16

    # Check f
    assert type(model.f) is nn.Sequential
    assert model.f[0].in_features == 2
    assert (
        model.f[0].out_features
        == sample_dataset2vec_config.f_dense_hidden_size
    )
    assert type(model.f[1]) is sample_dataset2vec_config.activation_cls
    assert type(model.f[2]) is ResidualBlock
    assert (
        model.f[2].input_size == sample_dataset2vec_config.f_dense_hidden_size
    )
    assert (
        model.f[2].output_size == sample_dataset2vec_config.f_dense_hidden_size
    )
    assert (
        model.f[3].in_features == sample_dataset2vec_config.f_dense_hidden_size
    )
    assert model.f[3].out_features == sample_dataset2vec_config.f_out_size

    # Check g
    assert type(model.g) is nn.Sequential
    assert model.g[0].in_features == sample_dataset2vec_config.f_out_size
    assert (
        model.g[0].out_features == sample_dataset2vec_config.g_layers_sizes[0]
    )
    assert type(model.g[1]) is sample_dataset2vec_config.activation_cls
    assert (
        model.g[2].in_features == sample_dataset2vec_config.g_layers_sizes[0]
    )
    assert (
        model.g[2].out_features == sample_dataset2vec_config.g_layers_sizes[1]
    )
    assert type(model.g[3]) is sample_dataset2vec_config.activation_cls
    assert (
        model.g[4].in_features == sample_dataset2vec_config.g_layers_sizes[1]
    )
    assert (
        model.g[4].out_features == sample_dataset2vec_config.g_layers_sizes[2]
    )
    assert type(model.g[5]) is sample_dataset2vec_config.activation_cls

    # Check h
    assert type(model.h) is nn.Sequential
    assert (
        model.h[0].in_features == sample_dataset2vec_config.g_layers_sizes[2]
    )
    assert (
        model.h[0].out_features
        == sample_dataset2vec_config.h_dense_hidden_size
    )
    assert type(model.h[1]) is sample_dataset2vec_config.activation_cls
    assert type(model.h[2]) is ResidualBlock
    assert (
        model.h[2].input_size == sample_dataset2vec_config.h_dense_hidden_size
    )
    assert (
        model.h[2].output_size == sample_dataset2vec_config.h_dense_hidden_size
    )
    assert (
        model.h[3].in_features == sample_dataset2vec_config.h_dense_hidden_size
    )
    assert model.h[3].out_features == sample_dataset2vec_config.output_size


def test_all_dataset2vec_params_are_trained(
    sample_model_input: Tensor, utils: Any
) -> None:
    # Given
    input_X, input_y = sample_model_input
    model = Dataset2Vec()

    # When
    test_adapter = utils.NetworkTestAdapter(model, input_y)

    # Then
    assert_vars_change(
        model=test_adapter,
        optim=optim.Adam(test_adapter.parameters()),
        loss_fn=lambda y, _: y.sum(),
        batch=(input_X, Tensor(0)),
        device="cpu:0",
    )


def test_forward_passes() -> None:
    # Given
    input = rand(20, 5), rand(20, 1)
    model = Dataset2Vec()

    # When
    encoding = model(*input)

    # Then
    assert encoding.shape == Size([16])


def test_forward_passes_when_one_dimensional_y() -> None:
    # Given
    input = rand(20, 5), rand(20)
    model = Dataset2Vec()

    # When
    encoding = model(*input)

    # Then
    assert encoding.shape == Size([16])


def test_forward_returns_encoding_of_the_same_dimensionality() -> None:
    # Given
    input_1 = rand(20, 5), rand(20, 2)
    input_2 = rand(10, 7), rand(10, 1)
    model = Dataset2Vec()

    # When
    encoding_1 = model(*input_1)
    encoding_2 = model(*input_2)

    # Then
    assert encoding_1.shape == Size([model.output_size])
    assert encoding_1.shape == encoding_2.shape


def test_forward_fails_when_incorrect_input_dimensionality() -> None:
    # Given
    input = rand(20, 5), rand(10, 2)
    model = Dataset2Vec()

    # Then
    with pytest.raises(AssertionError):
        model(*input)


def test__generate_feature_target_pairs(
    sample_model_input: Tensor, sample_feature_target_pairs: Tensor
) -> None:
    # Given
    input_X, input_y = sample_model_input
    model = Dataset2Vec()

    # When
    feature_target_pairs = model._Dataset2Vec__generate_feature_target_pairs(
        input_X, input_y
    )

    # Then
    assert feature_target_pairs.shape == (6, 2, 2)
    assert equal(
        feature_target_pairs,
        sample_feature_target_pairs,
    )


@patch("torch.nn.Sequential.forward")
def test__generate_interdependency_encoding(
    forward_mock: Mock,
    sample_feature_target_pairs: Tensor,
    sample_interdependency_encoding: Tensor,
) -> None:
    # Given
    forward_mock.side_effect = lambda X: X * 2
    model = Dataset2Vec()

    # When
    interdependency_encoding = (
        model._Dataset2Vec__generate_interdependency_encoding(
            sample_feature_target_pairs
        )
    )

    # Then
    assert interdependency_encoding.shape == (6, 2)
    assert equal(interdependency_encoding, sample_interdependency_encoding)


@patch("torch.nn.Sequential.forward")
def test__generate_joint_distributions_encoding(
    forward_mock: Mock,
    sample_interdependency_encoding: Tensor,
    sample_joint_distribution_encoding: Tensor,
) -> None:
    # Given
    forward_mock.side_effect = lambda X: X * 6
    model = Dataset2Vec()

    # When
    joint_distribution_encoding = (
        model._Dataset2Vec__generate_joint_distributions_encoding(
            sample_interdependency_encoding
        )
    )

    # Then
    assert joint_distribution_encoding.shape == Size([2])
    assert equal(
        joint_distribution_encoding, sample_joint_distribution_encoding
    )


@patch("torch.nn.Sequential.forward")
def test__generate_dataset_encoding(
    forward_mock: Mock,
    sample_joint_distribution_encoding: Tensor,
    sample_dataset_encoding: Tensor,
) -> None:
    # Given
    forward_mock.side_effect = lambda X: X // 3
    model = Dataset2Vec()

    # When
    dataset_encoding = model._Dataset2Vec__generate_dataset_encoding(
        sample_joint_distribution_encoding
    )

    # Then
    assert dataset_encoding.shape == Size([2])
    assert equal(dataset_encoding, sample_dataset_encoding)


def test__feed_forward_initialized_properly() -> None:
    # Given
    input_size = 32
    hidden_size = 32
    n_layers = 4
    output_size = 32
    activation_cls = nn.ReLU

    # When
    model = FeedForward(
        input_size, hidden_size, n_layers, output_size, activation_cls
    )

    # Then
    assert model.block is not None
    assert sum(map(lambda p: len(p.reshape(-1)), model.parameters())) == 4224
    assert (
        type(model.block[0]) is nn.Linear
        and model.block[0].in_features == input_size
        and model.block[0].out_features == hidden_size
    )
    assert type(model.block[1]) is activation_cls
    assert (
        type(model.block[2]) is nn.Linear
        and model.block[2].in_features == hidden_size
        and model.block[2].out_features == hidden_size
    )
    assert type(model.block[3]) is activation_cls
    assert (
        type(model.block[4]) is nn.Linear
        and model.block[4].in_features == hidden_size
        and model.block[4].out_features == output_size
    )
    assert type(model.block[5]) is activation_cls
    assert (
        type(model.block[6]) is nn.Linear
        and model.block[6].in_features == hidden_size
        and model.block[6].out_features == output_size
    )
    assert type(model.block[7]) is activation_cls


def test_all_feed_forward_params_are_trained() -> None:
    # Given
    input = rand(8, 16)
    model = FeedForward(16, 32, 3, 1, nn.Sigmoid)

    # Then
    assert_vars_change(
        model=model,
        optim=optim.Adam(model.parameters()),
        loss_fn=lambda y, _: y.sum(),
        batch=(input, Tensor(0)),
        device="cpu:0",
    )


def test_all_residual_params_are_trained() -> None:
    # Given
    input = rand(8, 16)
    model = ResidualBlock(16, 32, 3, 1, nn.Sigmoid)

    # Then
    assert_vars_change(
        model=model,
        optim=optim.Adam(model.parameters()),
        loss_fn=lambda y, _: y.sum(),
        batch=(input, Tensor(0)),
        device="cpu:0",
    )


@patch("dataset2vec.model.FeedForward.forward")
def test_all_residual_skip_connection_works(
    superclass_forward_mock: Mock,
) -> None:
    # Given
    superclass_forward_mock.return_value = 0
    input = rand(8, 16)
    model = ResidualBlock(16, 32, 3, 1, nn.Sigmoid)

    # When
    model_output = model(input)

    # Then
    assert equal(input, model_output)
