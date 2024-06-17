from typing import Any, Type

import pytest
from torch import Tensor, nn

from dataset2vec.model import Dataset2Vec


class Utils:
    class NetworkTestAdapter(nn.Module):

        def __init__(self, model: Dataset2Vec, y: Tensor):
            super().__init__()
            self.model = model
            self.y = y

        def forward(self, X: Tensor) -> Any:
            return self.model(X, self.y)


@pytest.fixture(scope="session")
def utils() -> Type[Utils]:
    return Utils
