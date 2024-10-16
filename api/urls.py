from django.urls import path
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from views.booking import BookingViewSet
from views.views import MovieViewSet


router = routers.DefaultRouter()
router.register(r"movie", MovieViewSet, basename="movie")
router.register(r"booking", BookingViewSet, basename="booking")

urlpatterns = router.urls


urlpatterns += [
    path("api-token-auth/", obtain_auth_token),
]
