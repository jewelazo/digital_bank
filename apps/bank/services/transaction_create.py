from django.db import transaction
from ..models import Transaction, BankAccount
from ..constants import TRANSACTION_TYPE_DICT


@transaction.atomic
def transaction_create(
    *, user, bank_account, amount, transaction_type, bank_account_to=None
) -> Transaction:
    """Creates a transaction for the given bank account with optional transfer to another account.

    Args:
        bank_account (BankAccount): The bank account from which the transaction is initiated.
        amount (Decimal): The amount involved in the transaction.
        transaction_type (str): The type of transaction (e.g., "deposit", "withdrawal").
        bank_account_to (BankAccount, optional): The target bank account for transfers. Defaults to None.

    Returns:
        Transaction: The created transaction instance.
    """
    if not user.accounts.filter(id=bank_account.id).exists():
        raise ValueError(
            {"response": "Only deposits and withdrawals from your accounts"}
        )
    bank_account = BankAccount.objects.select_for_update().get(id=bank_account.id)
    if not bank_account_to:
        if transaction_type == TRANSACTION_TYPE_DICT["DEPOSIT"]:
            transaction_obj = Transaction.objects.create(
                bank_account=bank_account,
                amount=amount,
                transaction_type=transaction_type,
            )
            bank_account.balance += amount
            bank_account.save()

        elif transaction_type == TRANSACTION_TYPE_DICT["WITHDRAWAL"]:
            # Validate if bank account has sufficient balance to the withdrawal transaction in the same account
            if amount <= bank_account.balance:
                transaction_obj = Transaction.objects.create(
                    bank_account=bank_account,
                    amount=amount,
                    transaction_type=transaction_type,
                )
                bank_account.balance -= amount
                bank_account.save()
            else:
                raise ValueError(
                    {"response": "Insufficient bank account balance"},
                )
    else:
        bank_account_to = BankAccount.objects.select_for_update().get(
            id=bank_account_to.id
        )
        if transaction_type == TRANSACTION_TYPE_DICT["DEPOSIT"]:
            # Validate if bank account has sufficient balance to withdrawal transaction between distinct accounts
            if bank_account.balance >= amount:
                transaction_obj = Transaction.objects.create(
                    bank_account=bank_account,
                    bank_account_to=bank_account_to,
                    amount=amount,
                    transaction_type=transaction_type,
                )

                bank_account.balance -= amount
                bank_account.save()
                bank_account_to.balance += amount
                bank_account_to.save()

            else:
                raise ValueError(
                    {"response": "Insufficient bank account balance"},
                )
    return transaction_obj
