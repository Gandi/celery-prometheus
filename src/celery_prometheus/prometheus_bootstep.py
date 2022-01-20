"""Helper for celery."""
import logging

from celery import VERSION as celery_version
from celery import Celery
from prometheus_client import REGISTRY, start_http_server
from prometheus_client.multiprocess import MultiProcessCollector

log = logging.getLogger(__name__)


if celery_version.major < 5:

    from celery.signals import user_preload_options

    @user_preload_options.connect
    def on_preload_parsed(options, **kwargs):
        prometheus_collector_addr = options.get("prometheus_collector_addr")
        app = kwargs["app"]
        attach_prometheus_registry(app, prometheus_collector_addr)


def add_prometheus_option(app):

    help = "Celery Prometheus Configureation."
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
        ip, port = prometheus_addr.rsplit(":")
        ip = int(ip)
        port = int(port)
        start_http_server(port, ip, REGISTRY)
