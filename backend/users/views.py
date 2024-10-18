from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
# from rest_framework.permissions import IsAuthenticated, IsAdminUser
from users.models import UserType
from users.serializers import RegistrationSerializer, UserSerializer
from rest_framework.response import  Response
from django.contrib.auth import authenticate, login
from users.utils import get_tokens_for_user, get_access_token_from_refresh
from users.permissons import CanCreateBankStaff


class CustomerRegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        user_type = request.data.get('user_type')
        if user_type != UserType.CUSTOMER.value:
            return Response({'user_type': 'you can only register as a customer'},status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        if 'email' not in request.data or 'password' not in request.data:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            auth_data = get_tokens_for_user(request.user)
            serializer = UserSerializer(user) 
            return Response({'user': serializer.data, **auth_data}, status=status.HTTP_200_OK)
        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class TokenView(APIView):
    def post(self, request):
        if 'token' not in request.data:
            return Response({'msg': 'Missing Token Credentials'}, status=status.HTTP_400_BAD_REQUEST)
        token = request.data.get('token')
        new_access = get_access_token_from_refresh(token=token)

        print(new_access)
        
        if token is not None:
            return Response({"token": new_access}, status=status.HTTP_200_OK)
        return Response({'msg': 'Invalid Token'}, status=status.HTTP_401_UNAUTHORIZED)


class BankStaffRegistrationView(APIView):
    permission_classes=[CanCreateBankStaff]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        user_type = request.data.get('user_type')
        is_staff = request.data.get('is_staff')
        if user_type != UserType.BANK_STAFF.value:
            return Response({'user_type': 'this is not a valid user type for staffs'},status=status.HTTP_400_BAD_REQUEST)
        if not is_staff:
            return Response({'is_staff': 'this field must be set to true'},status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

