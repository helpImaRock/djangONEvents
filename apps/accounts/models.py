from django import forms
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

# Create your models here.


class UserManager(BaseUserManager):
    use_in_migration = True  # ?

    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError(_('email must be set'))
        if not username:
            raise ValueError(_('username must be set'))
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_regular_user(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_anonymous_user(self, username, email, **extra_fields):
        extra_fields.setdefault('is_active',False)
        extra_fields.setdefault('is_anon',False)
        return self._create_user(username, email, password, **extra_fields)
    
    def create_user(self, username, email, **extra_fields):
        print("password: ",password)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        print("password: ",password)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField('username', max_length=40,
                                unique=True, blank=False)
    email = models.CharField('email', max_length=40, unique=True, default='')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    is_anon = models.BooleanField(
        "anonymous_user", default=False,
        help_text='allows for an "anonymous user to save username and email.'
    )
    is_superuser = models.BooleanField(
        'staff status',
        default=False,
        help_text='superuser error bypass',
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS =['email']

    objects = UserManager()

    def __str__(self):
        return 'username:' + self.username + ', email: ' + self.email

