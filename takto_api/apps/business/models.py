import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)


class Business(models.Model):
    business_id = models.CharField(max_length=32, unique=True)
    name = models.TextField()
    state = models.CharField(max_length=2)
    city = models.TextField()
    address = models.TextField()
    postal_code = models.CharField(max_length=32)
    latitude = models.FloatField()
    longitude = models.FloatField()
    stars = models.FloatField()
    review_count = models.IntegerField()
    is_open = models.BooleanField()
    attributes = models.JSONField(null=True)
    hours = models.JSONField(null=True)
    categories = models.ManyToManyField(Category)


class Photo(models.Model):
    photo_id = models.CharField(max_length=32)
    business = models.ForeignKey(Business, related_name='photos', on_delete=models.CASCADE)
    caption = models.TextField()
    label = models.CharField(max_length=32)


class User(AbstractUser):
    device_id = models.CharField(max_length=64, unique=True)


class Room(models.Model):
    room_id = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class UserInRoom(models.Model):
    class Status:
        VOTING = 'voting'
        READY = 'ready'
        choices = [
            (VOTING, 'Голосует'),
            (READY, 'Готов'),
        ]

    room = models.ForeignKey(Room, related_name='user_in_room', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_in_room', on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.VOTING)
