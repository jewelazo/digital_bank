from django.urls import path

from .views import BankAccountApiView

urlpatterns = [
    path('bank-accounts/', BankAccountApiView.as_view()),
]