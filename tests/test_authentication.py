import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestAuthentication:
    @pytest.fixture
    def user(self):
        return User.objects.create_user(email="testuser@example.com", password="password123")

    @pytest.fixture
    def auth_client(self, user):
        client = APIClient()
        url = reverse('token_obtain_pair')
        response = client.post(url, {"email": user.email, "password": "password123"}, format='json')
        assert response.status_code == status.HTTP_200_OK

        token = response.data['access']
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        return client

    def test_login_jwt_token(self, client, user):
        client = APIClient()
        url = reverse('token_obtain_pair')
        data = {"email": "testuser@example.com", "password": "password123"}
        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_access_protected_view(self, auth_client):
        url = reverse('ad-list-create')
        data = {"title": "Test Ad", "description": "Test Description"}
        response = auth_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
