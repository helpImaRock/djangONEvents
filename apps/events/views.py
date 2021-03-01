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
    '''
        class implementing View
        with a redirect to events/
        responding to GET requests at '/'

    '''

    def get(self, request):
        return HttpResponseRedirect('events/')

class EventListView(ListView):
    '''
        class implementing a listing on events,
        adding events to request context data
        responding to GET requests at 'events/'
    '''
    template_name = 'event_list.html'
    context_object_name = 'event_list'
    model = Event

    # method probably unneeded
    # as super().get_context_data(**kwargs) is called
    # confirm in docs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EventDetailView(DetailView):
    '''
        class implementing
        a view on the event model
        responding to GET requests at 'events/<int:pk>'
        subclassed by EventDetailSubscriptionsView
    '''
    template_name = 'event.html'
    queryset = Event.objects.all()

    

class EventUpdateView(UpdateView):
    '''
        class implementing a view for updating
        an Event, tied to a ModelForm implementing
        class EventForm
        responding to GET and POST requests at 'events/<int:pk>/update'
    '''
    model = Event
    form_class = EventForm
    template_name = 'event_update.html'
    success_url = '/events/'


class EventCreateView(CreateView):
    '''
        class implementing a view for creating
        an Event, tied to a ModelForm implementing
        class EventForm
        responding to GET and POST requests at 'events/<int:pk>/create'

    '''
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
        
        ##not currently tied to any url in urls.py
        should reply to POST requests at 'events/<int:pk>/delete'
    '''
    model = Event
    success_url ="/"

class SubscriptionListView(ListView):
    '''
        class implementing a listing on subscriptions,
        adding subscriptions to request context data

        ##not currently tied to any url in urls.py
        should reply to GET requests at 'user/<int:pk>/subscriptions'
    '''
    template_name = 'sub_list.html'
    context_object_name = 'subscription_list'
    model = Subscription

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SubscriptionCreateView(CreateView):
    '''
        class implementing a view for creating
        a Subscription, tied to a ModelForm implementing
        class SubscriptionForm
        responding to POST only requests at 'events/<int:pk1>/sub/create'
        redirecting to events/<int:pk>

    '''
    model = Subscription
    form_class = SubscriptionForm
    success_url = '/events/'

    # implements form validation,
    # called by subclass EventDetailSubscriptionsView
    # on subscription submission
    def form_invalid(self, form, event, error_msg):
        response = super().form_invalid(form)
        print(self.request)
        messages.add_message(self.request, messages.ERROR, error_msg)
        response = HttpResponseRedirect(self.get_success_url()+str(event.id))
        return response

    # saves a subscription and adds a success message
    # to a redirect response
    def save_valid_object(self,event,user,info_message):
        self.object.event = event
        self.object.subscriber = user
        self.object.save()
        messages.add_message(self.request, messages.INFO, info_message)
        return HttpResponseRedirect(self.get_success_url()+str(event.id))

    # called by subclass EventDetailSubscriptionsView
    # calls save_valid_object if 
    # object validity True
    # calls form_invalid if not
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
            return self.save_valid_object(event,self.request.user,info_message)    
        return HttpResponseRedirect(self.get_success_url()+str(event.id))


class SubscriptionDeleteView(DeleteView):
    '''
        class for Subscripiton Deletion
        update to send a confirmation message
        implement delete() from DeletionMixin
        responds to POST requests on events/<int:id>/sub/<slug:pk>/delete
        when user clicks unsubscribe for a subscribed event
    '''
    model = Subscription
    success_url ="/"

class SubscriptionUpdateView(UpdateView):
    pass


class EventDetailSubscriptionsView(EventDetailView, SubscriptionCreateView):
    '''
        View extends on EventDetailView and SubscriptinCreateView
        implementing get_context_data and post methods

        'subscriptions' key added to context
        'subscription' key is a subscription if user that
        made the request is subscribed to event, None if not
        
        responds to POST, GET requests at 'events/<int:pk>'
    '''

    form_class = SubscriptionForm
    subscriptions_queryset = Subscription.objects.all()


    def get_context_data(self, **kwargs):    
        user = self.request.user
        context = super().get_context_data(**kwargs)
        event = self.object
        
        # retrieves a list of subscriptions for event
        # used to implement event owner
        # event subscriptions listing
        context['subscriptions'] = Subscription.objects.filter(
            event=context["object"].id
        )
        # checks if user is loggedin
        if not user.is_anonymous:
            query = Subscription.objects.filter(subscriber=user, event=event)
            # if the user is subscribed
            # inserts subscription in request_context
            # inserts None if not
            # used to render 'already subscribed messages'
            if len(query) != 0:
                context['subscription'] = query[0]
            else:
                context['subscription'] = None
        # returns False so subscription form is rendered
        else:
            context['subscription'] = False
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        event = super().get_object()
        # submits subscription form and associated event
        # to SubscriptinCreateView
        return super().form_valid(form, event)