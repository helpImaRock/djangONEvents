from django.test import TestCase
from apps.accounts.forms import SignUpForm, LoginForm
from apps.accounts.models import User
from django.utils import translation
from django.utils.translation import gettext_lazy as _


class UserFormTestData:

    my_user = {
            'username':"my_user",
            'email':"awd@myuser.com",
            'password':"12234fba",
    }
    errors = {
            'password_size': {  'pt': 'Garanta que este valor tenha pelo menos 8 caracteres',
                                'en': 'Ensure this value has at least 8 characters'
                            },
            'null_field': {  'pt': 'Este campo é obrigatório.',
                                'en': 'This field is required.'
                            },
            'password_mismatch': {  'pt': 'Palavras-chave diferem.',
                                'en': 'Passwords mismatch.'
                            },
        }

class SignUpFormTest(TestCase):
    '''
        Base valid tests for SignUp form
        at url /accounts/signup
    '''

    def setUp(self):
        super().setUp()
        self.my_user = User(
                username=UserFormTestData.my_user["username"],
                email=UserFormTestData.my_user["email"],
                password=UserFormTestData.my_user["password"]
                )

    def tearDown(self):
        super().tearDown()

    def test_init(self):
        '''
            test instance creation
            REDO!!
        '''
        form = SignUpForm(self.my_user)

    def test_init_without_entry(self):
        '''
            should raise an error if instantiated without data
            REDO!!
        '''
        with self.assertRaises(KeyError):
            SignUpForm()

    def test_sign_up_form_valid_signIn(self):
        '''
            tests Sign Up form with valid data
        '''

        form = SignUpForm({
            'username': self.my_user.username,
            'email': self.my_user.email,
            'password1': self.my_user.password,
            'password2': self.my_user.password
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.data['username'],self.my_user.username)
        self.assertEqual(form.data['email'],self.my_user.email)
        self.assertEqual(form.data['password1'], self.my_user.password)
        self.assertEqual(form.data['password2'], self.my_user.password)
        
        
        ## we now test to see if we can 
        ## retrive newly created user from db
        
        form.save()
        query_users = User.objects.filter(username=self.my_user.username)
        self.assertEqual(len(query_users),1)
        self.assertEqual(self.my_user.username,query_users[0].username)
        self.assertEqual(self.my_user.email,query_users[0].email)

class SignUpFormTestPT(TestCase):
    '''
        testing for invalid forms in PT language
        yielded error messages ares compared
        to dictionary from UserFormTestData
    '''

    def setUp(self):
        super().setUp()
        self.my_user = User(
                username=UserFormTestData.my_user["username"],
                email=UserFormTestData.my_user["email"],
                password=UserFormTestData.my_user["password"]
                )
        translation.activate('pt') # class language activation 

    def tearDown(self):
        super().tearDown()

    def test_sign_up_form_invalid_signIn(self):
        '''
            tests invalid Sign Up form with
            empty fields
        '''

        form = SignUpForm({
            'username': "",
            'email': "",
            'password1': "",
            'password2': ""
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn(UserFormTestData.errors['null_field']['pt'],form.errors['username'])
        self.assertIn(UserFormTestData.errors['null_field']['pt'],form.errors['email'])
        self.assertIn(UserFormTestData.errors['null_field']['pt'],form.errors['password1'])
        self.assertIn(UserFormTestData.errors['null_field']['pt'],form.errors['password2'])

    def test_sign_up_form_password_mismatch(self):
        '''
            tests invalid Signup were password1 field data
            does not match password2 field data
        '''

        form = SignUpForm({
            'username': self.my_user.username,
            'email': self.my_user.email,
            'password1': self.my_user.password,
            'password2': self.my_user.password+"1"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn(UserFormTestData.errors['password_mismatch']['pt'],form.errors['password2'])

class SignUpFormTestEN(TestCase):
    '''
        testing for invalid forms in EN language
        yielded error messages ares compared
        to dictionary from UserFormTestData
    '''

    def setUp(self):
        super().setUp()
        self.my_user = User(
                username=UserFormTestData.my_user["username"],
                email=UserFormTestData.my_user["email"],
                password=UserFormTestData.my_user["password"]
                )
        translation.activate('en')

    def tearDown(self):
        super().tearDown()

    def test_sign_up_form_invalid_signIn(self):
        '''
            tests invalid Sign Up form with
            empty fields
        '''

        form = SignUpForm({
            'username': "",
            'email': "",
            'password1': "",
            'password2': ""
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn(UserFormTestData.errors['null_field']['en'],form.errors['username'])
        self.assertIn(UserFormTestData.errors['null_field']['en'],form.errors['email'])
        self.assertIn(UserFormTestData.errors['null_field']['en'],form.errors['password1'])
        self.assertIn(UserFormTestData.errors['null_field']['en'],form.errors['password2'])

    def test_sign_up_form_password_mismatch(self):
        '''
            tests invalid Signup were password1 field data
            does not match password2 field data
        '''

        form = SignUpForm({
            'username': self.my_user.username,
            'email': self.my_user.email,
            'password1': self.my_user.password,
            'password2': self.my_user.password+"1"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn(UserFormTestData.errors['password_mismatch']['en'],form.errors['password2'])

class LoginFormTest(TestCase):
    '''
        Base valid tests for Login form
        at url /accounts/login
    '''

    def setUp(self):
        super().setUp()
        self.my_user = User.objects.create(
                username=UserFormTestData.my_user["username"],
                email=UserFormTestData.my_user["email"],
                password=UserFormTestData.my_user["password"]
                )

    def tearDown(self):
        super().tearDown()

    def test_valid_data_input(self):
        '''
            tests Login form with valid data
        '''
        
        form = LoginForm({
            'username': self.my_user.username,
            'password': self.my_user.password
            },self.my_user
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.data['username'],self.my_user.username)
        self.assertEqual(form.data['password'], self.my_user.password)
    
    def test_correct_form_structure(self):
        pass
    

class LoginFormTestPT(TestCase):
    '''
        testing for invalid forms in PT language
        yielded error messages ares compared
        to dictionary from UserFormTestData
    '''
    def setUp(self):
        super().setUp()
        self.my_user = User.objects.create(
                username=UserFormTestData.my_user["username"],
                email=UserFormTestData.my_user["email"],
                password=UserFormTestData.my_user["password"]
                )
        translation.activate('pt')
    
    def tearDown(self):
        super().tearDown()

    def test_empty_data_input(self):
        '''
            tests invalid Sign Up form with
            empty fields
        '''
        
        form = LoginForm({
            'username': '',
            'password': ''
            },self.my_user
        )
        self.assertFalse(form.is_valid())
        self.assertIn(UserFormTestData.errors['null_field']['pt'],form.errors['username'])
        self.assertIn(UserFormTestData.errors['null_field']['pt'],form.errors['password'])

    def test_invalid_password_input(self):
        '''
            tests invalid Signup were password
            has invalid size
        '''
        
        form = LoginForm({
            'username': 'awd',
            'password': '123'
            },self.my_user
        )
        self.assertFalse(form.is_valid())
        self.assertIn(UserFormTestData.errors['password_size']['pt'],form.errors['password'][0])


class LoginFormTestEN(TestCase):
    '''
        testing for invalid forms in PT language
        yielded error messages ares compared
        to dictionary from UserFormTestData
    '''
    def setUp(self):
        super().setUp()
        self.my_user = User.objects.create(
                username=UserFormTestData.my_user["username"],
                email=UserFormTestData.my_user["email"],
                password=UserFormTestData.my_user["password"]
                )
        translation.activate('en')
    
    def tearDown(self):
        super().tearDown()
 
    def test_empty_data_input(self):
        '''
            tests invalid Sign Up form with
            empty fields
        '''
        
        form = LoginForm({
            'username': '',
            'password': ''
            },self.my_user
        )
        self.assertFalse(form.is_valid())
        self.assertIn(UserFormTestData.errors['null_field']['en'],form.errors['username'])
        self.assertIn(UserFormTestData.errors['null_field']['en'],form.errors['password'])

    def test_invalid_password_input(self):
        '''
            tests invalid Signup were password
            has invalid size
        '''
        
        form = LoginForm({
            'username': 'awd',
            'password': '123'
            },self.my_user
        )
        self.assertFalse(form.is_valid())
        self.assertIn(UserFormTestData.errors['password_size']['en'],form.errors['password'][0])

