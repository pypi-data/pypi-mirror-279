from pathlib import Path

from pytorch_lightning import Trainer

from dataset2vec import (
    Dataset2Vec,
    Dataset2VecLoader,
    RepeatableDataset2VecLoader,
)

train_loader = Dataset2VecLoader(Path("data/train"))  # Path with .csv files
val_loader = RepeatableDataset2VecLoader(
    Path("data/val")
)  # Path with .csv files

model = Dataset2Vec()

trainer = Trainer(
    max_epochs=2, log_every_n_steps=1, default_root_dir="output_logs"
)  # output of the training will be stored in output_logs

trainer.fit(model, train_loader, val_loader)
