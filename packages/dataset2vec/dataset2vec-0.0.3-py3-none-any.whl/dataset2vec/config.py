from typing import Annotated, Type

from pydantic import BaseModel, Field
from pydantic.functional_validators import AfterValidator
from torch import nn
from torch.optim import Adam, Optimizer

from dataset2vec.utils import Validators


class Dataset2VecConfig(BaseModel):
    """Configuration of the Dataset2Vec encoder"""

    activation_cls: Type[nn.Module] = Field(default=nn.ReLU)
    """Class of the activation function used in entire network."""
    f_dense_hidden_size: Annotated[
        int, AfterValidator(Validators.is_positive)
    ] = 32
    """Size of the hidden layers of the first stage."""
    f_res_hidden_size: Annotated[
        int, AfterValidator(Validators.is_positive)
    ] = 32
    """Size of the hidden layers of the residual blocks of the first stage."""
    f_res_n_layers: Annotated[int, AfterValidator(Validators.is_positive)] = 3
    """Number of the layers of the residual block of the first stage."""
    f_block_repetitions: Annotated[
        int, AfterValidator(Validators.is_positive)
    ] = 7
    """Number of building blocks of the first stage."""
    f_out_size: Annotated[int, AfterValidator(Validators.is_positive)] = 32
    """Dimensionality of the output of the first starge."""
    g_layers_sizes: Annotated[
        list[int],
        AfterValidator(Validators.all_elements_positive),
        AfterValidator(Validators.non_empty),
    ] = [32, 16, 8]
    """Sizes of the layers of the feed forward network in the second stage."""
    h_dense_hidden_size: Annotated[
        int, AfterValidator(Validators.is_positive)
    ] = 16
    """Size of the hidden layers of the feed forward net of the third stage."""
    h_res_hidden_size: Annotated[
        int, AfterValidator(Validators.is_positive)
    ] = 16
    """Size of the hidden layers of the residual blocks of the third stage."""
    h_res_n_layers: Annotated[int, AfterValidator(Validators.is_positive)] = 3
    """Number of layers of the residual block of the third stage."""
    h_block_repetitions: Annotated[
        int, AfterValidator(Validators.is_positive)
    ] = 3
    """Number of building blocks of the third stage."""
    output_size: Annotated[int, AfterValidator(Validators.is_positive)] = 16
    """Output dimensionality of the encoder."""


class OptimizerConfig(BaseModel):
    """Configuration of the Dataset2Vec training"""

    gamma: Annotated[float, AfterValidator(Validators.is_positive)] = 1
    """Scaling parameter for the calculation of the probability."""
    optimizer_cls: Type[Optimizer] = Adam
    """Class of the optimizer."""
    learning_rate: Annotated[float, AfterValidator(Validators.is_positive)] = (
        1e-4
    )
    """Learning rate."""
    weight_decay: Annotated[float, AfterValidator(Validators.non_negative)] = (
        1e-4
    )
    """Weight decay."""
