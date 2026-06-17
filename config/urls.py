from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "service-worker.js",
        TemplateView.as_view(
            template_name="service-worker.js",
            content_type="application/javascript",
            extra_context={"CACHE_VERSION": "1"},
        ),
        name="service-worker",
    ),
    path(
        "offline/",
        TemplateView.as_view(template_name="offline.html"),
        name="offline",
    ),
    path("", include("base.urls")),
    path("", include("cart.urls")),
    path("", include("user_register.urls")),
    path("api/", include("api.urls")),
    path("telegram/", include("telegram_app.urls")),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
