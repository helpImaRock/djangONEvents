from django.utils import timezone
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from events.events.models import Event

## check https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-display/#listview
class EventListView(ListView):
    template_name = 'event_list.html'
    context_object_name = 'event_list'
    model = Event

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class EventDetailView(DetailView):
    template_name = 'event.html'
    queryset = Event.objects.all()

    def get_object(self):
        return super().get_object()
