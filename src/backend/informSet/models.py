from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class WebUser(AbstractUser):
	avatar = models.ImageField(max_length = 200, null = True)
	extra_data = models.JSONField(blank = True)
	def __str__(self):
		return self.name

class UserScore(models.Model):
	uniqueId = models.IntegerField(primary_key = True)
	user_id	 = models.ForeignKey(WebUser, on_delete = models.CASCADE)
	score_list = models.JSONField(blank = True)

class UserFav(models.Model):
	user_id = models.ForeignKey(WebUser, on_delete = models.CASCADE)
	type =  models.CharField(max_length = 200)
	content = models.JSONField()