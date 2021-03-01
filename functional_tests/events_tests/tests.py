import unittest
from selenium.webdriver.firefox.webdriver import WebDriver
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select

import time

class UserEventCreationTest(LiveServerTestCase,unittest.TestCase):
    '''
        class tests apps event related operations
        create instances and listing avaialable
    '''

    def setUp(self):
        self.selenium = WebDriver()

        self.event = {
            'title': 'My Title',
            'description': 'This should be a long description about an event\n'\
                                    'but am gonna keep it short',
            'state': 'Private',
            'date': '2021-12-22'

        }
    
    def tearDown(self):
        self.selenium.quit()

    def register_user(self,username,email):
        '''
            submits a POST request to accounts/signup wiht user data
            before running login with user data
        '''
        self.client.post('/accounts/signup',data={
            'username': username,
            'email': email,
            'password1': "awdaw1234",
            'password2': "awdaw1234",
        })

    def login_user(self):
        '''
            logs in an user
        '''
        self.client.post('/accounts/login',data={
            'username': "my_user",
            'password': "awdaw1234",
        })

    def navigateToLogin(self):
        '''
            navigates to signup form root url
        '''
         ## access website
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        login_link = self.selenium.find_element_by_id('sign_in')
        
        ## navigate to login page
        sign_in_link = login_link.get_attribute('href')
        self.selenium.get(sign_in_link)

    
    def submitSignInForm(self,username,password):
        '''
            submits data to sign up form
        '''
        ## find and fill input fields
        user_name_field = self.selenium.find_element_by_id('id_username')
        user_name_field.send_keys(username)
        password_field = self.selenium.find_element_by_id('id_password')
        password_field.send_keys(password)

        ## click the submit button
        submit_form = self.selenium.find_element_by_tag_name('form')
        submit_form.submit()


    def fill_event(self):
        user_name_field = self.selenium.find_element_by_id('id_title')
        user_name_field.send_keys(self.event['title'])

        description_field = self.selenium.find_element_by_id('id_description')
        description_field.send_keys(self.event['description'])

        date_field = self.selenium.find_element_by_id('id_date')
        date_field.send_keys(self.event['date'])
        
        state_field = self.selenium.find_element_by_id('id_state')
        select_object = Select(state_field)
        select_object.select_by_visible_text(self.event['state'])

        form = self.selenium.find_element_by_tag_name('form')
        form.submit()

    def test_logged_in_user_event_creation(self):
        '''
            tests a logged in user 
            can create events and view them after
        '''
        timeout = 2

        ## register user wait 1 sec
        self.register_user("my_user","myuser@mydomain.com")
        time.sleep(1)

        ## login user wait 1 sec
        self.navigateToLogin()

        self.submitSignInForm("my_user","awdaw1234")

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_id('user_controls')
        )
        
        n = 1

        for _ in range(n):
            
            ## find the create button
            create_event_button = self.selenium.find_element_by_id('create_event')
            create_event_button.click()

            WebDriverWait(self.selenium, timeout).until(
                lambda driver: driver.find_element_by_id('id_title')
            )
            
            ## fills the event form
            self.fill_event()

            ## waits for redirection, locates the events list
            WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_id('events_list')
            )

            ## checks if the displayed event
            ## matches submitted event
            card = self.selenium.find_element_by_class_name('card')
            field_state = card.find_element_by_id('event_state')
            field_author = card.find_element_by_id('event_author')
            field_date = card.find_element_by_id('event_date')
            self.assertEqual(field_state.get_attribute('innerHTML'),self.event['state'])
            self.assertEqual(field_author.get_attribute('innerHTML'),'Author:'+'my_user')
            # formatting
            #self.assertEqual(field_date.get_attribute('innerHTML'),'Date:'+self.event['date'])

    def register_event(self):
        Event

    def test_loggedIn_user_subscribes_to_events(self):
        '''
            tests subscribing to event
        '''

        timeout = 2

        ## register user wait 1 sec
        self.register_user("my_user","myuser@mydomain.com")
        time.sleep(1)
        self.register_user("my_user1","myuser2@mydomain.com")
        time.sleep(1)

        ## login user wait 1 sec
        self.navigateToLogin()

        self.submitSignInForm("my_user","awdaw1234")

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_id('user_controls')
        )