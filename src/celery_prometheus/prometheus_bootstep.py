"""Helper for celery."""

import logging
import os
from typing import Any, Optional

from celery import Celery, bootsteps
from click import Option
from prometheus_client import CollectorRegistry, start_http_server
from prometheus_client.multiprocess import MultiProcessCollector

log = logging.getLogger(__name__)


def add_prometheus_option(app: Celery) -> None:
    help = "Celery Prometheus Configuration."

    app.user_options["preload"].add(
        Option(
            ["--prometheus-collector-addr"],
            required=False,
            help=help,
            default=os.getenv("CELERY_PROMETHEUS_COLLECTOR_ADDR"),
        )
    )

    class PrometheusBootstep(bootsteps.Step):
        def __init__(
            self,
            parent: bootsteps.Step,
            prometheus_collector_addr: str = "",
            **options: Any,
        ) -> None:
            attach_prometheus_registry(app, prometheus_collector_addr)

    app.steps["worker"].add(PrometheusBootstep)


def attach_prometheus_registry(app: Celery, prometheus_addr: Optional[str]) -> None:
    """Celery loader based on yaml file."""

    if prometheus_addr:
        registry = CollectorRegistry()
        MultiProcessCollector(registry)
        prom_addr, prom_port = prometheus_addr.rsplit(":")
        port = int(prom_port)
        start_http_server(port, prom_addr, registry)
