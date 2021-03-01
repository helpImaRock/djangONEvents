from django import forms
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import datetime
from apps.accounts.models import User


class Event(models.Model):

    class StateChoices(models.TextChoices):
        '''
            class defining static variables
            encoding Event state from human readable
            to database representation
        '''
        DRAFT = 'DF', _('Draft')
        PUBLIC = 'PU', _('Public')
        PRIVATE = 'PR', _('Private')

    # title of the event
    title = models.CharField(
        "title", max_length=30, blank=False, default=''
    )
    # description f the event
    description = models.TextField(
        "description", max_length=200, null=False, default=''
    )
    # event date
    date = models.DateField("date", null=False, default=datetime.date.today)
    
    # associates an user (foreignKey) to an event
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    # state described by inner class StateChoices
    state = models.CharField(
        "state", max_length=2,
        choices=StateChoices.choices,
        default=StateChoices.DRAFT
    )

    class Meta:
        db_table = "events"
        ordering = ['date']
        ## this yields and error if a date is gte than the current date
        ## frontend checks not enforced 

        #constraints = [
        #    models.CheckConstraint(check=models.Q(
        #        date__gte=datetime.date.today()), name='date_gte_present'
        #    ),
        #]
        verbose_name = "event"
        verbose_name_plural = "events"

    def get_absolute_url(self):
        return reverse('event-detail', args=[str(self.id)])

    def __str__(self):
        return 'id: '+str(self.id)+' title: '+self.title + "\ndescription: " + str(self.description)\
                + '\nauthor: ('+str(self.author)+ ')\ndate: ' +str(self.date)\
                + '\state: '+self.state


class Subscription(models.Model):
    '''
        Subscription class for events
        many-to-many with events and users
    '''
    
    # associates an user model (foreignKey) with a subscription
    subscriber = models.ForeignKey(
        User, on_delete=models.CASCADE,
        null=False, default=''
    )
    # associates an event model (foreignKey) with a subscription
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE,
        null=False, default=''
    )
    # subscripition comment field
    comment = models.TextField("comment", null=False)
    # a date for a subscription
    date = models.DateField(
        "date", default=datetime.date.today
    )

    class Meta:
        db_table = "subscriptions"
        ordering = ['date'] # orders subscription list by date

    def __str__(self):
        return "event: " + str(self.event) + "\ncomment: "\
            + str(self.comment) +" "+str(self.subscriber)