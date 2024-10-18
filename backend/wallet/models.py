from django.db import models
from users.models import CustomUser
from enum import Enum

# Create your models here.

class TransactionType(Enum):
    Deposit=1
    ReFund=2
    Withdraw=3


class UserWallet(models.Model):
    balance = models.FloatField(default=0.0)
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, null=True, unique=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, null=True, related_name="bank_staff")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} wallet"


class Transaction(models.Model):
    amount = models.FloatField(default=0.0)
    owner = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, null=True)
    approved = models.BooleanField(default=None, null=True)
    approved_by =  models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, null=True, related_name='staff')
    transaction_type= models.SmallIntegerField(default=TransactionType.Deposit.value, choices=[
                                         (ut.value, ut.name) for ut in TransactionType])
    created_at =  models.DateTimeField(auto_now_add=True)
    updated_at =  models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.owner.first_name}  {self.owner.last_name}"