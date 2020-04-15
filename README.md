# Logging loggers message to Datadog using HTTP API

## For now support only Django and celery

### Basic Installation
```
pip install https://github.com/scream4ik/datadog-logging/archive/master.zip
```

### Requirements

- requests

### Django configuration
- Add `datadog_logging.django` to INSTALLED_APPS
- Add `datalog_logging.django.handlers.DatadogLogHandler` to Django `LOGGING`

Example:
```
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'datadog_logging': {
            'level': 'DEBUG',
            'class': 'datadog_logging.django.handlers.DatadogLogHandler'
        }
    },
    'root': {
        'handlers': ['console', 'datadog_logging'],
        'level': 'WARNING',
    },
}
```

#### Also you can add middleware:

- `datadog_logging.django.middlewares.Log400ResponseMiddleware` - logging 4xx requests to Datadog
- `datadog_logging.django.middlewares.StatsMiddleware` - logging request path and duration to Datadog

#### Configuration

- `DATADOG_SERVICE_NAME` - the service name to be used for this program. For example: `backend_api`
- `DATADOG_ENV` - set an application’s environment e.g. `prod`, `pre-prod`, `staging`
- `DATADOG_DOMAIN_ZONE` - `com` or `eu`
- `DATADOG_API_KEY` - Datadog API key
- `DATADOG_ENABLE_REQUEST_STATS` - `True` or `False`. Enable logging requests path and duration
- `DATADOG_ENABLE_LOG_400` - `True` or `False`. Enable logging 4xx requests

#### Celery

In your `celery.py`, or where you created celery app, you need add:
```
from celery.signals import after_setup_logger
from datalog_logging.django.handlers import DatadogLogHandler


@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    formatter = logging.Formatter(
        '%(levelname)s %(asctime)s %(module)s '
        '%(process)d %(thread)d %(message)s'
    )
    handler = DatadogLogHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
```
