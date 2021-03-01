import unittest
from selenium.webdriver.firefox.webdriver import WebDriver
from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import time
from apps.accounts.models import User

host = 'http://localhost:8000'

class UserRegistrationTestClass(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def navigateToRegistration(self):
        '''
            navigates to signup form root url
        '''
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

class NewUserRegistrationTestClass(LiveServerTestCase):
    '''
        class tests apps accounts related operations
        signIn, signUp
    '''

    @classmethod
    def setUpClass(cls):
        #super().setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        #super().tearDownClass()


    def navigateToRegistration(self):
        '''
            navigates to signup form root url
        '''
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

    def test_user_invalid_signup_existing_user(self):
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

        ## log user out
        profile_logout = self.selenium.find_element_by_id('user_logout')
        log_out_link = profile_logout.get_attribute('href')
        self.selenium.get(log_out_link)

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_id('sign_up')
        )

        self.navigateToRegistration()

        self.submitSignUpForm(username,email,password)
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_id('login_error')
        )
        profile = self.selenium.find_element_by_id('login_error')
        self.assertEquals(profile.text,'User with this Username already exists. Sign In')
        
        ## no new user exists at this point in the queried db
        ## yet db file contains this user


class LoginTestClass(LiveServerTestCase):

    '''
        tests logging in in existing users, regular and
        anonymous
        and non existing users
    '''

    @classmethod
    def setUpClass(cls):
        #super().setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        #super().tearDownClass()

    def navigateToLogin(self):
        '''
            navigates to signup form root url
        '''
         ## access website
        self.selenium.get('%s%s' % (host, '/'))
        registration_link = self.selenium.find_element_by_id('sign_in')
        
        ## navigate to login page
        sign_in_link = registration_link.get_attribute('href')
        self.selenium.get(sign_in_link)

        username = "my_user"
        email = "myuser@mydomain.com"
        password = "awdaw1234"

    
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
        submit_button = self.selenium.find_element_by_tag_name('button')
        submit_button.click()


    def test_valid_login_logout_existing_regular_user(self):
        '''
            tests regular existing user valid login
        '''
        timeout = 2

        self.navigateToLogin()

        ## fill the form with valid data
        username = "my_user"
        password = "awdaw1234"
        self.submitSignInForm(username,password)

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_id('user_controls')
        )
        profile = self.selenium.find_element_by_id('user_controls')
        self.assertEquals(profile.text,username)

        ## log user out
        profile_logout = self.selenium.find_element_by_id('user_logout')
        log_out_link = profile_logout.get_attribute('href')
        self.selenium.get(log_out_link)

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_id('sign_up')
        )


    def _invalid_login(self,username,password):

        timeout = 2

        self.navigateToLogin()

        ## fill the form with valid data
        self.submitSignInForm(username,password)

        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_id('login_error')
        )
        login_error = self.selenium.find_element_by_id('login_error')
        self.assertEquals(login_error.text,'Wrong credentials please try again')

    def test_invalid_login_existing_regular_user(self):
        '''
            tests regular existing user valid login
        '''

        username = "my_user"
        password = "awdaw123d4"
        self._invalid_login(username,password)

    
    def test_invalid_login_anonymous_user(self):
        '''
            tests regular existing user valid login
        '''
        user = User(
            username='awdge',password='adwdawawdawd',
            email='awda@awdaw.com',is_anon=True,is_active=False
        )
        user.save()
        
        username = "awdge"
        password = "awdaw123d4"
        self._invalid_login(username,password)
