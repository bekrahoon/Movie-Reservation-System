from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from base.models import Movie, Booking


def movie_detail(request, pk):
    movie = get_object_or_404(Movie,  pk=pk)
    return render(request, 'movies/movie_detail.html', {'movie': movie})

@login_required
def book_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == "POST":
        seats = request.POST.get("seats")
        show_time = movie.show_time
        Booking.objects.create(
            user=request.user, movie=movie, seats=seats, show_time=show_time
        )
        return redirect("user_booking")
    return render(request, "movies/book_movie.html", {"movie": movie})


@login_required
def user_booking(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, "movies/user_booking.html", {"bookings": bookings})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if booking.user == request.user and booking.show_time > timezone.now():
        booking.delete()
    return redirect("user_booking")
