from django.db import models
import datetime


class Dealers(models.Model):
    class Meta:
        verbose_name_plural = "Dealers"

    dealerID = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    telephone = models.CharField(max_length=12)
    isBlocked = models.BooleanField(default=False)


class Orders(models.Model):
    class Meta:
        verbose_name_plural = "Orders"

    dealerID = models.ForeignKey(Dealers, db_column='dealerID', on_delete=models.CASCADE)
    # dealer_user_name = models.CharField(max_length=30)
    model = models.IntegerField()
    colour = models.CharField(max_length=1000)
    date = models.DateField(auto_now_add=True)
    homologation = models.BooleanField(default=False)
    custom_clearance = models.BooleanField(default=False)

    scheduled_completion_date = models.CharField(max_length=100)
    deposit_received = models.BooleanField(default=False)
    payment_received = models.BooleanField(default=False)


class Vehicles(models.Model):
    model = models.CharField(max_length=1000)
    headline = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)
    image = models.ImageField(default='bow.png', upload_to='vehicles/', blank=True, null=True)
