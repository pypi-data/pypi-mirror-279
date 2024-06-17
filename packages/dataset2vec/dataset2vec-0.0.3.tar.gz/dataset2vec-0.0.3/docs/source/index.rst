Welcome to Dataset2Vec's documentation!
=======================================

.. toctree::
   :maxdepth: 1

   modules/model
   modules/data
   modules/config

Introduction
=======================================
This package aims to implement the approach proposed in `Dataset2Vec: Learning Dataset Meta-Features`
by `Jomaa et al`. This package makes the training Dataset2Vec dataset encoder much more approachable
by providing an API that is compatible with ``pytorch-lightning``'s ``trainer`` API. The output logs
including tensorboard and checkpoints are stored in ``lightning_logs`` or in ``default_root_dir``
from ``pytroch_lightning.Trainer`` if specified.

Example
=======================================
Below you can find example of the usage of the package.

.. literalinclude:: ../../example.py
   :language: python