from django.db import models


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


class Category(models.Model):
    business = models.ForeignKey(Business, related_name='categories', on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
