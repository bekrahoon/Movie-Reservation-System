from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from views.views import home
from views.booking import movie_detail

urlpatterns = [path("", home, name="home"),
               path("movies/<int:pk>", movie_detail, name="movie_detail")
               ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
