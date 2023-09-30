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

@pytest.mark.django_db
def test_jwt_token_with_correct_credentials(api_client,create_user_payload):
    
    url = '/api/register/'
    response = api_client.post(url, create_user_payload, format='json')
    response = response.data
    username = response["user"]["username"]

    url = '/api/token/'
    response = api_client.post(url,{"username": username, "password": "123456"}, format="json")
    data = response.data

    assert response.status_code == status.HTTP_200_OK
    assert "access" in data
    assert "refresh" in data

@pytest.mark.django_db
def test_logout_user_with_jwt_token(api_client_with_token):
    url = '/api/logout/'
    response = api_client_with_token.post(url)

    assert response.status_code == status.HTTP_200_OK