import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ad_management.models import Ad
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestAdViews:
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

    def test_create_ad(self, auth_client):
        url = reverse('ad-list-create')
        data = {"title": "Test Ad", "description": "This is a test ad description."}
        response = auth_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == data['title']

    def test_update_ad(self, auth_client, user):
        ad = Ad.objects.create(title="Ad to Edit", description="Edit description", owner=user)
        url = reverse('ad-detail', kwargs={'pk': ad.id})
        data = {"title": "Updated Title"}
        response = auth_client.put(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == data['title']

    def test_delete_ad(self, auth_client, user):
        ad = Ad.objects.create(title="Ad to Delete", description="Delete description", owner=user)
        url = reverse('ad-detail', kwargs={'pk': ad.id})
        response = auth_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
