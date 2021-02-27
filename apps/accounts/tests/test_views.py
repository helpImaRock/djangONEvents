from django.test import TestCase
from apps.accounts.views import SignUpFormView


class UserRegistrationViewTest(TestCase):

    def setUp(self):
        pass

    def test_successfull_login_view(self):
        '''
            tests successful login on view
        '''
        ## post with form data to /accounts/login
        response = self.client.post('/accounts/login',
            data = {'username': 'awd',
                    'password': '123'
                    }
        )
        ## checks for a redirecto to main page
        self.assertEquals(response.status_code,302)
        self.assertTemplateUsed(response, 'event_list.html')

    def test_unsuccessful_login_view(self):
        '''
            tests unsuccessful login on view
        '''

        ## post with form data to /accounts/login
        response = self.client.post('/accounts/login',
            data = {'username': 'awd@fakwg.com',
                    'password': '123',
                    }
        )
        self.assertEquals(response.status_code,200)
        html = response.content.decode('utf8')
        self.assertTemplateUsed(response, 'login.html')
        self.assertIn("Wrong credentials please try again",html)

    def tearDown(self):
        pass

class UserLoginViewTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass