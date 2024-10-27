from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
import stripe
from base.models import Movie
from cart.models import Cart, CartItem


class CartView(LoginRequiredMixin, View):
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        items = CartItem.objects.filter(cart=cart)
        return render(request, 'movies/cart.html', {'cart': cart, 'items': items})

class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, movie_id):
        cart, created = Cart.objects.get_or_create(user=request.user)
        movie = get_object_or_404(Movie, id=movie_id)
        item, created = CartItem.objects.get_or_create(cart=cart, movie=movie)
        if not created:
            item.quantity += 1
            item.save()
        return redirect('cart')


class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        item = get_object_or_404(CartItem, id=item_id)
        item.delete()
        return redirect('cart')



from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
import stripe

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        movie_id = self.kwargs['pk']
        movie = get_object_or_404(Movie, pk=movie_id)

        YOUR_DOMAIN = "http://localhost:8000"
        line_items = [{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': movie.title,
                },
                'unit_amount': int(movie.price * 100),  # цена в центах
            },
            'quantity': 1,
        }]

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )

        return JsonResponse({'id': checkout_session.id})





