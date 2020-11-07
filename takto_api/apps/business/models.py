import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
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
    username = models.CharField(max_length=150, validators=[UnicodeUsernameValidator()])
    device_id = models.CharField(max_length=64, unique=True)

    USERNAME_FIELD = 'device_id'


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

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['room', 'user'], name='unique_room_user')
        ]

    @classmethod
    def create_with_choice(cls, room, user):
        instance = cls.objects.create(room=room, user=user)
        Choice.create_random(instance)
        return instance


class Choice(models.Model):
    user_in_room = models.ForeignKey(UserInRoom, related_name='choices', on_delete=models.CASCADE)
    first_business = models.ForeignKey(Business, related_name='+', on_delete=models.SET_NULL, null=True)
    second_business = models.ForeignKey(Business, related_name='+', on_delete=models.SET_NULL, null=True)
    first_business_chosen = models.BooleanField(null=True)

    @classmethod
    def create_random(cls, user_in_room, first_business=None):
        return cls.objects.create(
            user_in_room=user_in_room,
            first_business=first_business or Business.objects.order_by('?').first(),
            second_business=Business.objects.order_by('?').first()
        )
