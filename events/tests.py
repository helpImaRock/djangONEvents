from django.test import TestCase,Client
from django.urls import resolve
from django.http import HttpRequest
from events.views import LandingView

# Create your tests here.

class LandingPage(TestCase):

    def test_resolving_view(self):
        found = resolve('/')
        self.assertEqual(found.view_name,LandingView.template_name[:-5])

    def test_render_html_correctly(self):
        response = self.client.get('/')

        html = response.content.decode('utf-8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn("<title>ONEvents</title>",html)
        self.assertTrue(html.endswith('</html>'))
        
        self.assertTemplateUsed(response,'land.html')