from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from cart.models import Cart, CartItem
from base.models import Movie


class CartView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:

        cart, created = Cart.objects.get_or_create(user=request.user)
        items = CartItem.objects.filter(cart=cart)
        return render(request, "movies/cart.html", {"cart": cart, "items": items})


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest, movie_id: int) -> HttpResponse:
        # Retrieve the cart or create a new one for the user
        cart, created = Cart.objects.get_or_create(user=request.user)
        movie = get_object_or_404(Movie, id=movie_id)

        # Get the quantity from the form submission
        quantity = int(request.POST.get("quantity", 1))  # Default to 1 if not provided

        # Get or create a cart item
        item, created = CartItem.objects.get_or_create(cart=cart, movie=movie)

        if created:
            # If the item is new, set the quantity to the specified amount
            item.quantity = quantity
        else:
            # If it already exists, increment the quantity by the specified amount
            item.quantity += quantity

        # Save the item with the updated quantity
        item.save()

        return redirect("cart")


class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest, item_id: int) -> HttpResponse:
        item = get_object_or_404(CartItem, id=item_id)
        item.delete()
        return redirect("cart")
