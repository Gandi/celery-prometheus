import importlib.metadata

from .prometheus_bootstep import add_prometheus_option

__version__ = importlib.metadata.version("celery-prometheus")

__all__ = ["add_prometheus_option"]
