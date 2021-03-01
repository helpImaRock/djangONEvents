from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic.base import RedirectView
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import SignUpForm, LoginForm
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.views import View


# Create your views here.


class SignUpFormView(FormView):
    '''
        class responding to GET,POST requests at 'accounts/signup'
        creating a new user through tied SignUpForm
        logs in and redirects user if successful to /
    '''
    template_name = 'signup.html'
    form_class = SignUpForm
    success_url = '/events/'

    def form_valid(self, form):
        """
            called if form is valid
            process user signup
        """
        user = form.save(commit=False)
        b = user.save()
        a = login(self.request, user)
        if user is not None:
            return HttpResponseRedirect(self.success_url)
        return super().form_valid(form)

    def form_invalid(self, form):
        '''
            called if form is invalid
        '''
        response = super().form_invalid(form)
        return response


class LogoutView(View):
    '''
        class responding to GET requests at 'accounts/logout'
        redirecting to /
    '''

    # replies to GET with redirect
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('land'))

class LoginFormView(FormView):
    '''
        class implementing the user login view
        responds to GET, POST requests at 'accounts/login'
        tied to form LoginForm
    '''
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/events/'
    #success_message = "%(username)s logged In"


    def form_valid(self, form):
        """
            called if form is valid
            process user signup
        """
        # cleans form data
        credentials = form.cleaned_data

        # authenticates the user
        user = authenticate(username=credentials['username'],
                            password=credentials['password'])

        # if authentication unsuccessful
        # log in and redirect to /
        if user is not None:
            a = login(self.request, user)
            return HttpResponseRedirect(self.success_url)

        # adds an ERROR message and redirects same page
        else:
            messages.add_message(self.request, messages.ERROR, _('Wrong credentials '
                    +'please try again'))
            response = HttpResponseRedirect(reverse_lazy('login'))
            return response

    def form_invalid(self, form):
        '''
            called if form is invalid
        '''
        response = super().form_invalid(form)
        return response
