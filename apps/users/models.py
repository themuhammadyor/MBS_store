from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import ImageField, DecimalField, ForeignKey, CASCADE, PositiveIntegerField, TextField, CharField
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


class Follow(AbstractBaseModel):
    follower = ForeignKey('User', on_delete=CASCADE, related_name='following')
    followed = ForeignKey('User', on_delete=CASCADE, related_name='followers')

    class Meta:
        unique_together = ('follower', 'followed')

    def __str__(self):
        return f"{self.follower} follows {self.followed}"


class Feedback(AbstractBaseModel):
    user = ForeignKey('User', on_delete=CASCADE, related_name='feedbacks')
    body = TextField()
    like_count = PositiveIntegerField(default=0)


class Card(AbstractBaseModel):
    name = CharField(max_length=250)
    cover = ImageField(upload_to='cards/')


class UserCard(AbstractBaseModel):
    COLOR_CHOICES = [
        ('#FF5733', 'Red'),
        ('#33FF57', 'Green'),
        ('#3357FF', 'Blue'),
        ('#F3FF33', 'Yellow'),
        ('#000000', 'Black'),
        ('#FFFFFF', 'White'),
    ]

    user = ForeignKey('User', on_delete=CASCADE, related_name='user_cards')
    card = ForeignKey('Card', on_delete=CASCADE, related_name='user_cards')
    balance = DecimalField(max_digits=10, decimal_places=2, default=1000.00)
    color = CharField(max_length=7, choices=COLOR_CHOICES, default='Blue')
    password = CharField(max_length=28)
    code = PositiveIntegerField(max_length=16, unique=True)
