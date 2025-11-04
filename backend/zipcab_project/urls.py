# zipcab_project/urls.py
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

# If you have a custom view to serve React build
# you can define FrontendAppView like this:
class FrontendAppView(TemplateView):
    template_name = "index.html"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # or cab_booking.urls depending on your app name
    path('silk/', include('silk.urls', namespace='silk')),

    # This must be last — it catches all frontend routes (React)
    re_path(r'^.*$', FrontendAppView.as_view(), name='frontend'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
