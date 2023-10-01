import pytest
from rest_framework import status

#------------------------------------------------------------------BankAccount tests------------------------------------------------------------

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

#-----------------------------------Transaction tests(desposit and withdrawal) from the same account-------------------------------------------

@pytest.mark.django_db
def test_create_transaction_from_user_accounts(api_client_logged):

    url = '/api/bank-accounts/'
    response = api_client_logged.post(url)
    response_data = response.data
    payload = {'bank_account_number': response_data["account_number"], 'amount': '1000', 'transaction_type': "deposit"}
    url = '/api/transactions/'
    response = api_client_logged.post(url,payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED
   

@pytest.mark.django_db
def test_not_create_transaction_from_any_account_number(api_client_logged):

    url = '/api/bank-accounts/'
    response = api_client_logged.post(url)
    payload = {'bank_account_number': "1458723658456544", 'amount': '1000', 'transaction_type': "deposit"}
    url = '/api/transactions/'
    response = api_client_logged.post(url,payload, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_not_create_transaction_from_insufficient_balance_account(api_client_logged):

    url = '/api/bank-accounts/'
    response = api_client_logged.post(url)
    response_data = response.data
    payload = {'bank_account_number': response_data["account_number"], 'amount': '1000', 'transaction_type': "deposit"}
    url = '/api/transactions/'
    response = api_client_logged.post(url,payload, format="json")
    payload = {'bank_account_number': response_data["account_number"], 'amount': '2000', 'transaction_type': "withdrawal"}
    response = api_client_logged.post(url,payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST

#------------------Transaction tests(desposit and withdrawal) between distinct accounts("bank_account_number_to" field in payload)-------------------------------------------

@pytest.mark.django_db
def test_not_create_deposit_transaction_between_same_account(api_client_logged):
    
    url1 = '/api/bank-accounts/'
    response = api_client_logged.post(url1)
    response_data = response.data
    payload = {'bank_account_number': response_data["account_number"], 'amount': '5000', 'transaction_type': "deposit"}
    url2 = '/api/transactions/'
    response = api_client_logged.post(url2,payload, format="json")
    payload = {'bank_account_number': response_data["account_number"],'bank_account_number_to': response_data["account_number"], 'amount': '2000', 'transaction_type': "deposit"}
    response = api_client_logged.post(url2,payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_not_create_withdrawal_transaction_between_same_account(api_client_logged):
    
    url1 = '/api/bank-accounts/'
    response = api_client_logged.post(url1)
    response_data = response.data
    payload = {'bank_account_number': response_data["account_number"], 'amount': '5000', 'transaction_type': "deposit"}
    url2 = '/api/transactions/'
    response = api_client_logged.post(url2,payload, format="json")
    payload = {'bank_account_number': response_data["account_number"],'bank_account_number_to': response_data["account_number"], 'amount': '2000', 'transaction_type': "withdrawal"}
    response = api_client_logged.post(url2,payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_not_create_deposit_transaction_between_distinct_accounts_from_insufficient_balance(api_client_logged):
    
    url1 = '/api/bank-accounts/'
    response1 = api_client_logged.post(url1)
    response2 = api_client_logged.post(url1)
    response_data1 = response1.data
    response_data2 = response2.data
    payload = {'bank_account_number': response_data1["account_number"], 'amount': '1000', 'transaction_type': "deposit"}
    url2 = '/api/transactions/'
    response = api_client_logged.post(url2,payload, format="json")
    payload = {'bank_account_number': response_data1["account_number"],'bank_account_number_to': response_data2["account_number"], 'amount': '5000', 'transaction_type': "deposit"}
    response = api_client_logged.post(url2,payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_create_deposit_transaction_between_distinct_accounts(api_client_logged):
    
    url1 = '/api/bank-accounts/'
    response1 = api_client_logged.post(url1)
    response2 = api_client_logged.post(url1)
    response_data1 = response1.data
    response_data2 = response2.data
    payload = {'bank_account_number': response_data1["account_number"], 'amount': '5000', 'transaction_type': "deposit"}
    url2 = '/api/transactions/'
    response = api_client_logged.post(url2,payload, format="json")
    payload = {'bank_account_number': response_data1["account_number"],'bank_account_number_to': response_data2["account_number"], 'amount': '2000', 'transaction_type': "deposit"}
    response = api_client_logged.post(url2,payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED
