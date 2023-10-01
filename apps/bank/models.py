from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator,MinValueValidator

from apps.account.models import User
from .constants import TRANSACTION_TYPE_LIST

# Create your models here.
class BankAccount(models.Model):
    account_number = models.CharField(verbose_name=_('account_number'), max_length=16, validators=[MinLengthValidator(16)])
    balance = models.DecimalField(verbose_name=_('balance'), decimal_places=2, max_digits=10, default=0.00, 
                                    validators=[MinValueValidator(0.00)] )
    user = models.ForeignKey(User, verbose_name=_('user'), on_delete=models.PROTECT, related_name="accounts")
    created_at = models.DateTimeField(verbose_name=_('created_at'), auto_now_add=True)
    
class Transaction(models.Model):
    bank_account = models.ForeignKey(BankAccount, verbose_name=_('bank_account'),on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(verbose_name=_('amount'), decimal_places=2, max_digits=8, validators=[MinValueValidator(0.01)] )
    transaction_type = models.CharField(verbose_name=_('transaction_type'), choices=TRANSACTION_TYPE_LIST, max_length=20)
    created_at = models.DateTimeField(verbose_name=_('created_at'), auto_now_add=True)
