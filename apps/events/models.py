from django import forms
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Event(models.Model):
    
    class StateChoices(models.TextChoices):
        DRAFT = 'DF',_('Draft')
        PUBLIC = 'PU',_('Public')
        PRIVATE = 'PR',_('Private')
    
    title = models.CharField(_("Title"),max_length=30,unique=True,blank=False,default='')
    description = models.TextField(_("Description"),max_length=200,null=False,default='')
    date = models.DateField(_("Date"),null=False,default='')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    state = models.CharField(_("State"),max_length=2,
            choices=StateChoices.choices,
            default=StateChoices.DRAFT)

    class Meta:
        db_table = "events"
        ordering = ['date']

    def get_absolute_url(self):
        return reverse('event-detail', args=[str(self.id)])

    def __str__(self):
        return self.title + " " +str(self.date)


class EventForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['title'].widget.attrs.update({'placeholder': 'Title'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Description'})
    
    class Meta:
        model = Event
        exclude = ['state','author']



class Subscription(models.Model):

    username = models.CharField(_("Username"),max_length=30)
    email = models.CharField(_("Email"),max_length=30)
    comment = models.TextField(_("Comment"),null=False)
    dateTime = models.DateTimeField(_("DateTime"),auto_now_add=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.id +" "+self.email+" "+self.comment

    class Meta:
        db_table = "subscriptions"
        ordering = ['dateTime']

class SubscriptionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['title'].widget.attrs.update({'placeholder': 'Title'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Description'})
        self.fields['Date'].widget.attrs.update({'class': 'form-control'})
        self.fields['State'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Subscription
        exclude = ['event','dateTime']

