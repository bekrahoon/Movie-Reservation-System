from django.urls import path
from telegram_app.views import mini_app_page, telegram_auth, telegram_link

urlpatterns = [
    path("", mini_app_page, name="telegram_mini_app"),
    path("auth/", telegram_auth, name="telegram_auth"),
    path("link/", telegram_link, name="telegram_link"),
]
