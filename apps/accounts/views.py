from django.shortcuts import render,redirect
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.urls import reverse_lazy
from .models import SignUpForm,LoginForm

# Create your views here.


class SignUpFormView(CreateView):
    template_name = 'accounts/signup.html'
    form_class = SignUpForm
    success_url = '/events/'


class LoginFormView(FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = '/events/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        credentials = form.cleaned_data

        user = authenticate(username=credentials['email'],
                            password=credentials['password'])

        if user is not None:
            login(self.request,user)
            return HttpResponseRedirect(self.success_url)

        else:
            messages.add_message(self.request,messages.INFO,'Wrong credentials\
                    please try again')
            return HttpResponseRedirect(reverse_lazy('accounts:login'))