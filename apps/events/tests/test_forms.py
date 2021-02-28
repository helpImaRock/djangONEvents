from apps.events.forms import EventForm, SubscriptionForm
from django.test import TestCase
from django.urls import resolve

class EventFormViewTest(TestCase):

    def setUp(self):
        self.event = {
                "title": " my super duper title",
                "description": "this is an event that will be ocurring on ...",
                "author": "django",
                }

    def test_resolving_view(self):
        found = resolve('/events/new')
        self.assertEqual(found.view_name,"event-form")

    def test_event_form(self):

        response = self.client.get('/events/new')
        html = response.content.decode('utf-8')

        form = EventForm(data=self.event)
        form.is_valid()