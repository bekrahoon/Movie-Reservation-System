from django.urls import path
from views.cart import CreateCheckoutSessionView, CartView, AddToCartView, RemoveFromCartView

urlpatterns = [
    # другие пути
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<int:movie_id>/', AddToCartView.as_view(), name='add-to-cart'),
    path('remove-from-cart/<int:item_id>/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('create-checkout-session/<int:pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
]
