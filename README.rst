Celery Prometheus
=================

Add you own metrics to your celery backend.



Usage:

::

    app = Celery()
    add_prometheus_option(app)


Then, using Celery 4.


::
    
     export prometheus_multiproc_dir=/var/cache/my_celery_app
     celery worker -A sequoia_api_notif.backend --prometheus-collector-addr 0.0.0.0:6543


This will expose the metrics on 0.0.0.0:6543 of the host than can be scrapped by
prometheus.