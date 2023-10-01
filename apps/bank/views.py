from rest_framework import generics, status
from rest_framework.response import Response
from django.db.models import F

from .serializers import BankAccountSerializer, BankAccountModelSerializer, TransactionModelSerializer
from .models import BankAccount, Transaction
from .utils import generate_bank_number
from .constants import TRANSACTION_TYPE_DICT

# Create your views here.

class BankAccountApiView(generics.GenericAPIView):

    def get(self,request):
        accounts = request.user.accounts
        accounts_serializer = BankAccountModelSerializer(accounts, many=True)
        
        return Response(accounts_serializer.data, status=status.HTTP_200_OK)

    def post(self,request):

        bank_account_serializer = BankAccountSerializer(data=request.data)

        if bank_account_serializer.is_valid():

            user = request.user
            account_number = generate_bank_number()

            bank_account = BankAccount.objects.create(user=user, account_number=account_number)
            bank_account_serializer = BankAccountModelSerializer(bank_account)
            return Response(bank_account_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(bank_account_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
class TransactionsApiView(generics.GenericAPIView):
    serializer_class = TransactionModelSerializer

    def post(self,request):

        transaction_serializer = TransactionModelSerializer(data=request.data)

        if transaction_serializer.is_valid():
           
            bank_account = transaction_serializer.validated_data["bank_account_number"]
            bank_account_to = transaction_serializer.validated_data["bank_account_number_to"]
            transaction_type = transaction_serializer.validated_data["transaction_type"]
            amount = transaction_serializer.validated_data["amount"]

            # Validate only transactions from logged user accounts"
            if bank_account not in request.user.accounts.all():
                return Response({"response":"Only deposits and withdrawals from your accounts"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Validate only transactions from the same logged user(deposit-withdrawal),field "bank_account_number_to" not in payload or its value is None
            if not bank_account_to:
                
                if transaction_type == TRANSACTION_TYPE_DICT["DEPOSIT"]:
                    Transaction.objects.create(bank_account=bank_account, amount=amount, transaction_type=transaction_type)
                    bank_account.balance += amount
                    bank_account.save()
                    
                    return Response({"response":"Success Transaction"}, status=status.HTTP_201_CREATED)
                
                elif transaction_type == TRANSACTION_TYPE_DICT["WITHDRAWAL"]:
                    # Validate if bank account has sufficient balance to the withdrawal transaction in the same account
                    if amount <= bank_account.balance:
                        Transaction.objects.create(bank_account=bank_account, amount=amount, transaction_type=transaction_type)
                        bank_account.balance -= amount
                        bank_account.save()

                        return Response({"response":"Success Transaction"}, status=status.HTTP_201_CREATED)
                    
                    return Response({"response":"Insufficient bank account balance"}, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                
                if transaction_type == TRANSACTION_TYPE_DICT["DEPOSIT"]:
                    
                    bank_account = BankAccount.objects.filter(account_number=bank_account.account_number)
                    bank_account_to = BankAccount.objects.filter(account_number=bank_account_to.account_number)
                    
                    # Validate if bank account has sufficient balance to withdrawal transaction between distinct accounts
                    if bank_account.first().balance >= amount:
                        bank_account.update(balance=F("balance") - amount)
                        bank_account_to.update(balance=F("balance") + amount)
                        Transaction.objects.create(bank_account=bank_account.first(),bank_account_to=bank_account_to.first(), amount=amount, transaction_type=transaction_type)
                        return Response({"response":"Success Transaction"}, status=status.HTTP_201_CREATED)
                    
                    return Response({"response":"Insufficient bank account balance"}, status=status.HTTP_400_BAD_REQUEST)
                
        
        return Response(transaction_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


