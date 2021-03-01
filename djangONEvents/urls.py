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

from apps.events.views import EventListView, EventDetailSubscriptionsView
from apps.events.views import LandingView, EventCreateView, EventUpdateView
from apps.events.views import SubscriptionDeleteView, SubscriptionCreateView, SubscriptionUpdateView 
from apps.accounts.views import SignUpFormView, LoginFormView, LogoutView

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('', LandingView.as_view(), name="land"),
    path(
        'accounts/login',
        LoginFormView.as_view(template_name='login.html'),
        name='login'
    ),
    path(
        'accounts/signup',
        SignUpFormView.as_view(template_name='signup.html'),
        name='signup'
    ),
    path(
        'accounts/logout',
        LogoutView.as_view(), name='logout'
    ),
    path(
        'events/',
        EventListView.as_view(template_name='events/event_list.html'),
        name="event-list"
    ),
    path(
        'events/create',
        EventCreateView.as_view(template_name='events/event_create.html'),
        name="event-create"
    ),
    path('events/<int:pk>/update',
        EventUpdateView.as_view(template_name='events/event_update.html'),
        name="event-update"
    ),
    path(
        'events/<int:pk>',
        EventDetailSubscriptionsView.as_view(template_name='events/event.html'),
        name="event-detail"
    ),
    path('events/<int:id>/sub/<slug:pk>/delete',
        SubscriptionDeleteView.as_view(template_name='subscriptions/sub_delete.html'),
        name="sub-delete"
    ),
    path('events/<int:pk1>/sub/create',
        SubscriptionCreateView.as_view(),
        name="sub-create"
    ),
    path('events/<int:pk1>/sub/<int:pk2>/update',
        SubscriptionUpdateView.as_view(),
        name="sub-update"
    ),
]

handler404 = 'apps.events.views.ErrorPageNotFoundView'