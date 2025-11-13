import pytest
from rest_framework import status
from decimal import Decimal

from tests.bank.conftest import (
    BANK_ACCOUNTS_URL,
    TRANSACTIONS_URL,
    INITIAL_DEPOSIT_AMOUNT,
    TEST_DEPOSIT_AMOUNT,
    TEST_WITHDRAWAL_AMOUNT,
    INVALID_ACCOUNT_NUMBER,
    create_transaction,
    get_account_balance,
)


@pytest.mark.django_db
class TestBankAccount:
    """Test suite for bank account operations."""

    def test_create_bank_account(self, api_client_logged):
        """Test that a bank account can be created successfully."""
        response = api_client_logged.post(BANK_ACCOUNTS_URL)
        data = response.data

        assert response.status_code == status.HTTP_201_CREATED
        assert "account_number" in data
        assert "balance" in data
        assert Decimal(data["balance"]) == Decimal("0.00")

    def test_get_all_accounts_from_logged_user(self, api_client_logged, bank_account):
        """Test that all bank accounts for logged user can be retrieved."""
        response = api_client_logged.get(BANK_ACCOUNTS_URL)
        response_json = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response_json, list)
        assert len(response_json) == 1
        assert "transactions" in response_json[0]
        assert response_json[0]["account_number"] == bank_account["account_number"]


@pytest.mark.django_db
class TestSameAccountTransactions:
    """Test suite for deposit and withdrawal operations on the same account."""

    def test_create_deposit_transaction(self, api_client_logged, bank_account):
        """Test that a deposit transaction can be created successfully."""
        response = create_transaction(
            api_client_logged,
            bank_account["account_number"],
            TEST_DEPOSIT_AMOUNT,
            "deposit",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["response"] == "Success Transaction"

        # Verify balance was updated
        balance = get_account_balance(api_client_logged, bank_account["account_number"])
        assert balance == Decimal(TEST_DEPOSIT_AMOUNT)

    def test_not_create_transaction_with_invalid_account_number(
        self, api_client_logged
    ):
        """Test that transaction with invalid account number is rejected."""
        response = create_transaction(
            api_client_logged, INVALID_ACCOUNT_NUMBER, TEST_DEPOSIT_AMOUNT, "deposit"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_not_create_withdrawal_from_insufficient_balance(
        self, api_client_logged, bank_account
    ):
        """Test that withdrawal with insufficient balance is rejected."""
        # Create initial deposit of 1000
        create_transaction(
            api_client_logged,
            bank_account["account_number"],
            TEST_DEPOSIT_AMOUNT,
            "deposit",
        )

        # Try to withdraw 2000 (more than available balance)
        response = create_transaction(
            api_client_logged,
            bank_account["account_number"],
            TEST_WITHDRAWAL_AMOUNT,
            "withdrawal",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["response"] == "Insufficient bank account balance"


@pytest.mark.django_db
class TestAccountTransfers:
    """Test suite for transfer operations between different accounts."""

    @pytest.mark.parametrize("transaction_type", ["deposit", "withdrawal"])
    def test_not_create_transfer_to_same_account(
        self, api_client_logged, bank_account_with_balance, transaction_type
    ):
        """Test that transfers to the same account are rejected."""
        response = create_transaction(
            api_client_logged,
            bank_account_with_balance["account_number"],
            TEST_WITHDRAWAL_AMOUNT,
            transaction_type,
            account_number_to=bank_account_with_balance["account_number"],
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_not_create_transfer_with_insufficient_balance(
        self, api_client_logged, two_bank_accounts
    ):
        """Test that transfer with insufficient balance is rejected."""
        account1, account2 = two_bank_accounts

        # Deposit only 1000 to account1
        create_transaction(
            api_client_logged,
            account1["account_number"],
            TEST_DEPOSIT_AMOUNT,
            "deposit",
        )

        # Try to transfer 5000 (more than available)
        response = create_transaction(
            api_client_logged,
            account1["account_number"],
            INITIAL_DEPOSIT_AMOUNT,
            "deposit",
            account_number_to=account2["account_number"],
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["response"] == "Insufficient bank account balance"

    def test_create_transfer_between_accounts(
        self, api_client_logged, two_bank_accounts
    ):
        """Test that a successful transfer between accounts works correctly."""
        account1, account2 = two_bank_accounts

        # Initial deposit to account1
        create_transaction(
            api_client_logged,
            account1["account_number"],
            INITIAL_DEPOSIT_AMOUNT,
            "deposit",
        )

        # Transfer 2000 from account1 to account2
        response = create_transaction(
            api_client_logged,
            account1["account_number"],
            TEST_WITHDRAWAL_AMOUNT,
            "deposit",
            account_number_to=account2["account_number"],
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["response"] == "Success Transaction"

        # Verify balances
        balance1 = get_account_balance(api_client_logged, account1["account_number"])
        balance2 = get_account_balance(api_client_logged, account2["account_number"])

        assert balance1 == Decimal(INITIAL_DEPOSIT_AMOUNT) - Decimal(
            TEST_WITHDRAWAL_AMOUNT
        )
        assert balance2 == Decimal(TEST_WITHDRAWAL_AMOUNT)


@pytest.mark.django_db
class TestListTransactions:
    def test_list_transactions(self, api_client_logged, bank_account_with_balance):
        """Test that transactions for a bank account can be listed."""
        response = api_client_logged.get(
            f"{BANK_ACCOUNTS_URL}{bank_account_with_balance['id']}/transactions/"
        )
        response_json = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response_json, list)
        # assert len(response_json) == 3  # Assuming 3 transactions were created in the fixture
