from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from views.booking import booking_create, booking_edit, booking_list, cancel_booking
from views.views import  delete_movie, home, movie_detail

urlpatterns = [
    path("", home, name="home"),
    path("movies/<int:pk>/", movie_detail, name="movie_detail"),
    path("movies/<int:pk>delete", delete_movie ,name="movie_delete"),
    path("bookings/", booking_list, name="booking_list"),
    path("bookings/<int:pk>/create/", booking_create , name="booking_create"),
    path("bookings/<int:pk>/cancel/",  cancel_booking , name="booking_cancel"),
    path('bookings/edit/<int:pk>/', booking_edit, name='booking_edit'), 

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
