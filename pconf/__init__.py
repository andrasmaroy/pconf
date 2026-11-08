"""Hierarchical python configuration with files, environment variables and command-line arguments."""

from importlib.metadata import version

from .pconf import Pconf

__version__ = version("pconf")

__all__ = ["Pconf", "__version__"]
