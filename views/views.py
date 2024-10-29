from django.views.generic import DetailView, TemplateView, ListView
from django.db.models import Q
from base.serializers import MovieSerializer
from base.models import Genre, Movie
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from typing import Any, Dict


class HomeView(ListView):
    model = Movie
    template_name = "movies/home.html"
    context_object_name = "movies"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["genres"] = Genre.objects.all()
        return context


class MovieDetailView(DetailView):
    model = Movie
    template_name = "movies/movie_detail.html"
    context_object_name = "movie"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["genres"] = Genre.objects.all()
        return context


class AboutUsView(TemplateView):
    template_name = "movies/about_us.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["genres"] = Genre.objects.all()
        return context


class GenreListView(ListView):
    model = Genre
    template_name = "movies/genre.html"
    context_object_name = "genres"

    def get_queryset(self):
        # Возвращаем уникальные жанры
        return Genre.objects.distinct()


class GenreMoviesView(DetailView):
    model = Genre
    template_name = "movies/genre_movies.html"
    context_object_name = "genre"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        # Получаем контекст из родительского класса
        context = super().get_context_data(**kwargs)
        # Добавляем жанры и фильмы в контекст
        context["genres"] = Genre.objects.all()
        context["movies"] = self.object.movies.all()
        return context


class MovieSearchView(ListView):
    model = Movie
    template_name = "movies/search_movies.html"
    context_object_name = "movies"

    def get_queryset(self):
        q = self.request.GET.get("q")
        if q:
            return Movie.objects.filter(
                Q(title__icontains=q) | Q(description__icontains=q)
            )
        return Movie.objects.none()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q", "")
        return context


class MovieViewSet(ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    """
    A simple ViewSet for listing or retrieving Movies.
    """

    permission_classes = (IsAuthenticated,)
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
