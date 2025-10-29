import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from decimal import Decimal

from apps.account.models import User

# Test constants
BANK_ACCOUNTS_URL = "/api/bank-accounts/"
TRANSACTIONS_URL = "/api/transactions/"
INITIAL_DEPOSIT_AMOUNT = "5000"
TEST_DEPOSIT_AMOUNT = "1000"
TEST_WITHDRAWAL_AMOUNT = "2000"
INVALID_ACCOUNT_NUMBER = "1458723658456544"

# User payload for tests
USER_PAYLOAD = {
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


# Helper functions
def create_transaction(api_client, account_number, amount, transaction_type, account_number_to=None):
    """Helper function to create a transaction.

    Args:
        api_client: Authenticated API client
        account_number: Source account number
        amount: Transaction amount as string or number
        transaction_type: "deposit" or "withdrawal"
        account_number_to: Destination account number (optional, for transfers)

    Returns:
        Response object from the POST request
    """
    payload = {
        "bank_account_number": account_number,
        "amount": str(amount),
        "transaction_type": transaction_type,
    }
    if account_number_to:
        payload["bank_account_number_to"] = account_number_to

    return api_client.post(TRANSACTIONS_URL, payload, format="json")


def get_account_balance(api_client, account_number):
    """Helper function to get the current balance of an account.

    Args:
        api_client: Authenticated API client
        account_number: Account number to query

    Returns:
        Decimal: Current account balance
    """
    response = api_client.get(BANK_ACCOUNTS_URL)
    for account in response.data:
        if account["account_number"] == account_number:
            return Decimal(account["balance"])
    return None


# Fixtures
@pytest.fixture
def api_client_logged():
    """Creates an authenticated API client with a test user."""
    user = User.objects.create(**USER_PAYLOAD)
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client


@pytest.fixture
def bank_account(api_client_logged):
    """Creates a bank account for the logged-in user.

    Returns:
        dict: Bank account data from the API response
    """
    response = api_client_logged.post(BANK_ACCOUNTS_URL)
    return response.data


@pytest.fixture
def two_bank_accounts(api_client_logged):
    """Creates two bank accounts for the logged-in user.

    Returns:
        tuple: Two bank account data dictionaries
    """
    account1 = api_client_logged.post(BANK_ACCOUNTS_URL).data
    account2 = api_client_logged.post(BANK_ACCOUNTS_URL).data
    return account1, account2


@pytest.fixture
def bank_account_with_balance(api_client_logged, bank_account):
    """Creates a bank account with an initial deposit.

    Returns:
        dict: Bank account data with initial balance of 5000
    """
    create_transaction(
        api_client_logged,
        bank_account["account_number"],
        INITIAL_DEPOSIT_AMOUNT,
        "deposit"
    )
    return bank_account
