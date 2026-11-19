from django.db import models
from django.contrib.auth.models import AbstractUser





class Category(models.Model):
    name = models.CharField(max_length=50)
    players_count = models.PositiveIntegerField()




class User(AbstractUser):

    avatar = models.ImageField(upload_to="avatars", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=14, null=True, blank=True)


class Field(models.Model):

    image = models.ImageField(upload_to='images')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    address = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete= models.CASCADE, related_name="fields")
    description = models.TextField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)








class Booking(models.Model):

    booking_statuses = [
        ("active", "Активный"),
        ("completed", "Закончено"),
        ("cancelled", "Отменено")
    ]


    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name="bookings")
    field = models.ForeignKey(Field, on_delete= models.CASCADE, related_name="bookings")
    has_team = models.BooleanField(default=False)
    players_needed = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=booking_statuses, default="active")


class Participant(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="participants")
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ("booking", "user")