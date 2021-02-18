from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from events.components.userDataForm import UserForm

# Create your views here.

class LandingView(TemplateView):
    template_name = 'land.html'
    
    def get(self,request):
        return render(request,LandingView.template_name)


## check https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-display/#listview
class EventsView(TemplateView):
    template_name = 'events.html'

    def get(self,request):
        return render(request,EventsView.template_name)


class UserDataView(FormView):
    formClass = UserForm
    
    def form_valid(self,form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)

class RegistrationView(UserDataView):
    template_name = 'register.html'
    
    def get(self,request):
        return render(request,RegistrationView.template_name)

class LoginView(UserDataView):
    template_name = 'login.html' 
    
    def get(self,request):
        return render(request,LoginView.template_name)

    