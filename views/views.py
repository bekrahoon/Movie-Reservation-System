from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpRequest
from base.models import Genre, Movie
from django.db.models import Q

def home(request: HttpRequest):
    genres = Genre.objects.all()  
    
    movies = Movie.objects.all()
    context = {'movies':movies,  'genres':genres}

    return render(request, "movies/home.html", context)


def delete_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    
    if request.method == 'POST':
        movie.delete()
        return redirect("home")
    return render(request, 'movies/delete_movie.html', {'movie': movie})
        
        
def movie_detail(request, pk):
    genres = Genre.objects.all()  
    
    movie = get_object_or_404(Movie,  pk=pk)
    return render(request, 'movies/movie_detail.html', {'movie': movie,  'genres': genres})


def about_us(request):
    genres = Genre.objects.all()  
    
    return render (request, 'movies/about_us.html',  {'genres': genres})


def genres(request):
    genres = Genre.objects.filter().distinct()
    context = {'genres': genres}
    return render(request, 'movies/genre.html', context)

def genre_movies(request, pk):
    genres = Genre.objects.all()  
    genre = get_object_or_404(Genre, pk=pk)
    movies = genre.movies.all()
    context = {'genre':genre, 'genres':genres, 'movies':movies}
    return  render(request, 'movies/genre_movies.html', context)


def search_movies(request):
    q = request.GET.get('q')
    if q:
        movies = Movie.objects.filter(
            Q(title__icontains = q) | Q(description__icontains = q))
    else:   
        movies = Movie.objects.none()
    context = {'movies':movies, 'q':q}
    return render(request, 'movies/search_movies.html', context)