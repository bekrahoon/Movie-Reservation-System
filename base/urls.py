from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from views.booking import booking_create, booking_list
from views.views import add_movie, delete_movie, edit_movie, home, movie_detail, admin_report

urlpatterns = [
    path("", home, name="home"),
    path("movies/<int:pk>/", movie_detail, name="movie_detail"),
    path("movies/add/", add_movie, name="add_movie"),
    path("movie/<int:movie_id>edit/", edit_movie, name="movie_edit"),
    path("movies/<int:pk>delete", delete_movie ,name="movie_delete"),
    path("bookings/", booking_list, name="booking_list"),
    path("bookings/<int:pk>/cancel/", booking_create , name="booking_create"),
    path("admin/report/", admin_report , name="admin_report")
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
