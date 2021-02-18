import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class MyFunctionalTestClass(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def testPageAccess(self):
        self.browser.get('http://127.0.0.1:8000')
        self.fail('Finish the test!')
