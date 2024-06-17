import os
import sys

sys.path.insert(0, os.path.abspath("../.."))

project = "Dataset2Vec"
copyright = "2024, Antoni Zajko"
author = "Antoni Zajko"
release = "0.0.1"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]

exclude_patterns: list[str] = []

autodoc_inherit_docstrings = False

html_theme = "sphinx_rtd_theme"
pygments_style = "sphinx"
