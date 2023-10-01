from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from apps.account.models import User
from .models import BankAccount, Transaction

class BankAccountSerializer(serializers.Serializer):

    user_id = PrimaryKeyRelatedField(queryset=User.objects.all(),required=False)
    

class BankAccountModelSerializer(serializers.ModelSerializer):

    transactions = serializers.SerializerMethodField()

    def get_transactions(self,instance):

        transactions = instance.transactions.all().order_by("-created_at")
        return TransactionSerializer(transactions, many=True).data

    class Meta:
        model = BankAccount
        fields = ("id","account_number","balance","transactions",)


class TransactionModelSerializer(serializers.ModelSerializer):

    bank_account_number = serializers.SlugRelatedField(queryset=BankAccount.objects.all(),slug_field='account_number')

    class Meta:
        model = Transaction
        fields = ("amount", "transaction_type","bank_account_number",)


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = "__all__"