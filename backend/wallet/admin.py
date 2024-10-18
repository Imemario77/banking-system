from django.contrib import admin
from wallet.models import UserWallet, Transaction
# Register your models here.

admin.site.register(UserWallet)
admin.site.register(Transaction)
