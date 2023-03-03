"""Helper for celery."""
import logging

from celery import VERSION as celery_version  # type: ignore
from celery import Celery
from prometheus_client import REGISTRY, start_http_server  # type: ignore
from prometheus_client.multiprocess import MultiProcessCollector  # type: ignore

log = logging.getLogger(__name__)


if celery_version.major < 5:
    from celery.signals import user_preload_options  # type: ignore

    @user_preload_options.connect
    def on_preload_parsed(options, **kwargs) -> None:
        prometheus_collector_addr = options.get("prometheus_collector_addr")
        app = kwargs["app"]
        attach_prometheus_registry(app, prometheus_collector_addr)


def add_prometheus_option(app) -> None:
    help = "Celery Prometheus Configuration."
    if celery_version.major < 5:
        def add_preload_arguments(parser):
            parser.add_argument("--prometheus-collector-addr", default=None, help=help)

        app.user_options["preload"].add(add_preload_arguments)
    else:
        from celery import bootsteps
        from click import Option

        app.user_options["preload"].add(
            Option(["--prometheus-collector-addr"], required=False, help=help)
        )

        class PrometheusBootstep(bootsteps.Step):
            def __init__(self, parent, prometheus_collector_addr: str = "", **options):
                attach_prometheus_registry(app, prometheus_collector_addr)

        app.steps["worker"].add(PrometheusBootstep)


def attach_prometheus_registry(app: Celery, prometheus_addr: str) -> None:
    """Celery loader based on yaml file."""

    if prometheus_addr:
        MultiProcessCollector(REGISTRY)
        prom_addr, prom_port = prometheus_addr.rsplit(":")
        port = int(prom_port)
        start_http_server(port, prom_addr, REGISTRY)
