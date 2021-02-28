from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.utils.translation import ugettext_lazy as _
import re


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

    password1 = forms.CharField(label='password', min_length=8, widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', min_length=8, widget=forms.PasswordInput
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'email','password1','password2')
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if len(password2) <8 or len(password1) <8:
             raise ValidationError(
                    _("Password too small must have at least 8 characters"), code='invalid'
                )
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    _("Passwords mismatch."), code='invalid'
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
    password = forms.CharField(label='password',min_length=8, widget=forms.PasswordInput())

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
