from rest_framework import generics, status, serializers
from rest_framework.response import Response
from django.db.models import F
from drf_yasg.utils import swagger_auto_schema

from .serializers import (
    TransactionModelSerializer,
    TransactionSerializer,
)
from .models import BankAccount, Transaction
from .utils import generate_bank_number
from .constants import TRANSACTION_TYPE_DICT
from .swagger_schemas import (
    transaction_list_params,
    transaction_list_responses,
    transaction_list_description,
)
from .services.bank_account_create import bank_account_create
from .services.transaction_create import transaction_create


class BankAccountApiView(generics.GenericAPIView):
    class InputSerializer(serializers.Serializer):
        initial_balance = serializers.DecimalField(
            max_digits=12, decimal_places=2, required=False, default=0.00, min_value=0.00, help_text="Initial balance for the bank account",
        )

    class OutputSerializer(serializers.ModelSerializer):
        transactions = serializers.SerializerMethodField()

        def get_transactions(self, instance):
            transactions_from = instance.transactions.all()
            transactions_to = instance.transactions_to.all()
            transactions = (
                (transactions_from | transactions_to).order_by(
                    "-created_at").distinct()
            )
            return TransactionSerializer(transactions, many=True).data

        class Meta:
            model = BankAccount
            fields = (
                "id",
                "account_number",
                "balance",
                "transactions",
            )

    def get(self, request):
        accounts = request.user.accounts
        accounts_serializer = self.OutputSerializer(accounts, many=True)

        return Response(accounts_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=InputSerializer,
        responses={201: OutputSerializer()}
    )
    def post(self, request):
        bank_account_serializer = self.InputSerializer(data=request.data)
        bank_account_serializer.is_valid(raise_exception=True)
        bank_account = bank_account_create(
            user=request.user, initial_balance=bank_account_serializer.validated_data["initial_balance"])

        bank_account_serializer = self.OutputSerializer(bank_account)
        return Response(
            bank_account_serializer.data, status=status.HTTP_201_CREATED
        )


class TransactionsApiView(generics.GenericAPIView):
    serializer_class = TransactionModelSerializer

    def post(self, request):
        transaction_serializer = self.serializer_class(data=request.data)
        transaction_serializer.is_valid(raise_exception=True)

        bank_account = transaction_serializer.validated_data["bank_account_number"]
        bank_account_to = transaction_serializer.validated_data[
            "bank_account_number_to"
        ]
        transaction_type = transaction_serializer.validated_data["transaction_type"]
        amount = transaction_serializer.validated_data["amount"]
        try:
            transaction_create(
                user=request.user,
                bank_account=bank_account,
                amount=amount,
                transaction_type=transaction_type,
                bank_account_to=bank_account_to,
            )
        except ValueError as e:
            return Response(e.args[0], status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"response": "Success Transaction"}, status=status.HTTP_201_CREATED
        )


class TransactionListApiView(generics.GenericAPIView):
    @swagger_auto_schema(
        operation_description=transaction_list_description,
        manual_parameters=transaction_list_params,
        responses=transaction_list_responses,
    )
    def get(self, request, id=None):
        bank_account = BankAccount.objects.filter(id=id).first()
        if not bank_account or (
            bank_account and bank_account not in request.user.accounts.all()
        ):
            return Response(
                {"Error": "Should send a valid bank account and must be yours"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Convert string query params to boolean
        deposit = request.query_params.get("deposit", "true").lower() == "true"
        withdrawal = request.query_params.get(
            "withdrawal", "true").lower() == "true"

        transactions = bank_account.transactions.all()

        if deposit and not withdrawal:
            transactions = transactions.filter(
                transaction_type=TRANSACTION_TYPE_DICT["DEPOSIT"]
            )
        elif withdrawal and not deposit:
            transactions = transactions.filter(
                transaction_type=TRANSACTION_TYPE_DICT["WITHDRAWAL"]
            )

        transactions_serializer = TransactionSerializer(
            transactions, many=True)

        return Response(transactions_serializer.data, status=status.HTTP_200_OK)
