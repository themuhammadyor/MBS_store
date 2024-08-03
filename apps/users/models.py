from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import ImageField
from phone_field import PhoneField

from apps.shared.models import AbstractBaseModel


class User(AbstractUser, AbstractBaseModel):
    avatar = ImageField(upload_to='avatars/', default='default-avatar')
    phone = PhoneField(blank=True, help_text='Contact phone number')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
