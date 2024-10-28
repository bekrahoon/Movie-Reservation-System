from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from base.serializers import BookingSerializer
from base.models import Genre, Movie, Booking
from base.forms import BookingForm
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from json import JSONDecodeError


class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = "movies/booking_list.html"
    context_object_name = "bookings"
    login_url = "login"

    def get_queryset(self):
        # Фильтруем бронирования для текущего пользователя
        return Booking.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        # Добавляем жанры в контекст
        context = super().get_context_data(**kwargs)
        context["genres"] = Genre.objects.all()
        return context


class BookingCancelView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Booking
    template_name = (
        "movies/booking_confirm_delete.html"  # Шаблон подтверждения удаления
    )
    success_url = reverse_lazy("booking_list")
    login_url = "login"

    def test_func(self) -> bool:
        # Проверяем, что пользователь является владельцем бронирования
        booking = self.get_object()
        return self.request.user == booking.user

    def delete(self, request, *args, **kwargs):
        # Логика отмены бронирования
        booking = self.get_object()
        if booking.can_cancel():
            # Возвращаем количество мест в доступные места для фильма
            movie = booking.movie
            movie.available_seats += booking.seats
            movie.save()  # Сохраняем изменения в фильме

        return super().delete(request, *args, **kwargs)

    def handle_no_permission(self) -> HttpResponse:
        return HttpResponse("You are not allowed to cancel this booking!")
    
class BookingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Booking
    success_url = reverse_lazy("booking_list")
    login_url = "login"

    def test_func(self) -> bool:
        # Проверяем, что пользователь является владельцем бронирования
        booking = self.get_object()
        return self.request.user == booking.user

    def delete(self, request, *args, **kwargs):
        # Логика отмены бронирования
        booking = self.get_object()

        # Возвращаем количество мест в доступные места для фильма
        movie = booking.movie
        movie.save()  # Сохраняем изменения в фильме

        return super().delete(request, *args, **kwargs)

    def handle_no_permission(self) -> HttpResponse:
        return HttpResponse("You are not allowed to cancel this booking!")


class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = "movies/booking_form.html"
    login_url = "login"
    success_url = reverse_lazy("booking_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie = get_object_or_404(Movie, pk=self.kwargs["pk"])
        context["movie"] = movie
        return context

    def form_valid(self, form: BookingForm) -> HttpResponse:
        movie = get_object_or_404(Movie, pk=self.kwargs["pk"])
        form.instance.user = self.request.user
        form.instance.movie = movie
        seats = form.cleaned_data["seats"]
        if Booking.objects.filter(user=self.request.user, movie=movie).exists():
            form.add_error(
                None,
                "Вы уже забронировали этот фильм. Отмените бронирование, если хотите изменить.",
            )
            return self.form_invalid(form)
        if seats > movie.available_seats:
            form.add_error(
                None, f"Недостаточно мест. Доступно: {movie.available_seats}"
            )
            return self.form_invalid(form)
        movie.available_seats -= seats  # Обновляем количество доступных мест
        movie.save()
        response = super().form_valid(form)
        # Перенаправляем на страницу подтверждения бронирования
        return redirect('booking_list')



class CustomLoginView(auth_views.LoginView):
    def get(self, request, *args, **kwargs):
        messages.info(
            request,
            "Пожалуйста, войдите или зарегистрируйтесь, чтобы получить доступ к этой странице.",
        )
        return super().get(request, *args, **kwargs)



class BookingViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
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
        return Booking.objects.filter(user=user)

    def create(self, request):
        try:
            data = JSONParser().parse(request)
            serializer = BookingSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                movie = Movie.objects.get(pk=data["movie"])
                # Проверка на существующее бронирование и его удаление
                existing_booking = Booking.objects.filter(user=request.user, movie=movie)
                if existing_booking.exists():
                    existing_booking.delete()
                booking = movie.place_booking(request.user, data["seats"])
                return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse(
                {"result": "error", "message": "Json decoding error"}, status=400
            )
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
