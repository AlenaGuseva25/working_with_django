from django.contrib.auth.models import AbstractUser
from django.db import models

from config.settings import MODERATOR_GROUP


class User(AbstractUser):
    #username = models.CharField(max_length=150)
    email = models.EmailField(unique=True, verbose_name='Email')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Аватар')
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='Номер телефона')
    country = models.CharField(max_length=50, null=True, blank=True, verbose_name='Страна')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email

    @property
    def is_moderator(self) -> bool:
        return self.groups.filter(name=MODERATOR_GROUP).exists()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['email']