from django.urls import path
from wallet.views import CreateWallet, CreateTransaction, ApproveTransaction, ViewWalletAndTransactions


urlpatterns = [
    path('', ViewWalletAndTransactions.as_view()),
    path('create', CreateWallet.as_view()),
    path('transaction/create', CreateTransaction.as_view()),
    path('transaction/update/<int:pk>/', ApproveTransaction.as_view()),
]