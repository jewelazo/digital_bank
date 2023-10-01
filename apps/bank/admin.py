from django.contrib import admin

from .models import BankAccount, Transaction

# Register your models here.


@admin.register(BankAccount)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "account_number", "balance"]
    search_fields = ["user__username", "user__first_name", "user__last_name"]


@admin.register(Transaction)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "account_number",
        "amount",
        "transaction_type",
    ]
    search_fields = [
        "bank_account__user__id",
        "bank_account__user__first_name",
        "bank_account__user__last_name",
    ]

    def account_number(self, instance):
        return instance.bank_account.account_number
