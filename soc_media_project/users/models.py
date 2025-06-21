from django.db import models
from core.models import TimeStampedModel

# Create your models here.
class User(TimeStampedModel):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)