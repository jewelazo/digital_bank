from django.utils.translation import gettext_lazy as _


TRANSACTION_TYPE_LIST = (
    ('deposit', _('deposit')),
    ('withdrawals', _('withdrawals')),
)


TRANSACTION_TYPE_DICT = {
    "DEPOSIT":"deposit",
    "WITHDRAWALS":"withdrawals"
}
