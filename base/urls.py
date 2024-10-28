from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from views.booking import BookingConfirmationView, BookingCreateView, BookingListView, BookingDeleteView, BookingCancelView
from views.views import (
    AboutUsView,
    GenreMoviesView,
    GenreListView,
    HomeView,
    MovieDetailView,
    MovieSearchView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("movies/<int:pk>/", MovieDetailView.as_view(), name="movie_detail"),
    path("movies_genre/<int:pk>/", GenreMoviesView.as_view(), name="genre_movies"),
    path("movies_search/", MovieSearchView.as_view(), name="search_movies"),
    path("bookings/", BookingListView.as_view(), name="booking_list"),
    path(
        "bookings/<int:pk>/create/", BookingCreateView.as_view(), name="booking_create"
    ),
    path(
        "bookings/<int:pk>/cancel/", BookingCancelView.as_view(), name="booking_cancel"
    ),
    path('booking-confirmation/<int:pk>/', BookingConfirmationView.as_view(), name='booking_confirmation'),
    path("about_us/", AboutUsView.as_view(), name="about_us"),
    path("genres/", GenreListView.as_view(), name="genres"),
    path("bookings/<int:pk>/delete/",  BookingDeleteView.as_view(), name="booking_delete"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
