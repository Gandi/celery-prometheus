# Celery Prometheus

This module expose the Prometheus HTTP server to expose metrics of your Celery backends.

To install `celery-prometheus` with pip, use the command:

```
pip install celery-prometheus
```

With Poetry:

```
poetry add celery-prometheus
```

## Usage

To setup `celery-prometheus` to your backend, simply call the method `add_prometheus_option`
after the init of the `Celery` object.

Example:

```python

from celery import Celery
from celery_prometheus import add_prometheus_option

app = Celery()
add_prometheus_option(app)

# Rest of your code ...

```

Before starting your backend, you will need to expose the `PROMETHEUS_MULTIPROC_DIR` environment
variable to indicate which folder the Prometheus Client will use to store the metrics
(see [Multiprocess Mode (E.g. Gunicorn) of the Promehteus Client documentation](https://github.com/prometheus/client_python#multiprocess-mode-eg-gunicorn)).

To start and expose the Prometheus HTTP Server, you need to use the `--prometheus-collector-addr`
argument when starting your Celery backend:

```bash
export PROMETHEUS_MULTIPROC_DIR=/var/cache/my_celery_app
celery worker -A my_celery_backend.backend --prometheus-collector-addr 0.0.0.0:6543
```

Now that your backend is started, you can configure your Prometheus scrappers to scrappe your
Celery backend.

## Contributions

This project is open to external contributions. Feel free to submit us a
[Pull request](https://github.com/Gandi/celery-prometheus/pulls) if you want to contribute and
improve with us this project.

In order to maintain an overall good code quality, this project use the following tools:

 - [Black](https://github.com/psf/black)
 - [Isort](https://github.com/PyCQA/isort)
 - [Flake8](https://flake8.pycqa.org/en/latest/)

Linting and formatting tools are configured to match the [current default rules of Black](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html).

We also use [Mypy](https://mypy.readthedocs.io/en/stable/) as a static type checker.

Please ensure to run these tools before commiting and submiting a Pull request. In case one of
these mentionned tools report an error, the CI will automatically fail.

If you're making your first contribution to this project, please add your name to the
[contributors list](CONTRIBUTORS.txt).

## License

This project is released by [Gandi.net](https://www.gandi.net/en) tech team under the
[BSD-3 license](LICENSE).
