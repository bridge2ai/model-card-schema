"""Model Card Schema - LinkML implementation of Model Cards for Model Reporting."""

from . import datamodel

__all__ = ["datamodel"]

try:
    from ._version import __version__
except ImportError:
    __version__ = "unknown"
