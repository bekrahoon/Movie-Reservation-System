from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from base.models import Movie
from cart.models import Cart, CartItem


class CartView(LoginRequiredMixin, View):
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        items = CartItem.objects.filter(cart=cart)
        return render(request, "movies/cart.html", {"cart": cart, "items": items})


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, movie_id):
        cart, created = Cart.objects.get_or_create(user=request.user)
        movie = get_object_or_404(Movie, id=movie_id)
        item, created = CartItem.objects.get_or_create(cart=cart, movie=movie)
        if not created:
            item.quantity += 1
            item.save()
        return redirect("cart")


class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        item = get_object_or_404(CartItem, id=item_id)
        item.delete()
        return redirect("cart")

