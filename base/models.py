from django.db import transaction
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone
from utils.model_abstracts import BaseModel
from typing import Tuple, Any

User = get_user_model()


class Genre(BaseModel):
    name: str = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Movie(BaseModel):
    title: str = models.CharField(max_length=200)
    description: str = models.TextField()
    poster = models.ImageField(upload_to="poster/")
    genre = models.ManyToManyField(Genre, related_name="movies")
    show_time = models.DateTimeField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    available_seats: int = models.PositiveIntegerField()

    def can_cancel(self) ->  bool:
        return self.show_time > timezone.now()

    def check_available_seats(self, booking_seats) -> bool:
        return booking_seats <= self.available_seats

    def place_booking(self, user, seats: int) -> 'Booking':
        if not self.check_available_seats(seats):
            raise ValidationError("Not enough available seats.")
        booking = Booking.objects.create(user=user, movie=self, seats=seats)
        return booking

    def __str__(self) -> str:
        return self.title


class Booking(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    seats: str = models.PositiveIntegerField()
    booked_at = models.DateTimeField(default=timezone.now)

    def can_cancel(self) -> bool:
        # Проверка, что бронирование можно отменить только до начала сеанса
        return self.movie.show_time > timezone.now()

    def __str__(self) -> str:
        return f"{self.user.username} - {self.movie.title} - {self.movie.show_time} - {self.seats} seats"

    def save(self, *args: Tuple, **kwargs:  Any) -> None:
        # Применение транзакции
        with transaction.atomic():
            # Проверка доступных мест перед уменьшением
            if self.seats > self.movie.available_seats:
                raise ValidationError(
                    f"Not enough available seats. Available: {self.movie.available_seats}"
                )

            # Обновление количества доступных мест
            self.movie.available_seats -= self.seats
            self.movie.save()  # Сохранение изменения в фильме

            super().save(*args, **kwargs)  # Сохранение бронирования

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "movie"], name="unique_booking")
        ]
