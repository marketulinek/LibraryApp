from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User


class ILSViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testerka', 'terka.testerka@library.com', 'I.love.b00ks')