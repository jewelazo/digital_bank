from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from django.utils.translation import gettext_lazy as _

from apps.account.models import User
from .models import BankAccount, Transaction
from .constants import TRANSACTION_TYPE_DICT


class TransactionModelSerializer(serializers.ModelSerializer):
    bank_account_number = serializers.SlugRelatedField(
        queryset=BankAccount.objects.all(),
        slug_field="account_number",
        label=_("Bank account number"),
        help_text=_("Bank account number"),
    )
    # Optional field in payload, only to transactions between distinct accounts, default=None
    bank_account_number_to = serializers.SlugRelatedField(
        queryset=BankAccount.objects.all(),
        slug_field="account_number",
        allow_null=True,
        required=False,
        default=None,
        label=_("Bank account number to"),
        help_text=_("Bank account number to x-nullable: true"),
    )

    def validate(self, data):
        # Validate if bank_account_number and bank_account_number_to fields come in payload
        if data["bank_account_number"] and data["bank_account_number_to"]:
            # Validate transaction_type with "withdrawal" as value come in payload to raise exception
            first_condition = (
                data["transaction_type"] == TRANSACTION_TYPE_DICT["WITHDRAWAL"]
            )
            # Validate if bank_account_number and bank_account_number are the same to raise exception
            second_condition = (
                data["bank_account_number"].account_number
                == data["bank_account_number_to"].account_number
            )
            if first_condition or second_condition:
                raise serializers.ValidationError(
                    "Only deposits between distinct accounts"
                )
        return data

    class Meta:
        model = Transaction
        fields = (
            "amount",
            "transaction_type",
            "bank_account_number",
            "bank_account_number_to",
        )


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
