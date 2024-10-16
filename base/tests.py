from django.contrib.auth.models import User
from base.models import Movie, Booking
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status


class EcommerceTestCase(APITestCase):
    """
    Test suite for Movies and Bookings
    """
    def setUp(self):

        Movie.objects.create(title= "Demo movie 1",description= "This is a description for demo 1",price= 500,stock= 20)
        Movie.objects.create(title= "Demo movie 2",description= "This is a description for demo 2",price= 700,stock= 15)
        Movie.objects.create(title= "Demo movie 3",description= "This is a description for demo 3",price= 300,stock= 18)
        Movie.objects.create(title= "Demo movie 4",description= "This is a description for demo 4",price= 400,stock= 14)
        Movie.objects.create(title= "Demo movie 5",description= "This is a description for demo 5",price= 500,stock= 30)
        self.movies = Movie.objects.all()
        self.user = User.objects.create_user(
            username='testuser1', 
            password='this_is_a_test',
            email='testuser1@test.com'
        )
        Booking.objects.create(movie = Movie.objects.first(), user = User.objects.first(), quantity=1)
        Booking.objects.create(movie = Movie.objects.first(), user = User.objects.first(), quantity=2)
        
        #The app uses token authentication
        self.token = Token.objects.get(user = self.user)
        self.client = APIClient()
        
        #We pass the token in all calls to the API
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)


    def test_get_all_movies(self):
        '''
        test MoviesViewSet list method
        '''
        self.assertEqual(self.movies.count(), 5)
        response = self.client.get('/movie/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_movie(self):
        '''
        test MoviesViewSet retrieve method
        '''
        for movie in self.movies:
            response = self.client.get(f'/movie/{movie.id}/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_booking_is_more_than_stock(self):
        '''
        test Movie.check_stock when booking.quantity > movie.stock
        '''
        for i in self.movies:
            current_stock = i.stock
            self.assertEqual(i.check_stock(current_stock + 1), False)

    def test_booking_equals_stock(self):
        '''
        test Movie.check_stock when booking.quantity == movie.stock
        '''
        for i in self.movies:
            current_stock = i.stock
            self.assertEqual(i.check_stock(current_stock), True)

    def test_booking_is_less_than_stock(self):
        '''
        test Movie.check_stock when booking.quantity < movie.stock
        '''
        for i in self.movies:
            current_stock = i.stock
            self.assertTrue(i.check_stock(current_stock - 1), True)
    
    def test_create_booking_with_more_than_stock(self):
        '''
        test BookingsViewSet create method when booking.quantity > movie.stock
        '''
        for i in self.movies:
            stock = i.stock
            data = {"movie": str(i.id), "quantity": str(stock+1)}
            response = self.client.post(f'/booking/', data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_booking_with_less_than_stock(self):
        '''
        test BookingsViewSet create method when booking.quantity < movie.stock
        '''
        for i in self.movies:
            data = {"movie": str(i.id), "quantity": 1}
            response = self.client.post(f'/booking/',data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_booking_with_equal_stock(self):
        '''
        test BookingsViewSet create method when booking.quantity == movie.stock
        '''
        for i in self.movies:
            stock = i.stock
            data = {"movie": str(i.id), "quantity": str(stock)}
            response = self.client.post(f'/booking/',data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_bookings(self):
        '''
        test BookingsViewSet list method
        '''
        self.assertEqual(Booking.objects.count(), 2)
        response = self.client.get('/booking/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

    def test_get_one_booking(self):
        '''
        test BookingsViewSet retrieve method
        '''
        bookings = Booking.objects.filter(user = self.user)
        for o in bookings:
            response = self.client.get(f'/booking/{o.id}/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)