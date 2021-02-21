"""djangONEvents URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from apps.events.views import EventListView,EventDetailView,EventCreateView,LandingView
from apps.accounts.views import SignUpFormView, LoginFormView

urlpatterns = [
    #path('admin/', admin.site.urls),
    
    path('',LandingView.as_view(template_name = 'land.html'),name="land"),
    path('accounts/login',LoginFormView.as_view(),name='login'),
    path('accounts/signup',SignUpFormView.as_view(),name='signup'),
    path('admin/',admin.site.urls),
    path('events/',EventListView.as_view(template_name='events/event_list.html'),name="event-list"),
    path('events/new',EventCreateView.as_view(template_name='events/new.html'),name="event-form"),
    path('events/<int:pk>',EventDetailView.as_view(template_name='events/event.html'),name="event-detail"),

    
    #path('accounts/registration/',RegistrationView.as_view(),name="register"),
    #path('accounts/login/',LoginView.as_view(),name="login"),
]
