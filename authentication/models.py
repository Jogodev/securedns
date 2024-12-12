from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=100)
    
    USER_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
