import os
from django.http import FileResponse, Http404
from django.views import View

class FrontendAppView(View):
    def get(self, request, *args, **kwargs):
        index_path = os.path.join(
            os.path.dirname(__file__), 
            "../static/frontend_build/index.html"
        )
        if os.path.exists(index_path):
            return FileResponse(open(index_path, "rb"))
        raise Http404("index.html not found")
