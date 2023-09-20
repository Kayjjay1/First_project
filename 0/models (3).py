from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

class UserModel(AbstractUser):

    other_name = models.CharField(max_length=16)

    dob = models.DateField(max_length=16, null=True)
    
    # unique nin field
    username = models.CharField(max_length=11, unique=True)

    blood_group = models.CharField(max_length=2)

    genotype = models.CharField(max_length=2)

    phonenumber = models.CharField(max_length=11)

    date_registered = models.DateTimeField(auto_now_add=True)

    last_updated = models.DateTimeField(auto_now=True)
