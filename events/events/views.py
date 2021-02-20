from django.utils import timezone
from django.views.generic import ListView

from events.events.models import Event

## check https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-display/#listview
class EventListView(ListView):
    template_name = 'event-list.html'
    context_object_name = 'event_list'
    model = Event

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
