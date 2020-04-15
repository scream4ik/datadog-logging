import logging
import time

from django.conf import settings

logger = logging.getLogger(__name__)


class Log400ResponseMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if getattr(settings, 'DATADOG_ENABLE_LOG_400', False):
            status_code = getattr(response, 'status_code', None)
            if status_code and 400 <= status_code < 500:
                logger.info(
                    f'Path: {request.path}, '
                    f'Code: {response.status_code}, '
                    f'Reason: {response.content}'
                )

        return response


class StatsMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration_ms = (time.time() - start_time) * 1000

        if getattr(settings, 'DATADOG_ENABLE_REQUEST_STATS', False):
            logger.info(
                f'Request duration: {duration_ms} ms, '
                f'Path: {request.path}'
            )

        return response
