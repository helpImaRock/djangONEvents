from django.test import TestCase,Client
from django.urls import resolve
from django.http import HttpRequest
from events.views import LandingView

# Create your tests here.

class LandingPageTest(TestCase):

    def test_resolving_view(self):
        found = resolve('/')
        self.assertEqual(found.view_name,LandingView.template_name[:-5])

    def test_render_html_correctly(self):
        response = self.client.get('/')

        html = response.content.decode('utf-8')
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn("<title>ONEvents</title>",html)
        self.assertTrue(html.endswith('</html>'))
        self.assertTemplateUsed(response,'land.html')




""" class RegistrationTest(TestCase):
    
    def test_resolving_view(self):
        found = resolve('/accounts/registration/')
        self.assertEqual(found.view_name,RegistrationView.template_name[:-5])

    def test_render_html_correctly(self):

        response = self.client.get('/accounts/registration/')

        html = response.content.decode('utf-8')
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn("<title>ONEvents</title>",html)
        
        self.assertIn("<form action",html)
        self.assertIn("</form>",html)
        self.assertTrue(html.endswith('</html>'))
        self.assertTemplateUsed(response,'register.html')


class LoginTest(TestCase):
    
    def test_resolving_view(self):
        found = resolve('/accounts/login/')
        self.assertEqual(found.view_name,LoginView.template_name[:-5])

    def test_render_html_correctly(self):

        response = self.client.get('/accounts/login/')

        html = response.content.decode('utf-8')
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn("<title>ONEvents</title>",html)
        self.assertIn("<form action",html)
        self.assertIn("</form>",html)
        self.assertTrue(html.endswith('</html>'))
        self.assertTemplateUsed(response,'login.html') """



