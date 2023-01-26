from rest_framework.test import APITestCase
from django.urls import reverse

class TestSetup(APITestCase):
    

    def setUp(self):
        self.register_url = reverse('register')
        self.user_data ={
            "email": "ngobidaniel04@gmail.com",
            "username": "email",
            "password": "ngobidaniel04@gmail.com",
        }
        return super().setUp()

    def tearDown(self):
        return super().tearDown()
    
