import pytest
from rest_framework import status

@pytest.mark.django_db
def test_create_bank_account(api_client_logged):
    api_client = api_client_logged
    url = '/api/bank-accounts/'
    response = api_client.post(url)
    data = response.data
    
    assert response.status_code == status.HTTP_201_CREATED
    assert "account_number" in data
    assert "balance" in data


@pytest.mark.django_db
def test_get_all_accounts_from_logged_user(api_client_logged):
    api_client = api_client_logged
    url = '/api/bank-accounts/'
    response = api_client.post(url)
    response = api_client.get(url)
    response_json = response.json()
    
    assert response.status_code == status.HTTP_200_OK
    assert type(response_json) == type([])
    assert len(response_json) == 1
