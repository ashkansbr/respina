import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ad_management.models import Ad, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestCommentViews:
    @pytest.fixture
    def user(self):
        return User.objects.create_user(email="testuser@example.com", password="password123")

    @pytest.fixture
    def ad(self, user):
        return Ad.objects.create(title="Sample Ad", description="Sample Description", owner=user)

    @pytest.fixture
    def auth_client(self, user):
        client = APIClient()
        url = reverse('token_obtain_pair')
        response = client.post(url, {"email": user.email, "password": "password123"}, format='json')
        assert response.status_code == status.HTTP_200_OK
        token = response.data['access']
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        return client

    def test_create_comment(self, auth_client, ad):
        url = reverse('comment-list-create', kwargs={'pk': ad.id})
        data = {"text": "This is a test comment."}
        response = auth_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['text'] == data['text']

    def test_prevent_multiple_comments(self, auth_client, ad, user):
        Comment.objects.create(ad=ad, user=user, text="First comment")
        url = reverse('comment-list-create', kwargs={'pk': ad.id})
        data = {"text": "Another comment"}
        response = auth_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_comments_for_ad(self, client, ad, user):
        Comment.objects.create(ad=ad, user=user, text="Sample Comment")
        url = reverse('comment-list-create', kwargs={'pk': ad.id})
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
