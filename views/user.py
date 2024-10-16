from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from user_register.forms import RegisterForm
from django.views.generic import CreateView
from django.urls import reverse_lazy


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        # Сохраняем пользователя и выполняем автоматический вход
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


def logoutUser(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("home")
