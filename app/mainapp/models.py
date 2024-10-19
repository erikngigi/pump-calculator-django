# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    expiration_date = models.DateTimeField(default=timezone.now() + timedelta(days=30))  # Default to 30 days from now

    def is_expired(self):
        return timezone.now() >= self.expiration_date
