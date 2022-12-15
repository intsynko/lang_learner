from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("apps.web.urls", namespace="web")),
    path("api/", include("api.urls")),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^assets/(?P<path>.*)$', serve, {'document_root': settings.ASSETS_ROOT}),
]

# if settings.DEBUG:
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

