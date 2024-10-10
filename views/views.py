from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpRequest
from base.forms import MovieForm
from base.models import Booking, Movie
from django.contrib import messages

def home(request: HttpRequest):
    movies = Movie.objects.all()
    context = {'movies':movies}
    return render(request, "movies/home.html", context)


@staff_member_required
def add_movie(request):
    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid:
            form.save()
            messages.success(request, 'Фильм успешно добавлен.')
            return redirect("home")
    else:
        form = MovieForm()
    return render(request, "movies/add_movie.html", {"form": form})


@staff_member_required
def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == "POST":
        form = MovieForm(request.Post, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect("home")

    else:
        form = MovieForm(instance=movie)
    return render(request, "movies/edit_movie.html", {"form": form, "movie":movie})

def delete_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    
    if request.method == 'POST':
        movie.delete()
        return redirect("home")
    return render(request, 'movies/delete_movie.html', {'movie': movie})
        
        
def movie_detail(request, pk):
    movie = get_object_or_404(Movie,  pk=pk)
    return render(request, 'movies/movie_detail.html', {'movie': movie})


@staff_member_required
def admin_report(request):
    bookings = Booking.objects.all()
    
    total_income = sum(booking.movie.price * booking.seats for booking in bookings)
    
    available_seats = {movie.title: movie.available_seats for movie in Movie.objects.all()}
    
    context = {
        "bookings":bookings,
        "total_income":total_income,
        "available_seats":available_seats
    }
    return render(request, "admin/report.html", context)