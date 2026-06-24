from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    title=models.CharField(max_length=100)
    duration=models.IntegerField()

    def __str__(self):
        return self.title


class Theater(models.Model):
    name=models.CharField(max_length=100)
    location=models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Show(models.Model):
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE)
    theater=models.ForeignKey(Theater,on_delete=models.CASCADE)
    show_time=models.DateTimeField()

    def __str__(self):
        return f"{self.movie.title}-{self.show_time}"


class Seat(models.Model):
    STATUS_CHOICES=[
        ('AVAILABLE','Available'),
        ('RESERVED','Reserved'),
        ('BOOKED','Booked'),
    ]

    show=models.ForeignKey(Show,on_delete=models.CASCADE)
    seat_number=models.CharField(max_length=10)
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default='AVAILABLE')

    class Meta:
        unique_together=('show','seat_number')

    def __str__(self):
        return self.seat_number


class Reservation(models.Model):
    STATUS_CHOICES=[
        ('PENDING','Pending'),
        ('CONFIRMED','Confirmed'),
        ('EXPIRED','Expired'),
    ]

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    seat=models.ForeignKey(Seat,on_delete=models.CASCADE)
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default='PENDING')
    created_at=models.DateTimeField(auto_now_add=True)
    expires_at=models.DateTimeField()

    def __str__(self):
        return f"{self.user.username}-{self.seat.seat_number}"