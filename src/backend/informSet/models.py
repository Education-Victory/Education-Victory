from django.db import models
from accounts.models import CustomUser
# Create your models here.

class WebUser(models.Model):
	user = models.OneToOneField(CustomUser, on_delete = models.CASCADE, null=True, blank=True)
	name = models.CharField(max_length = 200, null = True)
	email = models.CharField(max_length = 200, null = True)
	avatar = models.CharField(max_length = 200, null = True)
	def __str__(self):
		return self.name
