from django.contrib import admin

from .models import User

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "full_name", "username"]
    search_fields = ["first_name", "last_name", "email"]
