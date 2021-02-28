from django.test import TestCase
from django.urls import resolve
from apps.events.models import Event, Subscription
from apps.accounts.models import User
from apps.events.views import EventListView, EventDetailView, LandingView


# Create your tests here.

class LandingPageTest(TestCase):

    def test_resolving_view(self):
        found = resolve('/')
        self.assertEquals(found.url_name, 'land')

    def test_correct_redirect(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code,302)

class EventViewData:
    
    user = {'username':'my_user',
            'email':'myuser@awd.cm',
            'password':'1223132123'
    }
    event = {'title':"my event ",
            'description':"some descritption will never"\
            +"be able to convey a proper idea of"\
            +" what will actually occur",
            'state':'PU'}

class EventDetailViewTest(TestCase):
    '''
        Test on event details view at url /events/<int:pk>

    '''

    def setUp(self):

        user = EventViewData.user
        event = EventViewData.event

        self.my_user = User.objects.create(
            username=user['username'],
            email=user['email'],
            password=user['password'],
        )
        
        self.event = Event(
                title=event['title'],
                description=event['description'],
                author=self.my_user,
                state=event['state'],
            )
        
        self.event.save()

    def test_resolving_views(self):
        response = self.client.get('/events/'+str(self.event.pk))
        self.assertTemplateUsed(response,'events/event.html')
        
        event = response.context['event']
        self.assertTrue(event.title == self.event.title)
        self.assertTrue(event.author == self.event.author)
        self.assertTrue(event.description == self.event.description)
        self.assertTemplateUsed(response,'events/event.html')
        

    def tearDown(self):
        pass

class EvenListViewTest(TestCase):

    def setUp(self):
        user = EventViewData.user
        event = EventViewData.event

        self.my_user = User.objects.create(
            username=user['username'],
            email=user['email'],
            password=user['password'],
        )
        self.my_user.save()
        event_num = 10
        self.events = []
        for _ in range(event_num):
            e = Event(
                title=event['title'],
                description=event['description'],
                author=self.my_user,
                state=event['state'],
            )
            e.save()
            self.events.append(e)

    def test_event_list(self):
        
        response = self.client.get('/events/')
        html = response.content.decode('utf-8')
        self.assertTemplateUsed(response,'events/event_list.html')

        for saved_event in self.events:
            self.assertIn('<div class="card"  id="event_'+str(saved_event.pk)+'">',html)
        self.assertTrue(len(response.context['event_list'])==10)

        
    def tearDown(self):
        pass