import os
from django.http import FileResponse, HttpResponse
from django.views import View
from django.conf import settings


class FrontendAppView(View):
    def get(self, request, *args, **kwargs):
        index_path = os.path.join(settings.STATIC_ROOT, "index.html")
        if os.path.exists(index_path):
            return FileResponse(open(index_path, "rb"))
        return HttpResponse("index.html not found", content_type="text/plain")
