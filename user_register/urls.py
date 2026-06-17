from django.urls import path
from django.contrib.auth.views import LoginView
from views.booking import CustomLoginView
from views.user import logoutUser, RegisterView, LinkPhoneView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logoutUser, name="logout"),
    path("accounts/login/", CustomLoginView.as_view(), name="login"),
    path("profile/phone/", LinkPhoneView.as_view(), name="link_phone"),
]
