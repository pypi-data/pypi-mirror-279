import shutil
from typing import Generator

import pytest
import torch
from pytorch_lightning import Trainer

from dataset2vec.config import OptimizerConfig
from dataset2vec.data import Dataset2VecLoader, RepeatableDataset2VecLoader
from dataset2vec.model import Dataset2Vec


@pytest.fixture
def train_output_path() -> Generator[str, None, None]:
    path = "test_logs"
    yield path
    shutil.rmtree(path)


def test_dummy_training_does_not_fail(train_output_path: str) -> None:
    # Given
    train_loader = Dataset2VecLoader(
        [
            torch.rand((16, 7)),
            torch.rand((16, 7)),
            torch.rand((16, 7)),
        ],
        batch_size=4,
        n_batches=2,
    )
    val_loader = RepeatableDataset2VecLoader(
        [
            torch.rand((16, 7)),
            torch.rand((16, 7)),
            torch.rand((16, 7)),
        ],
        batch_size=4,
        n_batches=2,
    )
    model = Dataset2Vec(optimizer_config=OptimizerConfig(learning_rate=1e-3))
    trainer = Trainer(
        max_epochs=2, log_every_n_steps=1, default_root_dir=train_output_path
    )

    # Then
    trainer.fit(model, train_loader, val_loader)
