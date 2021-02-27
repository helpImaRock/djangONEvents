from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from apps.accounts.models import User


class UserModelTest(TestCase):

    def setUp(self):

        self.uniq_valid_user = User(
            username="user1",
            email="email@e1.com",
            password="adawdawdawd"
        )

        self.dup_valid_username = User(
            username="user1",
            email="email@e2.com",
            password="adawdawdawd"
        )

        self.dup_valid_email = User(
            username="user2",
            email="email@e1.com",
            password="adawdawdawd"
        )

        self.dup_invalid_password = User(
            username="some tin",
            email="email@email.com",
            password="wadg3g" ## below minimum size
        )
    
    def test_unique_username_email_save(self):
        '''
            tests user regular using insertion saving
        '''
        
        user = self.uniq_valid_user 
        self.assertEquals(str(user),"username:user1, email: email@e1.com")
        user.save()
        query = User.objects.filter(username=user.username)
        self.assertIn(user,query)
        self.assertEqual(len(query),1)
        user = query[0]

        ## default db user table attributes
        self.assertTrue(user.is_active == 1)
        self.assertTrue(user.is_anon == 0)
        self.assertTrue(user.is_admin == 0)
        self.assertTrue(user.is_staff == 0)
        self.assertTrue(user.is_superuser == 0)

    def test_duplicate_username_entry(self):
        '''
            tests inserting user 
            with already db existing username
        '''

        user1 = self.uniq_valid_user
        user2 = self.dup_valid_username

        user1.save()
        with self.assertRaises(IntegrityError):
            user2.save()

    def test_duplicate_email_entry(self):
        '''
            tests inserting user 
            with already db existing email
        '''

        user1 = self.uniq_valid_user
        user2 = self.dup_valid_email

        user1.save()
        with self.assertRaises(IntegrityError):
            user2.save()
    
    def tearDown(self):
        
        self.uniq_valid_user = None
        self.dup_valid_username = None
        self.dup_valid_email = None
        self.dup_invalid_password = None

"""     def test_password_too_small(self):
        '''
            tests db insertion small password
        '''

        user1 = self.dup_invalid_password
        with self.assertRaises(ValidationError):
            user1.save()
 """
