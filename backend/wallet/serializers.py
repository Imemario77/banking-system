from rest_framework.serializers import ModelSerializer
from wallet.models import UserWallet, Transaction

class WalletSerializer(ModelSerializer):
    class Meta:
        model = UserWallet
        fields = ["user","balance"]

class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = ("owner","amount", "transaction_type")

class ApproveTransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__" #("approved")
