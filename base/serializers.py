from rest_framework.exceptions import APIException
from rest_framework_json_api import serializers
from rest_framework import status
from collections import OrderedDict
from .models import Movie, Booking


class NotEnoughAvailable_seatsException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "There is not enough available_seats"
    default_code = "invalid"


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = (
            "title",
            "available_seats",
            "price",
        )


class BookingSerializer(serializers.ModelSerializer):

    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all(), many=False)

    class Meta:
        model = Booking
        fields = (
            "movie",
            "seats",
        )

    def validate(self, res: OrderedDict):
        """
        Used to validate Movie stock levels
        """
        movie = res.get("movie")
        seats = res.get("seats")
        if not movie.check_available_seats(seats):
            raise NotEnoughAvailable_seatsException
        return res
