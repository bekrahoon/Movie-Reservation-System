from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from base.forms import BookingForm
from base.models import Movie, Booking
from django.contrib.auth import views as auth_views
from django.contrib import messages


@login_required
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, "movies/booking_list.html", context={"bookings":bookings})


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
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            seats = form.cleaned_data['seats']
            if Booking.objects.filter(user = request.user, movie=movie).exists():
                form.add_error(None, 'Вы уже забронировали этот фильм.')
            elif seats > movie.available_seats:
                form.add_error(None, f'Недостаточно мест. Доступно: {movie.available_seats}')
            elif seats == 0:
                form.add_error(None, f' Места не могут быть нулевыми')
            else:
                booking = form.save(commit = False)
                booking.movie = movie
                booking.user = request.user
                booking.save()
                return redirect("booking_list")
    else:
        form =  BookingForm()
    return render(request, "movies/booking_form.html", context={"form":form, "movie":movie})


@login_required
def booking_edit(request, pk):
    booking = get_object_or_404(Booking, id=pk, user=request.user)
    movie = booking.movie

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            seats = form.cleaned_data['seats']
            if seats > movie.available_seats:
                form.add_error(None, f'Недостаточно мест. Доступно:  {movie.available_seats}')
            elif seats == 0:
                form.add_error(None, f' Места не могут быть нулевыми')
            else:
                booking = form.save(commit = False)
                booking.movie = movie
                booking.user = request.user
                booking.save()
                return redirect("booking_list")
    else:
        form = BookingForm(instance=booking)

    return render(request, "movies/booking_form_edit.html", context={"form": form, "movie": movie})


class CustomLoginView(auth_views.LoginView):
    def get(self, request, *args, **kwargs):
        messages.info(request, "Пожалуйста, войдите или зарегистрируйтесь, чтобы получить доступ к этой странице.")
        return super().get(request, *args, **kwargs)