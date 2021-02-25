from django import forms
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import re

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

    def create_user(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
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


class SignUpForm(forms.ModelForm):
    '''registration form'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs.update(
            {'placeholder': _('username')}
        )
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'placeholder': _('email')})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update(
            {'placeholder': _('password')}
        )
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update(
            {'placeholder': _('confirm password')}
        )

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    _("Passwords don't match"), code='invalid'
                )
        return password2

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            if re.search(r'\b[a-z0-9]+@[a-z]+.[a-z0-9]{2,5}\b', email) is None:
                raise ValidationError(_("Invalid email"), code='invalid')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    ''' login form '''
    username = forms.CharField(label='username', max_length=60)
    password = forms.CharField(label='password', widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs.update(
            {'placeholder': _('username')}
        )
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update(
            {'placeholder': _('password')}
        )

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')
