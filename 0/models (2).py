from enum import Enum
from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

class BloodGroups(Enum):

    APOSITIVE = "A+"
    ANEGATIVE = "A-"
    BPOSITIVE = "B+"
    BNEGATIVE = "B-"
    ABPOSITIVE = "AB+"
    ABNEGATIVE = "AB-"
    OPOSITIVE = "O+"
    ONEGATIVE = "O-"

class Genotypes(Enum):

    AA = "AA"
    AS = "AS"
    AC = "AC"
    SC = "SC"
    SS = "SS"
    CC = "CC"


class UserModel(AbstractUser):

    other_name = models.CharField(max_length=16)

    dob = models.DateField(max_length=16, null=True)
    
    # unique nin field
    username = models.CharField(max_length=11, unique=True)

    blood_group = models.CharField(max_length=10,  choices=((blood_group.name, blood_group.value) for blood_group in BloodGroups))

    genotype = models.CharField(max_length=2, choices=((genotype.name, genotype.value) for genotype in Genotypes))

    phonenumber = models.CharField(max_length=11)

    date_registered = models.DateTimeField(auto_now_add=True)

    last_updated = models.DateTimeField(auto_now=True)
