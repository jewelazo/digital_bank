from django.urls import path

from .views import BankAccountApiView, TransactionsApiView, TransactionListApiView

urlpatterns = [
    path("bank-accounts/", BankAccountApiView.as_view()),
    path("transactions/", TransactionsApiView.as_view()),
    path("bank-accounts/<int:id>/transactions/", TransactionListApiView.as_view()),
]
