from django import forms

class UserForm(forms.Form):
    email = forms.CharField()
    password = forms.PasswordInput()
    