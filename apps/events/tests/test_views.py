from django.test import TestCase
from apps.events.models import Event,EventForm
from django.urls import resolve

from apps.events.views import EventListView,EventDetailView


class EventListViewTest(TestCase):

    def setUp(self):
        
        event_num = 10
        for event_id in range(event_num):
            Event.objects.create(
                title="my event "+str(event_id),
                description="some descritption",
                author="self",
            )

    def test_resolving_view(self):
        found = resolve('/events/')
        self.assertEqual(found.view_name,"event-list")

    def test_lists_events(self):

        response = self.client.get('/events/')

        html = response.content.decode('utf-8')
        self.assertTrue(len(response.context['event_list'])==10)
        self.assertTemplateUsed(response,'events/event_list.html')


    def tearDown(self):
        pass


class EvenDetailViewTest(TestCase):

    def setUp(self):
        Event.objects.create(
            title="my title",
            description = "some description of a happening",
            author = "self less"
        )
        self.event = Event.objects.get(title="my title")

    def test_resolving_view(self):
        found = resolve('/events/'+str(self.event.pk))
        self.assertEqual(found.view_name,"event-detail")

    def test_event(self):
        response = self.client.get('/events/'+str(self.event.pk))

        html = response.content.decode('utf-8')
        event = response.context['event']
        self.assertTrue(event.title == self.event.title)
        self.assertTrue(event.author == self.event.author)
        self.assertTrue(event.description == self.event.description)
        self.assertTemplateUsed(response,'events/event.html')


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

        

        
