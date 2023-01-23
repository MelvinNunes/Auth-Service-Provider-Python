from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import datetime

# Create your models here.


def filepath_avatar(request, filename):
    old_filename = filename
    time_now = datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = '%s%s' % (time_now, old_filename)
    return f'usuarios/avatar/{filename}'


class User(AbstractUser):
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    email = models.EmailField(unique=True, null=False)
    birth_date = models.DateField(null=False)
    contact_1 = models.CharField(max_length=255, null=False)
    contact_2 = models.CharField(max_length=255, null=True, blank=True)
    contact_3 = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE, null=True)
