from django.urls import path
from users.views import CustomerRegistrationView, LoginView, BankStaffRegistrationView, TokenView

urlpatterns = [
    path('customer/register', CustomerRegistrationView.as_view()),
    path('login', LoginView.as_view()),
    path('token', TokenView.as_view()),
    path('staff/register', BankStaffRegistrationView.as_view()),
]