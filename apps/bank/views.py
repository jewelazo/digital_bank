from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from drf_yasg.utils import swagger_auto_schema

from .serializers import (
    TransactionModelSerializer,
    TransactionSerializer,
)
from .models import BankAccount, Transaction
from .services.bank_account_create import bank_account_create
from .services.transaction_create import transaction_create
from .filters import TransactionFilter
from django_filters.rest_framework import DjangoFilterBackend


class BankAccountApiView(generics.GenericAPIView):
    class InputSerializer(serializers.Serializer):
        initial_balance = serializers.DecimalField(
            max_digits=12,
            decimal_places=2,
            required=False,
            default=0.00,
            min_value=0.00,
            help_text="Initial balance for the bank account",
        )

    class OutputSerializer(serializers.ModelSerializer):
        transactions = serializers.SerializerMethodField()

        def get_transactions(self, instance):
            transactions_from = instance.transactions.all()
            transactions_to = instance.transactions_to.all()
            transactions = (transactions_from | transactions_to).order_by("-created_at")
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
        request_body=InputSerializer, responses={201: OutputSerializer()}
    )
    def post(self, request):
        bank_account_serializer = self.InputSerializer(data=request.data)
        bank_account_serializer.is_valid(raise_exception=True)
        bank_account = bank_account_create(
            user=request.user,
            initial_balance=bank_account_serializer.validated_data["initial_balance"],
        )

        bank_account_serializer = self.OutputSerializer(bank_account)
        return Response(bank_account_serializer.data, status=status.HTTP_201_CREATED)


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


class TransactionListApiView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = TransactionFilter
    ordering_fields = ["created_at", "amount"]
    ordering = ["-created_at"]

    def get_queryset(self):
        bank_account_id = self.kwargs.get("id")

        # Validate bank account exists and belongs to user
        bank_account = BankAccount.objects.filter(id=bank_account_id).first()
        if not bank_account:
            raise serializers.ValidationError({"error": "Bank account not found"})

        if not self.request.user.accounts.filter(id=bank_account.id).exists():
            raise serializers.ValidationError(
                {"error": "You don't have permission to access this bank account"}
            )

        # Return transactions for this bank account (both outgoing and incoming)
        return Transaction.objects.filter(
            bank_account=bank_account
        ) | Transaction.objects.filter(bank_account_to=bank_account)
