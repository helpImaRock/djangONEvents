from django.shortcuts import render,redirect
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.views.generic import View, ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from django.db.utils import IntegrityError
from django.db.models import Q
import datetime
from django.urls import reverse_lazy, reverse
from .models import Event, Subscription
from .forms import EventForm, SubscriptionForm
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

ANONYMOUS_PASSWORD = settings.ANONYMOUS_PASSWORD

class ErrorPageNotFoundView(View):

    root='/'

    def __init__(self,request, *args, **argv):
        return HttpResponseRedirect('/events/')


class LandingView(View):

    def get(self, request):
        return HttpResponseRedirect('events/')

class EventListView(ListView):
    template_name = 'event_list.html'
    context_object_name = 'event_list'
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EventDetailView(DetailView):
    template_name = 'event.html'
    queryset = Event.objects.all()

    def get_object(self):
        return super().get_object()
    

class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'event_update.html'
    success_url = '/events/'


class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'event_create.html'
    success_url = '/events/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class EventDeleteView(DeleteView):
    '''
        class for Event Deletion
        update to send a confirmation message
        implement delete() to limit deletes
    '''
    model = Event
    success_url ="/"

class SubscriptionListView(ListView):
    template_name = 'sub_list.html'
    context_object_name = 'subscription_list'
    model = Subscription

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SubscriptionCreateView(CreateView):
    model = Subscription
    form_class = SubscriptionForm
    success_url = '/events/'

    def form_invalid(self, form, event, error_msg):
        response = super().form_invalid(form)
        print(self.request)
        messages.add_message(self.request, messages.ERROR, error_msg)
        response = HttpResponseRedirect(self.get_success_url()+str(event.id))
        return response

    def save_valid_object(self,event,user,info_message):
        
        self.object.event = event
        self.object.subscriber = user
        self.object.save()
        messages.add_message(self.request, messages.INFO, info_message)
        return HttpResponseRedirect(self.get_success_url()+str(event.id))

    def form_valid(self,form,event):
        '''
            performs numerous checks
            for different users states
        '''
        self.object = form.save(commit=False)
        email = form.cleaned_data['email']
        name = form.cleaned_data['username']
        info_message = _('You are subscribed to this event')
        error_message = _('User already subscribed to event')
        
        # if request came from a non loggedIn user
        if self.request.user.is_anonymous:
            User = get_user_model()
            ## check if a user with that username 
            ## or email is registered
            user_query = User.objects.filter(
                    Q(username=name) |
                    Q(email=email)
                    )
            ## if not, create the anonymous user 
            user = None
            if len(user_query) == 0:
                    ## instantiates an anonymous user
                    ## and saves it
                user = User.objects.create(
                    username=name,
                    email=email,
                    password=ANONYMOUS_PASSWORD,
                    is_anon=True,
                    is_active=False
                )
            elif len(user_query) > 0:
                user = user_query[0]
                ## check if there already is a subscription
                ## to this event by this user
                ## if so return error
                subs = Subscription.objects.filter(subscriber=user,event=event)
                if len(subs) > 0:
                    return self.form_invalid(form, event, error_message)
            return self.save_valid_object(event, user, info_message)
        else:
            print("NOT ANONYMOUS REQUEST")
            return self.save_valid_object(event,self.request.user,info_message)    
        return HttpResponseRedirect(self.get_success_url()+str(event.id))


class SubscriptionDeleteView(DeleteView):
    '''
        class for Subscripiton Deletion
        update to send a confirmation message
        implement delete() from DeletionMixin
    '''
    model = Subscription
    success_url ="/"

class SubscriptionUpdateView(UpdateView):
    pass


class EventDetailSubscriptionsView(EventDetailView, SubscriptionCreateView):
    '''
        View extends on Event DetailView
        implementing get_context_data and post methods
        'subscriptions' key of event added to context
        'subscription' key is a subscription if user that
        made the request is subscribed to event, None if not
        
    '''

    form_class = SubscriptionForm
    subscriptions_queryset = Subscription.objects.all()

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        event = self.object
        context['subscriptions'] = Subscription.objects.filter(
            event=context["object"].id
        )
        if not user.is_anonymous:
            query = Subscription.objects.filter(subscriber=user, event=event)
            if len(query) != 0:
                context['subscription'] = query[0]
            else:
                context['subscription'] = None
        else:
            context['subscription'] = False
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        event = super().get_object()
        return super().form_valid(form, event)