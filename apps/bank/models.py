from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator,MinValueValidator

from apps.account.models import User

# Create your models here.
class BankAccount(models.Model):
    account_number = models.CharField(verbose_name=_('account_number'), max_length=16, validators=[MinLengthValidator(16)])
    balance = models.DecimalField(verbose_name=_('balance'), decimal_places=2, max_digits=8, default=0.00, 
                                    validators=[MinValueValidator(0.00)] )
    user = models.ForeignKey(User, verbose_name=_('user'), on_delete=models.PROTECT, related_name="accounts")
    created_at = models.DateTimeField(verbose_name=_('created_at'), auto_now_add=True)
    