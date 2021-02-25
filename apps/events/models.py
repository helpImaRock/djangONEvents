from django import forms
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import datetime
from django.forms import NumberInput
from apps.accounts.models import User


class Event(models.Model):

    class StateChoices(models.TextChoices):
        DRAFT = 'DF', _('Draft')
        PUBLIC = 'PU', _('Public')
        PRIVATE = 'PR', _('Private')

    title = models.CharField(
        "title", max_length=30, unique=True, blank=False, default=''
    )
    description = models.TextField(
        "description", max_length=200, null=False, default=''
    )
    date = models.DateField("date", null=False, default='')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    state = models.CharField(
        "state", max_length=2,
        choices=StateChoices.choices,
        default=StateChoices.DRAFT
    )

    class Meta:
        db_table = "events"
        ordering = ['date']
        constraints = [
            models.CheckConstraint(check=models.Q(
                date__gte=datetime.date.today()), name='date_gte_present'
            ),
        ]
        verbose_name = "event"
        verbose_name_plural = "events"

    def get_absolute_url(self):
        return reverse('event-detail', args=[str(self.id)])

    def __str__(self):
        return self.title + " " + str(self.date)


class EventForm(forms.ModelForm):

    date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    state = forms.ChoiceField(choices=Event.StateChoices.choices)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['title'].widget.attrs.update({'placeholder': _('title')})
        self.fields['description'].widget.attrs.update(
            {'class': 'form-control'}
        )
        self.fields['description'].widget.attrs.update(
            {'placeholder': _('description')}
        )

    class Meta:
        model = Event
        exclude = ['author']


class Subscription(models.Model):

    subscriber = models.ForeignKey(
        User, on_delete=models.CASCADE,
        null=False, default=''
    )
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE,
        null=False, default=''
    )
    comment = models.TextField("comment", null=False)
    date = models.DateField(
        "date", default=datetime.date.today
    )

    def __str__(self):
        return self.id + " "+self.username + " " + self.comment

    class Meta:
        db_table = "subscriptions"
        ordering = ['date']

    def __str__(self):
        return _("event") + ": " + str(self.id) + _("user") + ": " \
            + self.subscriber.username + _("comment") \
            + ": " + str(self.comment)


class SubscriptionForm(forms.ModelForm):

    username = forms.CharField(label=_('username'), max_length=60)
    email = forms.CharField(label=_('email'),)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs.update(
            {'placeholder': _('username')}
        )
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'placeholder': _('email')})
        self.fields['comment'].widget.attrs.update({'class': 'form-control'})
        self.fields['comment'].widget.attrs.update(
            {'placeholder': _('comment')}
        )

    class Meta:
        model = Subscription
        exclude = ['event', 'date']
        fields = ('comment', )
