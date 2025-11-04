import os
from django.views.generic import View
from django.http import FileResponse, HttpResponseNotFound
from django.conf import settings

class FrontendAppView(View):
    def get(self, request, *args, **kwargs):
        index_path = os.path.join(settings.BASE_DIR, "backend", "static", "frontend_build", "index.html")
        if os.path.exists(index_path):
            return FileResponse(open(index_path, "rb"))
        return HttpResponseNotFound("index.html not found")
