from django.db import models
from django.contrib.auth.models import User


class RareUser(models.Model):
    bio = models.CharField(max_length=200)
    profile_image_url = models.CharField(max_length=200)
    created_on = models.DateTimeField()
    active = models.BooleanField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
