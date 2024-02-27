import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings

def get_default_json():
    return {}


class User(AbstractUser):
    avatar = models.URLField(max_length=1000, blank=True)
    year_of_programming = models.PositiveSmallIntegerField(blank=True, null=True)
    solved_problem = models.PositiveSmallIntegerField(blank=True, null=True)
    target = models.JSONField(default=get_default_json)
    ability = models.JSONField(default=get_default_json)
    is_premium = models.BooleanField(default=False)
    premium_expired_day = models.DateTimeField(
        default=timezone.make_aware(datetime.datetime(2000, 5, 1, 12, 0)))
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    desc = models.TextField(blank=True)
    resource = models.URLField(max_length=1000, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
