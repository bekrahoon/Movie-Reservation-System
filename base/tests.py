from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from base.models import Movie, Booking


class EcommerceTestCase(APITestCase):
    """
    Test suite for Movies and Bookings
    """

    def setUp(self):
        # Create demo movies
        self.poster_file = SimpleUploadedFile(
            "poster.jpg", b"file_content", content_type="image/jpeg"
        )
        self.movies = [
            Movie.objects.create(
                title="Demo movie 1",
                description="This is a description for demo 1",
                price=500,
                available_seats=20,
                poster=self.poster_file,
                show_time=timezone.now(),
            ),
            Movie.objects.create(
                title="Demo movie 2",
                description="This is a description for demo 2",
                price=700,
                available_seats=15,
                poster=self.poster_file,
                show_time=timezone.now(),
            ),
            Movie.objects.create(
                title="Demo movie 3",
                description="This is a description for demo 3",
                price=300,
                available_seats=18,
                poster=self.poster_file,
                show_time=timezone.now(),
            ),
            Movie.objects.create(
                title="Demo movie 4",
                description="This is a description for demo 4",
                price=400,
                available_seats=14,
                poster=self.poster_file,
                show_time=timezone.now(),
            ),
            Movie.objects.create(
                title="Demo movie 5",
                description="This is a description for demo 5",
                price=500,
                available_seats=30,
                poster=self.poster_file,
                show_time=timezone.now(),
            ),
        ]

        # Create a test user
        self.user = User.objects.create_user(
            username="testuser1", password="this_is_a_test", email="testuser1@test.com"
        )

        # Create bookings
        Booking.objects.create(movie=self.movies[1], user=self.user, seats=1)

        # Set up token and client for API authentication
        self.token = Token.objects.get(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_get_all_movies(self):
        """Test MoviesViewSet list method"""
        response = self.client.get("/api/movie/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_movie(self):
        """Test MoviesViewSet retrieve method"""
        for movie in self.movies:
            response = self.client.get(f"/api/movie/{movie.id}/")
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_booking_exceeds_available_seats(self):
        """Test Movie.check_available_seats when booking.seats > movie.available_seats"""
        for movie in self.movies:
            self.assertFalse(movie.check_available_seats(movie.available_seats + 1))

    def test_booking_equals_available_seats(self):
        """Test Movie.check_available_seats when booking.seats == movie.available_seats"""
        for movie in self.movies:
            self.assertTrue(movie.check_available_seats(movie.available_seats))

    def test_booking_less_than_available_seats(self):
        """Test Movie.check_available_seats when booking.seats < movie.available_seats"""
        for movie in self.movies:
            self.assertTrue(movie.check_available_seats(movie.available_seats - 1))

    def test_create_booking_exceeds_available_seats(self):
        """Test BookingsViewSet create method when booking.seats > movie.available_seats"""
        for movie in self.movies:
            data = {"movie": movie.id, "seats": movie.available_seats + 1}
            response = self.client.post("/api/booking/", data, format="vnd.api+json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_booking_less_than_available_seats(self):
        """Test BookingsViewSet create method when booking.seats < movie.available_seats"""
        for movie in self.movies:
            data = {"movie": movie.id, "seats": 1}
            response = self.client.post("/api/booking/", data, format="vnd.api+json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_booking_equal_available_seats(self):
        """Test BookingsViewSet create method when booking.seats == movie.available_seats"""
        for movie in self.movies:
            data = {"movie": movie.id, "seats": movie.available_seats}
            response = self.client.post("/api/booking/", data, format="vnd.api+json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_all_bookings(self):
        """Test BookingsViewSet list method"""
        response = self.client.get("/api/booking/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), Booking.objects.count()
        )  # Проверьте количество бронирований
