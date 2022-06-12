from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.urls import reverse


class ILSViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testerka', email='terka.testerka@library.com', password='I.love.b00ks')

        self.new_user = {'username':'testerka',
                                                 "email":'terka.testerka@library.com',
                                                 "password1":'I.love.b00ks',
                                                 "password2":'I.love.b00ks',
                                                 "first_name":'terka',
                                                 "last_name":'testerka'}
        self.register_url=reverse('register')


    def test_get_registration_form(self):
        self.client.login(username='testerka', password='I.love.b00ks')
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'registration/register.html')

    def test_user_can_register(self):
        response = self.client.post(self.register_url, self.new_user, format="text/html")
        self.assertEqual(response.status_code, 302)


    def test_get_book_create(self):
        self.client.login(username='testerka', password='I.love.b00ks')
        response = self.client.get(reverse('book_form'))
        self.assertEqual(response.status_code, 200)
