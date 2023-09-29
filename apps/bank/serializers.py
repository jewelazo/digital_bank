from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from apps.account.models import User
from .models import BankAccount

class BankAccountSerializer(serializers.Serializer):

    user_id = PrimaryKeyRelatedField(queryset=User.objects.all(),required=False)
    

class BankAccountModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankAccount
        fields = ("id","account_number","balance",)


