import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from question.models import Tag

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


class UserAbility(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='abilities')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='user_abilities')
    ability_score = models.IntegerField(default=50)

    class Meta:
        unique_together = ('user', 'tag')

    def __str__(self):
        return f'{self.user.username} - {self.tag.name}: {self.ability_score}'


class AbilityHistory(models.Model):
    user_ability = models.ForeignKey(UserAbility, on_delete=models.CASCADE)
    recorded_date = models.DateField(auto_now_add=True)
    ability_score = models.IntegerField()

    def __str__(self):
        return f'{self.user_ability.user.username} - {self.user_ability.tag.name}: {self.ability_score} on {self.recorded_date}'
