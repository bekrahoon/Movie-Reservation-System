from django.http import HttpRequest, HttpResponse
from django.contrib.auth import login, logout
from django.views.generic import CreateView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from user_register.forms import RegisterForm
from typing import Any


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form: Any) -> HttpResponse:
        # Сохраняем пользователя и выполняем автоматический вход
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


def logoutUser(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("home")
