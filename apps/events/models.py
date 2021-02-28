from django import forms
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import datetime
from apps.accounts.models import User


class Event(models.Model):

    class StateChoices(models.TextChoices):
        DRAFT = 'DF', _('Draft')
        PUBLIC = 'PU', _('Public')
        PRIVATE = 'PR', _('Private')

    title = models.CharField(
        "title", max_length=30, blank=False, default=''
    )
    description = models.TextField(
        "description", max_length=200, null=False, default=''
    )
    date = models.DateField("date", null=False, default=datetime.date.today)
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
        return 'title: '+self.title + "\ndescription: " + str(self.description)\
                + '\nauthor: ('+str(self.author)+ ')\ndate: ' +str(self.date)\
                + '\state: '+self.state


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
        return "event" + ": " + str(self.id) + "user" + ": " \
            + self.subscriber.username + "comment" \
            + ": " + str(self.comment)