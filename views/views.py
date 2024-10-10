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


def delete_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    
    if request.method == 'POST':
        movie.delete()
        return redirect("home")
    return render(request, 'movies/delete_movie.html', {'movie': movie})
        
        
def movie_detail(request, pk):
    movie = get_object_or_404(Movie,  pk=pk)
    return render(request, 'movies/movie_detail.html', {'movie': movie})



