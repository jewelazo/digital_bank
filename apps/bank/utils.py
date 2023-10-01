import random
import string
from .models import BankAccount


def generate_bank_number():
    while True:
        bank_number = "".join(random.choices(string.digits, k=16))
        accounts = BankAccount.objects.filter(account_number=bank_number)

        if not accounts.exists():
            break

    return bank_number
