import pytest

from rest_framework import status

from apps.account.models import User

# Create your tests here.

@pytest.mark.django_db
def test_create_user(api_client, create_user_payload):
    url = '/api/register/'
    response = api_client.post(url, create_user_payload, format='json')
    data = response.data
    assert response.status_code == status.HTTP_201_CREATED
    assert data["user"]["username"] == create_user_payload["username"]
    assert data["user"]["email"] == create_user_payload["email"]
    assert data["user"]["phone_number"] == create_user_payload["phone_number"]
    assert data["user"]["country"] == create_user_payload["country"]
    assert User.objects.all().count() == 1