from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpRequest
from base.forms import MovieForm
from base.models import Booking, Movie
from django.db.models import Sum


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
    return render(request, "movies/edit_movie.html", {"form": form})


@staff_member_required
def admin_report(request):
    total_bookings = Booking.objects.count()
    total_income = Booking.objects.aaggregate(income=Sum("seats"))["income"]
    return render(
        request,
        "admin/admin_report.html",
        {"total_bookings": total_bookings, "total_income": total_income},
    )
