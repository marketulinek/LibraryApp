from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.urls import reverse


class ILSViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testerka', 'terka.testerka@library.com', 'I.love.b00ks')

    def test_my_account_not_signed(self):
        response = self.client.get(reverse('my_account'), follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/my_account')