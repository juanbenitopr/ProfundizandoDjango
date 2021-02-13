import json
import logging
from typing import Callable

from rest_framework.response import Response


class LoggingMiddleware:

    def __init__(self, get_response: Callable):
        self.request_logger = logging.getLogger('middleware.requests')
        self.response_logger = logging.getLogger('middleware.response')
        self.get_response = get_response

    def __call__(self, request):
        self.request_logger.info('request received',
                                 extra={'user': json.dumps({'id': request.user.id, 'username': request.user.username}),
                                        'body': json.dumps(request.POST),
                                        'path': request.path
                                        })

        response: Response = self.get_response(request)

        if response.status_code > 299:
            self.response_logger.info('response sent',
                                      extra={'user': json.dumps(
                                          {'id': request.user.id, 'username': request.user.username}),
                                             'path': request.path,
                                             'status': response.status_code,
                                             'body': json.dumps(response.__dict__.get('data', {}))})

        return response
