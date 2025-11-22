import time
from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()
        return None

    def process_response(self, request, response):
        # Calculate request processing time
        total_time = time.time() - request.start_time

        # Log the request details
        log_data = {
            'method': request.method,
            'path': request.path,
            'status_code': response.status_code,
            'processing_time': total_time,
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'user': str(getattr(request, 'user', 'AnonymousUser')),
            'ip': request.META.get('REMOTE_ADDR', ''),
        }

        logger.info(
            f"{request.method} {request.path} {response.status_code} "
            f"in {total_time:.2f}s - User: {log_data['user']}"
        )

        return response