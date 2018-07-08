from django.db import models
import datetime

class Orders(models.Model):
	dealer_user_name = models.CharField(max_length=30)
	model = models.IntegerField()
	colour = models.CharField(max_length=1000)
	date = models.DateField(auto_now_add=True)