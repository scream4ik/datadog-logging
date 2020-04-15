import logging
import requests

from django.conf import settings


class DatadogLogHandler(logging.StreamHandler):
    """
    Log handler that store logs in Datadog
    """

    def emit(self, record):
        msg = self.format(record)

        json = {
            'message': msg,
            'ddsource': settings.DATADOG_SERVICE_NAME,
            'ddtags': f'env:{settings.DATADOG_ENV}',
            'service': settings.DATADOG_SERVICE_NAME,
            'host': settings.DATADOG_SERVICE_NAME
        }

        try:
            requests.post(
                f'https://http-intake.logs.datadoghq.{DATADOG_DOMAIN_ZONE}'
                f'/v1/input/{settings.DATADOG_API_KEY}',
                json=json
            )
        except requests.exceptions.Timeout:
            pass
