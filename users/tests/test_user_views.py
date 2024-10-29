import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestUserViews:

    def test_user_registration(self, client):
        url = reverse('user-register')
        data = {"email": "newuser@example.com", "password": "newpassword123", 'confirm_password': 'newpassword123'}
        response = client.post(url, data, format='json')
        print(response.data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['email'] == data['email']

    def test_duplicate_email_registration(self, client):
        User.objects.create_user(email="testuser@example.com", password="password123")
        url = reverse('user-register')
        data = {"email": "testuser@example.com", "password": "password123"}
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
