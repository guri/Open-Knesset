"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from models import *

now = datetime.datetime.now()

class SimpleTest(TestCase):
    fixtures = ['links']
    def setUp (self):
        self.comite = Comite.objects.create(name='comite')
        self.u1 = User.objects.create(username='abe')

    def test_creation(self):
        """
        Tests the creation of all the models
        """
        self.assertTrue(self.comite.concepts.create(title='Hello World', creator=self.u1))
        self.assertTrue(self.comite.links.create(url='http://example.com'))
        self.assertTrue(self.comite.events.create(when=now, what='sunrise'))

    def tearDown(self):
        self.comite.delete()
