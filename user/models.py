from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    zip = models.CharField(max_length=10)
    first_name =  models.CharField(max_length=100)
    last_name =  models.CharField(max_length=100)