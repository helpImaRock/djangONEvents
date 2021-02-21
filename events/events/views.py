from django.utils import timezone
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
import datetime

from events.events.models import Event,EventForm,Subscription,SubscriptionForm

## check https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-display/#listview
class EventListView(ListView):
    template_name = 'event_list.html'
    context_object_name = 'event_list'
    model = Event

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context

class EventDetailView(DetailView):
    template_name = 'event.html'
    queryset = Event.objects.all()

    def get_object(self):
        return super().get_object()


class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'new.html'
    success_url = '/events/'


    def get_initial(self,*args,**kwargs):
        initial = super().get_initial(**kwargs)
        initial['title'] = 'Enter a Title'
        initial['description'] = 'Enter an event description'
        return initial


class SubscriptionListView(ListView):
    template_name = 'subscription_list.html'
    context_object_name = 'subscription_list'
    model = Subscription

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context

class SubscriptionDetailView(DetailView):
    template_name = 'subscription.html'
    queryset = Subscription.objects.all()

    def get_object(self):
        return super().get_object()


class SubscriptionForm(CreateView):
    template_name = 'new.html'
    form_class = SubscriptionForm
