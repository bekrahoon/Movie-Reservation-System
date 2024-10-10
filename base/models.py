from django.db import models
from django.contrib.auth import get_user_model
from .base_model import BaseModel
from django.utils import timezone
User = get_user_model()


class Genre(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(BaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField()
    poster = models.ImageField(upload_to="poster/")
    genre = models.ManyToManyField(Genre)
    show_time = models.DateTimeField()
    price = models.DecimalField(max_digits=6, decimal_places=2)  
    available_seats = models.PositiveIntegerField() 
    
    def __str__(self):
        return self.title


class Booking(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    show_time = models.DateTimeField()
    seats = models.PositiveIntegerField()
    booked_at = models.DateTimeField(default=timezone.now())
    
    def can_cancel(self):
        # Проверка, что бронирование можно отменить только до начала сеанса
        return self.show_time > timezone.now()

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} - {self.show_time}  - {self.seats} seats"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "movie", "show_time"], name="unique_booking"
            )
        ]
