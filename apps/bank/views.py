from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import BankAccountSerializer, BankAccountModelSerializer
from .models import BankAccount
from .utils import generate_bank_number


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
