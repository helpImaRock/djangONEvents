import unittest
from selenium import webdriver
from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import time

host = 'http://localhost:8000'

class UserRegistrationTestClass(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Firefox()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def navigateToRegistration(self):
        """
            navigates to signup form root url
        """
         ## access website
        self.selenium.get('%s%s' % (host, '/'))
        registration_link = self.selenium.find_element_by_id('sign_up')
        
        ## navigate to registration page
        sign_up_link = registration_link.get_attribute('href')
        self.selenium.get(sign_up_link)

    def submitSignUpForm(self,username,email,password):
        '''
            submits data to sign up form
        '''
        ## find and fill input fields
        user_name_field = self.selenium.find_element_by_id('id_username')
        user_name_field.send_keys(username)
        email_field = self.selenium.find_element_by_id('id_email')
        email_field.send_keys(email)
        password1_field = self.selenium.find_element_by_id('id_password1')
        password1_field.send_keys(password)
        password2_field = self.selenium.find_element_by_id('id_password2')
        password2_field.send_keys(password)

        ## click the submit button
        submit_button = self.selenium.find_element_by_tag_name('button')
        submit_button.click()

"""
class ExistingRegistrationTestClass(UserRegistrationTestClass):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def testExistingUserSignUp(self):
        '''
            Testing unsuccessful new user creation
        '''

        self.navigateToRegistration()

        ## fill the form with valid data
        username = "my_user"
        email = "myuser@mydomain.com"
        password = "awdaw1234"
        self.submitSignUpForm(username,email,password)

        self.sleep(1)
"""
    
class NewUserRegistrationTestClass(UserRegistrationTestClass):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def testUserValidSignUp(self):
        '''
            Testing successful new user creation
        '''
        timeout = 2

        self.navigateToRegistration()

        ## fill the form with valid data
        username = "my_user"
        email = "myuser@mydomain.com"
        password = "awdaw1234"
        self.submitSignUpForm(username,email,password)

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_id('user_controls')
        )
        profile = self.selenium.find_element_by_id('user_controls')
        self.assertEquals(profile.text,username)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()