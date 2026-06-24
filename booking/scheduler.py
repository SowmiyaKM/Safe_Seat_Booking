from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from .models import Reservation

def release_expired_reservations():
    expired_reservations=Reservation.objects.filter(
        status='PENDING',
        expires_at__lte=timezone.now()
    )

    for reservation in expired_reservations:
        reservation.status='EXPIRED'
        reservation.save()

        seat=reservation.seat
        seat.status='AVAILABLE'
        seat.save()

        print(f"{seat.seat_number} released")

def start():
    print("Scheduler started")

    scheduler=BackgroundScheduler()
    scheduler.add_job(
        release_expired_reservations,
        'interval',
        seconds=10
    )
    scheduler.start()