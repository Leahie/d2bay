from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from core.models import TimeStampedModel

# Create your models here.
class CustomUser(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(max_length=500, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)

    interest_field = [
            ('music', 'Music'),
            ('sports', 'Sports'),
            ('travel', 'Travel'),
            ('reading', 'Reading'),
            ('gaming', 'Gaming'),
        ]
    interests = models.CharField(
        choices=interest_field,
        max_length = 20,
        null=True,
        blank=True
    )