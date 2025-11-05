from django.utils.deprecation import MiddlewareMixin

class RequestDebugMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print(f"🧭 Incoming: {request.path}")
        return None
