from django.shortcuts import render,get_object_or_404
from .models import Movie,Show,Seat,Reservation
from django.http import HttpResponse
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def movie_list(request):
    movies=Movie.objects.all()
    return render(request,'booking/movie_list.html',{'movies':movies})

def show_list(request,movie_id):
    movie=get_object_or_404(Movie,id=movie_id)
    shows=Show.objects.filter(movie=movie)
    return render(request,'booking/show_list.html',{
        'movie':movie,
        'shows':shows
    })

@login_required
def seat_list(request,show_id):
    show=get_object_or_404(Show,id=show_id)
    seats=Seat.objects.filter(show=show)

    if request.method=='POST':
        seat_ids=request.POST.getlist('seat_ids')

        user=request.user

        with transaction.atomic():

            for seat_id in seat_ids:

                seat=Seat.objects.select_for_update().get(id=seat_id)

                if seat.status!='AVAILABLE':
                    return HttpResponse(
                        f"Seat {seat.seat_number} is already reserved or booked"
                    )

                seat.status='RESERVED'
                seat.save()

                Reservation.objects.create(
                    user=user,
                    seat=seat,
                    status='PENDING',
                    expires_at=timezone.now()+timedelta(minutes=2)
                )

        return render(request,'booking/payment.html')

    return render(request,'booking/seat_list.html',{
        'show':show,
        'seats':seats
    })

@login_required
def confirm_payment(request):
    user=request.user
    reservations=Reservation.objects.filter(
        user=user,
        status='PENDING'
    )

    for reservation in reservations:
        reservation.status='CONFIRMED'
        reservation.save()

        seat=reservation.seat
        seat.status='BOOKED'
        seat.save()

    return render(request,'booking/success.html')