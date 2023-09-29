import pytest
from rest_framework.test import APIClient

payload = {
    "first_name":"test1",
    "last_name":"test1",
    "email":"test1@mai.com",
    "username":"test1@mail.com",
    "phone_number":"879464d512",
    "doc_type":"DNI",
    "doc_number":"78965412",
    "country":"PE",
    "password":"123456"
}

@pytest.fixture
def api_client():
    client = APIClient()
    return client

@pytest.fixture
def create_user_payload():
    return payload