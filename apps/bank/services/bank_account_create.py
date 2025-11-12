
from apps.bank.models import BankAccount
from apps.account.models import User
from ..utils import generate_bank_number


def bank_account_create(*, user: User, initial_balance=0.00) -> BankAccount:
    """Creates a bank account for the given user with an optional initial balance.

    Args:
        user (User): The user for whom the bank account is to be created.
        initial_balance (Decimal, optional): The initial balance for the bank account. Defaults to 0.00.
    Returns:
        BankAccount: The created bank account instance.
    """
    account_number = generate_bank_number()

    bank_account = BankAccount(
        user=user, account_number=account_number, balance=initial_balance
    )
    bank_account.full_clean()
    bank_account.save()
    return bank_account
