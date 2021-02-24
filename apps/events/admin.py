from django.contrib import admin

# Register your models here.

from apps.events.models import Event,Subscription

admin.site.register(Event)
admin.site.register(Subscription)