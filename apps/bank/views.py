from rest_framework import generics, permissions, status
from rest_framework.response import Response

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

    def post(self,request):

        transaction_serializer = TransactionModelSerializer(data=request.data)

        if transaction_serializer.is_valid():
    
            bank_account = transaction_serializer.validated_data["back_account_number"]
            transaction_type = transaction_serializer.validated_data["transaction_type"]
            amount = transaction_serializer.validated_data["amount"]

            if bank_account not in request.user.accounts.all():
                return Response({"response":"Only deposits and withdrawals from your accounts"}, status=status.HTTP_400_BAD_REQUEST)
            
    
            if transaction_type == TRANSACTION_TYPE_DICT["DEPOSIT"]:
                Transaction.objects.create(bank_account=bank_account, amount=amount, transaction_type=transaction_type)
                bank_account.balance += amount
                bank_account.save()
                
                return Response({"response":"Success Transaction"}, status=status.HTTP_201_CREATED)
            
            elif transaction_type == TRANSACTION_TYPE_DICT["WITHDRAWALS"]:
                if amount <= bank_account.balance:
                    Transaction.objects.create(bank_account=bank_account, amount=amount, transaction_type=transaction_type)
                    bank_account.balance -= amount
                    bank_account.save()

                    return Response({"response":"Success Transaction"}, status=status.HTTP_201_CREATED)
                
                return Response({"response":"Insufficient bank account balance"}, status=status.HTTP_400_BAD_REQUEST)
                
        
        return Response(transaction_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


