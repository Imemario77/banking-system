from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND
from wallet.custom_exception import CustomValidationException
from wallet.models import TransactionType
from users.models import UserType
from wallet.serializers import WalletSerializer, TransactionSerializer, ApproveTransactionSerializer
from rest_framework.permissions import IsAuthenticated
from wallet.models import Transaction, UserWallet


class CreateWallet(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        if "balance" not in request.data or "user" not in request.data:
            return Response({"msg":"invalid data"}, status=HTTP_400_BAD_REQUEST)
        user = request.user

        print(user.user_type)

        if user.user_type not in [UserType.ADMIN.value, UserType.BANK_STAFF.value ]:
            return Response({"msg":"Only bank staff or admin can create accounts"}, status=HTTP_400_BAD_REQUEST)
        

        serializer = WalletSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(created_by=user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class CreateTransaction(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        if "amount" not in request.data or "owner" not in request.data or "transaction_type" not in request.data:
            return Response({"msg":"invalid data"}, status=HTTP_400_BAD_REQUEST)
        user = request.user

        serializer = TransactionSerializer(data=request.data)

        if request.data.get("amount") < 10 and  request.data.get("transaction_type") == TransactionType.Deposit.value:
            return Response({"msg":"You can't deposit lower than 10"}, status=HTTP_400_BAD_REQUEST)

        if request.data.get("amount") < 100 and  request.data.get("transaction_type") == TransactionType.Withdraw.value:
            return Response({"msg":"You can't withdraw lower than 100"}, status=HTTP_400_BAD_REQUEST)

        if request.data.get("amount") > 10000 and  request.data.get("transaction_type") == TransactionType.Withdraw.value:
            return Response({"msg":"You can't withdraw more than 10000"}, status=HTTP_400_BAD_REQUEST)
        
        if request.data.get("transaction_type") == TransactionType.ReFund.value and user.user_type == 3:
            return Response({"msg":"You can't make a refund"}, status=HTTP_400_BAD_REQUEST)

        if user.user_type in [UserType.ADMIN.value, UserType.BANK_STAFF.value]:
            approved=True
            approved_by=user
        else:
            approved=False
            approved_by=None
        

        if serializer.is_valid():
            serializer.save(approved=approved, approved_by=approved_by)
            return Response(serializer.data, status=HTTP_201_CREATED)
        
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class ApproveTransaction(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, pk=None):
        user = request.user
        transaction = Transaction.objects.get(pk=pk)
        serializer = ApproveTransactionSerializer(transaction, data=request.data)

        if user.user_type not in [UserType.ADMIN.value, UserType.BANK_STAFF.value]:
            return Response({"msg":"Only bank staffs and admin can approve transactions"}, status=HTTP_400_BAD_REQUEST)
        
        if serializer.is_valid():
            serializer.save(approved_by=user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
class ViewWalletAndTransactions(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        pk = request.query_params.get("pk")
        wallet = UserWallet.objects.get(user=user)

        if (pk):
            transaction = Transaction.objects.get(pk=pk)

            transactions = [transaction]
        else:
            transactions = Transaction.objects.filter(owner=user)
        transaction_data = [{"id": t.id, "amount": t.amount, "date": t.created_at} for t in transactions]

        wallet = UserWallet.objects.get(user=user)

        return Response({"wallet_balance": wallet.balance, "transactions": transaction_data}, status=HTTP_200_OK)