from django.urls import path

from .views import BankAccountApiView, TransactionsApiView

urlpatterns = [
    path('bank-accounts/', BankAccountApiView.as_view()),
    path('transactions/', TransactionsApiView.as_view()),
]