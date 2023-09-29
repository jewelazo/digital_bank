from django.contrib import admin

from .models import BankAccount
# Register your models here.

@admin.register(BankAccount)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "account_number", "balance"]
    search_fields = ["user__username","user__first_name","user__last_name"]
