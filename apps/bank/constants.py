from django.utils.translation import gettext_lazy as _


TRANSACTION_TYPE_LIST = (
    ("deposit", _("deposit")),
    ("withdrawal", _("withdrawal")),
)


TRANSACTION_TYPE_DICT = {"DEPOSIT": "deposit", "WITHDRAWAL": "withdrawal"}
