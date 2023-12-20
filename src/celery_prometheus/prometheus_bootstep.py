"""Helper for celery."""
import logging
import os
from argparse import ArgumentParser
from typing import Any, Mapping, Optional, cast

from celery import VERSION as celery_version  # type: ignore
from celery import Celery
from prometheus_client import CollectorRegistry, start_http_server
from prometheus_client.multiprocess import MultiProcessCollector

log = logging.getLogger(__name__)


if celery_version.major < 5:
    from celery.signals import user_preload_options  # type: ignore

    @user_preload_options.connect
    def on_preload_parsed(options: Mapping[str, Any], **kwargs: Any) -> None:
        prometheus_collector_addr = options.get("prometheus_collector_addr")
        app = cast(Celery, kwargs["app"])
        attach_prometheus_registry(app, prometheus_collector_addr)


def add_prometheus_option(app: Celery) -> None:
    help = "Celery Prometheus Configuration."
    if celery_version.major < 5:

        def add_preload_arguments(parser: ArgumentParser) -> None:
            parser.add_argument(
                "--prometheus-collector-addr",
                default=os.getenv("CELERY_PROMETHEUS_COLLECTOR_ADDR"),
                help=help,
            )

        app.user_options["preload"].add(add_preload_arguments)
    else:
        from celery import bootsteps
        from click import Option

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
