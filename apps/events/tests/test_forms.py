from apps.events.forms import EventForm, SubscriptionForm
from apps.events.models import Event
from apps.accounts.models import User
from django.test import TestCase
from django.urls import resolve

class EventFormViewTest(TestCase):

    def setUp(self):

        self.event = {'title':"my event ",
            'description':"some descritption will never"\
            +"be able to convey a proper idea of"\
            +" what will actually occur",
            'state':'PU'}

        self.user = {'username':'my_user',
            'email':'myuser@awd.cm',
            'password':'1223132123'
        }

    def test_resolving_view(self):
        found = resolve('/events/create')
        self.assertEqual(found.view_name,"event-create")

    def test_event_form(self):

        response = self.client.get('/events/create')
        html = response.content.decode('utf-8')

        user = User(**self.user)
        event = Event(author=user,**self.event)
        form = EventForm(instance=event)
        #self.assertTrue(form.is_valid())