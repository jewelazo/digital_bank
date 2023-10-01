import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.account.models import User

payload = {
    "first_name": "test",
    "last_name": "test",
    "email": "test@mail.com",
    "username": "test@mail.com",
    "phone_number": "879464d512",
    "doc_type": "DNI",
    "doc_number": "78965412",
    "country": "CO",
    "password": "123456",
}


@pytest.fixture
def api_client_logged():
    user = User.objects.create(**payload)
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    return client
