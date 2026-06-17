from django.http import HttpRequest, HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, FormView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from user_register.forms import RegisterForm, PhoneForm
from user_register.models import Profile
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


class LinkPhoneView(LoginRequiredMixin, FormView):
    template_name = "registration/link_phone.html"
    form_class = PhoneForm
    success_url = reverse_lazy("link_phone")
    login_url = "login"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        context["current_phone"] = profile.phone
        return context

    def form_valid(self, form):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        profile.phone = form.cleaned_data["phone"]
        profile.save()
        return super().form_valid(form)


def logoutUser(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("home")
