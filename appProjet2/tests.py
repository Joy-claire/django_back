from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class ProjectAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_create_project(self):
        url = reverse('project-list')
        data = {
            'title': 'Projet Test',
            'description': 'Description du projet',
            'manager': self.user.id,
            'start_date': '2025-02-01',
            'end_date': '2025-03-01',
            'status': 'en_cours'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
