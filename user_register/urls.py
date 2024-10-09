from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from views.user import register, logoutUser

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logoutUser, name="logout"),
]
