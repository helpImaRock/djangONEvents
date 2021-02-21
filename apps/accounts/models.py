from django import forms
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser,BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

# Create your models here.

class UserManager(BaseUserManager):
    use_in_migration = True # WTF is this?

    def _create_user(self,username,email,password,**extra_fields):

        if not email:
            raise ValueError('email must be set')
        if not username:
            raise ValueError('username must be set')
        user = self.model(email=email,username=username,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_user(self,email,password,**extra_fields):
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(email,password,**extra_fields)

    
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_superuser',True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email,password,**extra_fields)



class User(AbstractBaseUser,PermissionsMixin):

    identifier = models.CharField(_('username'),max_length=40, unique=True,blank=False)
    email = models.CharField(_('email'),max_length=40,unique=True,default='')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'identifier'

    objects = UserManager()

    def __str__(self):
        return 'user '+ self.username + 'with email' + self.email


class SignUpForm(forms.ModelForm):
    '''registration form'''
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        exclude = []


class LoginForm(forms.Form):
    ''' login form '''
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())