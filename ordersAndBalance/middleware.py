import uuid
import structlog 

class StructlogLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = str(uuid.uuid4())

        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
        )

        response = self.get_response(request)

        if (hasattr(request, "user")) and request.user.is_authenticated:
            structlog.contextvars.bind_contextvars(user_id=request.user.id)

        return response