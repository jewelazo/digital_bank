import django_filters
from .models import Transaction
from .constants import TRANSACTION_TYPE_LIST


class TransactionFilter(django_filters.FilterSet):
    transaction_type = django_filters.ChoiceFilter(
        field_name="transaction_type",
        choices=TRANSACTION_TYPE_LIST,
    )
    date_from = django_filters.DateFilter(field_name="created_at", lookup_expr="gte")
    date_to = django_filters.DateFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Transaction
        fields = []  # Empty because filters are explicitly defined above
