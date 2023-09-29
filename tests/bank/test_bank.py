import pytest
from  rest_framework.test import APIClient
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
    assert "transactions" in response_json[0]
    
@pytest.mark.django_db
def test_create_transaction_from_user_accounts(api_client_logged):
    api_client = api_client_logged
    url = '/api/bank-accounts/'
    response = api_client.post(url)
    response_data = response.data
    payload = {'back_account_number': response_data["account_number"], 'amount': '1000', 'transaction_type': "deposit"}
    url = '/api/transactions/'
    response = api_client.post(url,payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED
   

@pytest.mark.django_db
def test_not_create_transaction_from_any_account_number(api_client_logged):
    api_client = api_client_logged
    url = '/api/bank-accounts/'
    response = api_client.post(url)
    payload = {'back_account_number': "1458723658456544", 'amount': '1000', 'transaction_type': "deposit"}
    url = '/api/transactions/'
    response = api_client.post(url,payload, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_not_create_transaction_from_insufficient_balance_account(api_client_logged):
    api_client = api_client_logged
    url = '/api/bank-accounts/'
    response = api_client.post(url)
    response_data = response.data
    payload = {'back_account_number': response_data["account_number"], 'amount': '1000', 'transaction_type': "deposit"}
    url = '/api/transactions/'
    payload = {'back_account_number': response_data["account_number"], 'amount': '2000', 'transaction_type': "withdrawals"}
    response = api_client.post(url,payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST