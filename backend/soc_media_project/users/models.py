from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from core.models import TimeStampedModel

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    # will be put into profile model 
    