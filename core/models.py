from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_farmer = models.BooleanField(default=False)
    is_consumer = models.BooleanField(default=False)

class Farmer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    farmer_id = models.AutoField(primary_key=True)
    farmerUsername = models.CharField(max_length=100)
    farmerPhone = models.CharField(max_length=15, blank=True, null=True)
    farmerEmail = models.EmailField(max_length=100, blank=True, null=True)
    farmerAddress = models.CharField(max_length=100, blank=True, null=True)

class Consumer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    consumer_id = models.AutoField(primary_key=True)
    consumerUsername= models.CharField(max_length=100)
    consumerPhone= models.CharField(max_length=15)
    consumerAddress=models.CharField(max_length=100,  blank=True, null=True) 
    consumerEmail = models.EmailField(max_length=100,  blank=True, null=True)