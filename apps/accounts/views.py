from django.shortcuts import render, redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import FormView
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.urls import reverse_lazy
from .models import SignUpForm, LoginForm
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext_lazy as _

# Create your views here.


class SignUpFormView(FormView):
    template_name = 'signup.html'
    form_class = SignUpForm
    success_url = '/events/'

    def form_valid(self, form):
        """ process user signup"""
        user = form.save(commit=False)
        user.save()
        a = login(self.request, user)
        if user is not None:
            return HttpResponseRedirect(self.success_url)
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        return response


def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('land'))


class LoginFormView(FormView,SuccessMessageMixin):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/events/'
    #success_message = "%(username)s logged In"


    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        credentials = form.cleaned_data

        user = authenticate(username=credentials['username'],
                            password=credentials['password'])
        if user is not None:
            a = login(self.request, user)
            return HttpResponseRedirect(self.success_url)

        else:
            messages.add_message(self.request, messages.ERROR, _('Wrong credentials '
                    +'please try again'))
            #return HttpResponseRedirect(reverse_lazy('login'))
            return render(self.request, 'login.html')

    def form_invalid(self, form):
        response = super().form_invalid(form)
        return response
