from django.test import TestCase
from apps.accounts.views import SignUpFormView


class UserRegistrationViewTest(TestCase):

    def setUp(self):
        pass

    def test_successfull_registration(self):
        '''
            tests unsuccessful registration on view
        '''
        response = self.client.post('/accounts/signup',
            data = {'username': 'awd',
                    'email': 'awfaw@awfawf.com',
                    'password1': '1232341a',
                    'password2': '1232341a'
                    }
        )
        self.assertEquals(response.status_code,302)
        self.assertEquals(response.url,'/events/')

    def tearDown(self):
        pass

class UserLoginViewTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_successfull_login_view(self):
        '''
            tests successful login on view
        '''
        """ ## post with form data to /accounts/login
        response = self.client.post('/accounts/login',
            data = {'username': 'awd',
                    'password': '123'
                    }
        )
        ## checks for a redirect to main page
        self.assertEquals(response.status_code,302)
        print(response)
        self.assertEquals(response.url, 'events/') """
        pass

    def test_unsuccessful_login_view(self):
        '''
            tests unsuccessful login on view
        '''
        pass