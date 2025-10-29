from django.urls import path

from .views import BankAccountApiView, TransactionsApiView, TransactionListApiView

urlpatterns = [
    path("bank-accounts/", BankAccountApiView.as_view()),
    path("transactions/", TransactionsApiView.as_view()),
    path("transactions/<int:id>/", TransactionListApiView.as_view()),
]
