#zipcab_project/urls.py

import os
from django.views.generic import View
from django.http import FileResponse, HttpResponseNotFound
from django.urls import path, include, re_path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


class FrontendAppView(View):
    def get(self, request):
        index_file = os.path.join(settings.BASE_DIR, "..", "frontend", "dist", "index.html")
        print("Serving:", os.path.abspath(index_file))
        if os.path.exists(index_file):
            return FileResponse(open(index_file, "rb"))
        return HttpResponseNotFound("index.html not found")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("silk/", include("silk.urls", namespace="silk")),
]

# --- Add static + media first ---
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# --- Catch-all for React (must always be last) ---
urlpatterns.append(re_path(r"^(?:.*)/?$", FrontendAppView.as_view(), name="frontend"))
