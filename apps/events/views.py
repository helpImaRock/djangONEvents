from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.views.generic import ListView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
import datetime
from .models import Event, EventForm, Subscription, SubscriptionForm

ANONYMOUS_PASSWORD = '111333555'


class LandingView(TemplateView):

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


class EventFormView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'new.html'
    success_url = '/events/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class SubscriptionListView(ListView):
    template_name = 'subscription_list.html'
    context_object_name = 'subscription_list'
    model = Subscription

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SubscriptionFormView(CreateView):
    model = Subscription
    form_class = SubscriptionForm
    template_name = 'new.html'
    success_url = '/events/<int:event_id>'

    def form_valid(self, form, event):
        self.object = form.save(commit=False)

        if self.request.user.is_anonymous:
            email = form.cleaned_data['email']
            name = form.cleaned_data['username']
            User = get_user_model()
            user = User.objects._create_user(
                username=name,
                email=email,
                password=ANONYMOUS_PASSWORD,
                is_anon=True
            )
            self.object.subscriber = user
        else:
            self.object.subscriber = self.request.user
        self.object.event = event
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class EventSubscriptionView(EventDetailView, SubscriptionFormView):
    model = EventFormView.model
    form_class = SubscriptionForm
    event_instance = None

    def get_context_data(self, **kwargs):
        user = self.request.user
        event = super().get_object()
        context = super().get_context_data(**kwargs)
        context['subscriptions'] = Subscription.objects.filter(
            event=context["object"].id
        )
        if not user.is_anonymous:
            query = Subscription.objects.filter(subscriber=user, event=event)
            if len(query) != 0:
                context['subscribed'] = True
            else:
                context['subscribed'] = False
        else:
            context['subscribed'] = False
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        event = super().get_object()
        if super().form_valid(form, event):
            return HttpResponseRedirect(str(event.id))
