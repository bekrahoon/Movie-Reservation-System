from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from base.forms import BookingForm
from base.models import Movie, Booking
from django.contrib import messages

def booking_list(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, "movies/booking_list.html", context={"bookings":bookings})


@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, id=pk, user=request.user)
    
    
    if booking.can_cancel():
        booking.delete()
        messages.success(request, "Бронирование успешно отменено")
    else:
        messages.error(request, " Вы не можете отменить это бронирование ")
    return redirect("booking_list")


@login_required
def booking_create(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit = False)
            booking.movie = movie
            booking.user = request.user
            booking.save()
            messages.success(request, "Бронирование успешно создано")
            return redirect("booking_list")
    else:
        form =  BookingForm()
    return render(request, "movies/booking_form.html", context={"form":form, "movie":movie})