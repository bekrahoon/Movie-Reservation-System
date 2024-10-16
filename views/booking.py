from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from base.forms import BookingForm
from base.models import Genre, Movie, Booking
from django.contrib.auth import views as auth_views
from django.contrib import messages
from json import JSONDecodeError
from django.http import JsonResponse
from base.serializers import BookingSerializer
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin,UpdateModelMixin,RetrieveModelMixin


@login_required
def booking_list(request):
    genres = Genre.objects.all()

    bookings = Booking.objects.filter(user=request.user)
    return render(
        request,
        "movies/booking_list.html",
        context={"bookings": bookings, "genres": genres},
    )


@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, id=pk, user=request.user)

    if booking.can_cancel():
        # Возвращаем количество мест в доступные места для фильма
        movie = booking.movie
        movie.available_seats += booking.seats
        movie.save()  # Сохраняем изменения в фильме

        booking.delete()  # Удаляем бронирование

    return redirect("booking_list")


@login_required
def booking_create(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            seats = form.cleaned_data["seats"]
            if Booking.objects.filter(user=request.user, movie=movie).exists():
                form.add_error(
                    None,
                    "Вы уже забронировали этот фильм. Отмените бронирование если хотите изменить",
                )
            elif seats > movie.available_seats:
                form.add_error(
                    None, f"Недостаточно мест. Доступно: {movie.available_seats}"
                )
            else:
                booking = form.save(commit=False)
                booking.movie = movie
                booking.user = request.user
                booking.save()
                return redirect("booking_list")
    else:
        form = BookingForm()
    return render(
        request, "movies/booking_form.html", context={"form": form, "movie": movie}
    )


class CustomLoginView(auth_views.LoginView):
    def get(self, request, *args, **kwargs):
        messages.info(
            request,
            "Пожалуйста, войдите или зарегистрируйтесь, чтобы получить доступ к этой странице.",
        )
        return super().get(request, *args, **kwargs)




class BookingViewSet(
        ListModelMixin,
        RetrieveModelMixin,
        UpdateModelMixin, 
        viewsets.GenericViewSet
        ):
    """
    A simple ViewSet for listing, retrieving and creating Bookings.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = BookingSerializer

    def get_queryset(self):
        """
        This view should return a list of all the Bookings
        for the currently authenticated user.
        """
        user = self.request.user
        return Booking.objects.filter(user = user)

    def create(self, request):
        try:
            data = JSONParser().parse(request)
            serializer = BookingSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                movie = Movie.objects.get(pk = data["Movie"])
                booking = movie.place_Booking(request.user, data["quantity"])
                return Response(BookingSerializer(booking).data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error","message": "Json decoding error"}, status= 400)