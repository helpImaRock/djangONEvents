from django.shortcuts import render,redirect
from django.views.generic.edit import FormView
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.urls import reverse_lazy
from .models import SignUpForm,LoginForm
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.


class SignUpFormView(FormView):
    template_name = 'signup.html'
    form_class = SignUpForm
    success_url = '/events/'

    def form_valid(self, form):
        """ process user signup"""
        print(form)
        user = form.save(commit=False)
        user.save()
        login(self.request, user)
        if user is not None:
            return HttpResponseRedirect(self.success_url)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        #print("INVALID FORM")
        print(form.errors)
        response = super().form_invalid(form)
        return response

    
def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('accounts:logout'))

class LoginFormView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/events/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        credentials = form.cleaned_data

        user = authenticate(username=credentials['username'],
                            password=credentials['password'])

        if user is not None:
            login(self.request,user)
            return HttpResponseRedirect(self.success_url)

        else:
            messages.add_message(self.request,messages.INFO,'Wrong credentials\
                    please try again')
            return HttpResponseRedirect(reverse_lazy('accounts:login'))