from django.db import models
from django.contrib.auth.models import AbstractUser
from .models_saves import StartGame

class CustomAuth(AbstractUser):
	saves = models.ManyToManyField(StartGame, blank=True)

	active_save = models.IntegerField(default=0)

	@property
	def isauthenticated(self):
		return True