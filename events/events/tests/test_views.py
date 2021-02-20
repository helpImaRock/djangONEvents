from django.test import TestCase
from events.events.models import Event
from django.urls import resolve

from events.events.views import EventListView


class EventListViewTest(TestCase):

    def setUp(self):
        
        event_num = 10
        for event_id in range(event_num):
            Event.objects.create(
                title=event_id,
                description="some descritption",
                author="self",
            )

    def test_resolving_view(self):
        found = resolve('/events/')
        self.assertEqual(found.view_name,EventListView.template_name[:-5])

    def test_lists_events(self):

        response = self.client.get('/events/')

        html = response.content.decode('utf-8')
        self.assertTrue(len(response.context['event_list'])==10)
        self.assertTemplateUsed(response,'event-list.html')


    def tearDown(self):
        pass